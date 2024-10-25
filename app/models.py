from diffusers import AutoPipelineForInpainting
import torch
import logging

logger = logging.getLogger("InpaintLogging")

def load_inpainting_model(model_name: str):
    """
    Load the inpainting model pipeline from Hugging Face Diffusers.

    Args:
        model_name (str): The model name to load from Hugging Face. Default is runwayml/stable-diffusion-inpainting.

    Returns:
        The inpainting model pipeline.
    """
    torch_dtype =torch.float16 if torch.cuda.is_available() else torch.float32
    logger.info(f"Loading inpainting model on {'GPU' if torch.cuda.is_available() else 'CPU'}...")

    try:
        pipe = AutoPipelineForInpainting.from_pretrained(model_name, torch_dtype=torch_dtype)
        logger.info("Model loaded successfully.")

        if torch.cuda.is_available():
            pipe.enable_model_cpu_offload()
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise RuntimeError("Failed to load inpainting model") from e

    return pipe
