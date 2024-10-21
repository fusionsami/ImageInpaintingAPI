from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel, Field, ValidationError, BaseSettings
from PIL import Image, ImageOps
import io
import logging
from dotenv import load_dotenv

from utils import validate_image, pad_image, create_mask, inpaint_image
from models import load_inpainting_model

load_dotenv()
class Settings(BaseSettings):
    target_width: int = Field(512, description="Default target width for inpainted images")
    target_height: int = Field(512, description="Default target height for inpainted images")

    class Config:
        env_file = ".env" 

settings = Settings()
app = FastAPI()

#Logger with date, time, and line number
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

pipe = load_inpainting_model()

#Pydantic model for validating input parameters
class ImageSize(BaseModel):
    width: int = Field(..., gt=0, le=4096, description="The target width for the inpainted image (must be between 1 and 4096)")
    height: int = Field(..., gt=0, le=4096, description="The target height for the inpainted image (must be between 1 and 4096)")

@app.post("/inpaint/")
async def inpaint(image: UploadFile = File(...), width: int = Form(...), height: int = Form(...)):
    """
    API endpoint to perform image inpainting.

    Args:
        image (UploadFile): The image file to be inpainted.
        width (int): The target width for the inpainted image. Default is 512.
        height (int): The target height for the inpainted image. Default is 512.

    Returns:
        dict: Response inpainted image.

    Raises:
        HTTPException: If an error occurs during image processing or validation.
    """

    try:
        params = ImageSize(width=width, height=height)
        logger.info(f"Received image for inpainting with target dimensions: {params.width}x{params.height}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=e.errors())
    
    image_bytes = await image.read()
    if not image_bytes:
        logger.error("Uploaded file is empty.")
        raise HTTPException(status_code=400, detail="No image file uploaded or file is empty.")
    
    validated_image = validate_image(image_bytes)
    padded_image = pad_image(validated_image, width, height)
    mask = create_mask(validated_image, width, height)

    inpainted_image = inpaint_image(pipe,padded_image,mask,width,height)
    
    return StreamingResponse(inpainted_image, media_type="image/jpeg")


