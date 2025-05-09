import base64
import io
import logging
import os

import PIL.Image

logger = logging.getLogger(__name__)

OUTPUT_IMAGE_PATH = os.getenv("OUTPUT_IMAGE_PATH") or os.path.expanduser("~/gen_image")

if not os.path.exists(OUTPUT_IMAGE_PATH):
    os.makedirs(OUTPUT_IMAGE_PATH)

def validate_base64_image(base64_string: str) -> bool:
    """Validate if a string is a valid base64-encoded image.

    Args:
        base64_string: The base64 string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        # Try to decode base64
        image_data = base64.b64decode(base64_string)

        # Try to open as image
        with PIL.Image.open(io.BytesIO(image_data)) as img:
            logger.debug(
                f"Validated base64 image, format: {img.format}, size: {img.size}"
            )
            return True

    except Exception as e:
        logger.warning(f"Invalid base64 image: {str(e)}")
        return False
    
async def save_image(image_data: bytes, filename: str) -> str:
    """Save image data to disk with a descriptive filename.
    
    Args:
        image_data: Raw image data
        filename: Base string to use for generating filename
        
    Returns:
        Path to the saved image file
    """
    try:
        # Open image from bytes
        image = PIL.Image.open(io.BytesIO(image_data))
        
        # Save the image
        image_path = os.path.join(OUTPUT_IMAGE_PATH, f"{filename}.png")
        image.save(image_path)
        logger.info(f"Image saved to {image_path}")
        
        # Display the image
        image.show()
        
        return image_path
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        raise
