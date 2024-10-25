# utils.py
import io
import logging
from PIL import Image, ImageOps
from fastapi import HTTPException

logger = logging.getLogger("InpaintLogging")

def validate_image(image_bytes: bytes) -> Image.Image:
    """
    Validate and open the image from bytes.

    Args:
        image_bytes (bytes): The image bytes to validate.

    Returns:
        Image.Image: The opened PIL Image.

    Raises:
        HTTPException: If the image is invalid or corrupted.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.convert("RGB")
        image.verify()
        logger.info(f"Uploaded image format: {image.format}, size: {image.size}")
        return image
    except IOError as e:
        logger.error(f"Error loading image: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid image file or corrupted.")
    except Exception as e:
        logger.error(f"Unexpected error loading image: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while reading the image.")


def calculate_padding(original_width: int, original_height: int, target_width: int, target_height: int):
    """
    Calculate the padding values needed to resize an image to the target dimensions.

    Args:
        original_width (int): The width of the original image.
        original_height (int): The height of the original image.
        target_width (int): The desired width after padding.
        target_height (int): The desired height after padding.

    Returns:
        tuple: Padding values (left, top, right, bottom)
    """
    left_padding = (target_width - original_width) // 2
    top_padding = (target_height - original_height) // 2
    right_padding = target_width - original_width - left_padding
    bottom_padding = target_height - original_height - top_padding

    return left_padding, top_padding, right_padding, bottom_padding

def pad_image(original_image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """
    Pad the original image to fit the target dimensions.

    Args:
        original_image (Image.Image): The original image to pad.
        target_width (int): The target width after padding.
        target_height (int): The target height after padding.

    Returns:
        Image.Image: The padded image.
    """
    original_width, original_height = original_image.size

    left_padding, top_padding, right_padding, bottom_padding = calculate_padding(
        original_width, original_height, target_width, target_height
    )

    padded_image = ImageOps.expand(original_image, (left_padding, top_padding, right_padding, bottom_padding), fill=0)

    return padded_image




def create_mask(original_image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """
    Create a mask based on the padding of the original image.

    Args:
        original_image (Image.Image): The original image dimensions to base the mask on.
        target_width (int): The target width for the mask.
        target_height (int): The target height for the mask.

    Returns:
        Image.Image: The created mask image.
    """
    original_width, original_height = original_image.size

    left_padding, top_padding, right_padding, bottom_padding = calculate_padding(
        original_width, original_height, target_width, target_height
    )

    mask = Image.new("L", (target_width, target_height), 0)  # Start with a black mask
    mask.paste(255, (0, 0, left_padding, target_height))  # Left padding
    mask.paste(255, (target_width - right_padding, 0, target_width, target_height))  # Right padding
    mask.paste(255, (0, 0, target_width, top_padding))  # Top padding
    mask.paste(255, (0, target_height - bottom_padding, target_width, target_height))  #bottom padding

    return mask


def inpaint_image(pipe, padded_image: Image.Image, mask: Image.Image, width: int, height: int, settings):
    """
    Perform inpainting on the padded image using the provided mask.

    Args:
        pipe: The inpainting pipeline.
        padded_image (Image.Image): The padded image.
        mask (Image.Image): The mask image.

    Returns:
        Image.Image: The inpainted image.

    Raises:
        HTTPException: If an error occurs during inpainting.
    """
    try:

        params = {
            'image': padded_image,
            'mask_image': mask,
            'width': width,
            'height': height,
        }

        if settings.PROMPT is not None:
            params['prompt'] = settings.PROMPT
        else:
            params['prompt'] = "expand image, resize and fill naturally, high resolution, natural continuation, natural background characters, realistic background characters"
        
        if settings.NEGATIVE_PROMPT is not None:
            params['negative_prompt'] = settings.NEGATIVE_PROMPT
        else:
            params['negative_prompt'] = "blurry, image repeat, distorted, unclear, low resolution, Double head, Double figure, double body, Disfigured body, logo, watermark, text, title, signature, words, letters, characters, subtitle, cropped, zoomed, extra fingers, extra limbs, unnatural hands, extra legs, disfigured, disfigured fingers, disfigured hands, glasses, straws, unnatural background characters"
        
        if settings.GUIDANCE_SCALE is not None:
            params['guidance_scale'] = settings.GUIDANCE_SCALE

        if settings.STRENGTH is not None:
            params['strength'] = settings.STRENGTH

        if settings.NUM_INFERENCE_STEPS is not None:
            params['num_inference_steps'] = settings.NUM_INFERENCE_STEPS

        logger.info(f"width: {width}, height: {height}, NUM_INFERENCE_STEPS: {settings.NUM_INFERENCE_STEPS}, guidance_scale: {settings.GUIDANCE_SCALE}, STRENGTH: {settings.STRENGTH}")

        inpainted_image = pipe(**params).images[0]

        img_byte_arr = io.BytesIO()
        inpainted_image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        logger.info("Image inpainting successful")
        return img_byte_arr

    except Exception as e:
        logger.error(f"Error during inpainting: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during inpainting.")

   