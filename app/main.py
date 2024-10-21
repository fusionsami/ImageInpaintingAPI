from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, ValidationError, BaseSettings, validator
from dotenv import load_dotenv

from utils import validate_image, pad_image, create_mask, inpaint_image
from models import load_inpainting_model
from logging_config import setup_logging

class Settings(BaseSettings):
    PROMPT: str = Field(..., description="Prompt for inpainting")
    NEGATIVE_PROMPT: str = Field(..., description="Negative prompt for inpainting")
    GUIDANCE_SCALE: float = Field(..., description="Guidance scale for inpainting")
    STRENGTH: float = Field(..., description="Strength for inpainting")
    MODEL_NAME: str = Field(description="Model name for inpainting")
    NUM_INFERENCE_STEPS: int = Field(..., description="Num inference steps")


    class Config:
        env_file = ".env" 

settings = Settings()
app = FastAPI()

logger = setup_logging() 

pipe = load_inpainting_model(settings.MODEL_NAME)


class ImageSize(BaseModel):
    width: int = Field(...)
    height: int = Field(...)

    @validator("width")
    def validate_width(cls, value):
        if value <= 0 or value % 8 != 0:
            raise ValueError("Width must be a positive even number divisible by 8.")
        return value

    @validator("height")
    def validate_height(cls, value):
        if value <= 0 or value % 8 != 0:
            raise ValueError("Height must be a positive even number divisible by 8.")
        return value

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

    inpainted_image = inpaint_image(pipe,padded_image,mask,width,height, settings)
    
    return StreamingResponse(inpainted_image, media_type="image/jpeg")


