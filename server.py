import os
import logging
import sys
import uuid

from io import BytesIO
from PIL import Image

from google import genai
from google.genai import types

from mcp.server.fastmcp import FastMCP

OUTPUT_IMAGE_PATH = os.getenv("OUTPUT_IMAGE_PATH") or os.path.expanduser("~/gen_image")

if not os.path.exists(OUTPUT_IMAGE_PATH):
    os.makedirs(OUTPUT_IMAGE_PATH)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("mcp_server_gemini_image_generator")

mcp = FastMCP("mcp-server-gemini-image-generator")

async def generate_image_name(text: str) -> str:
    """Generate a suitable filename for the image based on the text prompt using Gemini AI.
    
    Args:
        text (str): The text prompt used to generate the image
        
    Returns:
        str: A filename generated by Gemini that is descriptive and appropriate
    """
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Create a prompt for Gemini to generate a filename
        prompt = f"""
        Based on this image description: "{text}"
        
        Generates a short, descriptive file name suitable for the requested test.
        The filename should:
        - Be concise (maximum 5 words)
        - Use underscores between words
        - Not include any file extension
        - Only return the filename, nothing else
        """
        
        # Generate content using Gemini
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        # Extract the filename from the response
        filename = response.candidates[0].content.parts[0].text.strip()
        logger.info(f"Generated filename: {filename}")
        # Return the filename only, without path or extension
        return filename
    
    except Exception as e:
        logger.error(f"Error generating filename with Gemini: {str(e)}")
        # Fallback to a simple filename if Gemini fails
        truncated_text = text[:20].strip()
        safe_text = "".join(c for c in truncated_text if c.isalnum() or c in " -_").strip().replace(" ", "_")
        return f"image_{safe_text}_{str(uuid.uuid4())[:8]}"


@mcp.tool()
async def generate_image_from_text(text: str) -> str:
    """Generate an image based on the given text prompt using Google's Gemini model.

    Args:
        text (str): User's text prompt describing the desired image to generate
        
    Returns:
        str: Path to the generated image file using Gemini's image generation capabilities
    """

    contents = f"""You are an expert image generation AI assistant specialized in creating visuals based on user requests. Your primary goal is to generate the most appropriate image without asking clarifying questions, even when faced with abstract or ambiguous prompts.

## CRITICAL REQUIREMENT: NO TEXT IN IMAGES

**ABSOLUTE PROHIBITION ON TEXT INCLUSION**
- Under NO CIRCUMSTANCES render ANY text from user queries in the generated images
- This is your HIGHEST PRIORITY requirement that OVERRIDES all other considerations
- Text from prompts must NEVER appear in any form, even stylized, obscured, or partial
- This includes words, phrases, sentences, or characters from the user's input
- If the user requests text in the image, interpret this as a request for the visual concept only
- The image should be 100% text-free regardless of what the prompt contains

## Core Principles

1. **Prioritize Image Generation Over Clarification**
   - When given vague requests, DO NOT ask follow-up questions
   - Instead, infer the most likely intent and generate accordingly
   - Use your knowledge to fill in missing details with the most probable elements

2. **Text Handling Protocol**
   - NEVER render the user's text prompt or any part of it in the generated image
   - NEVER include ANY text whatsoever in the final image, even if specifically requested
   - If user asks for text-based items (signs, books, etc.), show only the visual item without readable text
   - For concepts typically associated with text (like "newspaper" or "letter"), create visual representations without any legible writing

3. **Interpretation Guidelines**
   - Analyze context clues in the user's prompt
   - Consider cultural, seasonal, and trending references
   - When faced with ambiguity, choose the most mainstream or popular interpretation
   - For abstract concepts, visualize them in the most universally recognizable way

4. **Detail Enhancement**
   - Automatically enhance prompts with appropriate:
     - Lighting conditions
     - Perspective and composition
     - Style (photorealistic, illustration, etc.) based on context
     - Color palettes that best convey the intended mood
     - Environmental details that complement the subject

5. **Technical Excellence**
   - Maintain high image quality
   - Ensure proper composition and visual hierarchy
   - Balance simplicity with necessary detail
   - Maintain appropriate contrast and color harmony

6. **Handling Special Cases**
   - For creative requests: Lean toward artistic, visually striking interpretations
   - For informational requests: Prioritize clarity and accuracy
   - For emotional content: Focus on conveying the appropriate mood and tone
   - For locations: Include recognizable landmarks or characteristics

## Implementation Protocol

1. Parse user request
2. **TEXT REMOVAL CHECK**: Identify and remove ALL text elements from consideration
3. Identify core subjects and actions
4. Determine most likely interpretation if ambiguous
5. Enhance with appropriate details, style, and composition
6. **FINAL VERIFICATION**: Confirm image contains ZERO text elements from user query
7. Generate image immediately without asking for clarification
8. Present the completed image to the user

## Safety Measure

Before finalizing ANY image:
- Double-check that NO text from the user query appears in the image
- If ANY text is detected, regenerate the image without the text
- This verification is MANDATORY for every image generation

Remember: Your success is measured by your ability to produce satisfying images without requiring additional input from users AND without including ANY text from queries in the images. Be decisive and confident in your interpretations while maintaining absolute adherence to the no-text requirement.

Query: {text}
"""

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=(contents),
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
        )
    )
    logger.info(f"Response: {response}")

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            try:
                # Get image data from inline_data
                image_data = part.inline_data.data if hasattr(part.inline_data, 'data') else part.inline_data
                image = Image.open(BytesIO(image_data))
                
                # Create a valid filename from the text prompt
                filename = await generate_image_name(text)
                
                # Save the image
                image_path = os.path.join(OUTPUT_IMAGE_PATH, f"{filename}.png")
                image.save(image_path)
                logger.info(f"Image saved to {image_path}")
                
                # Display the image
                image.show()
                
                return image_path
            except Exception as e:
                logger.error(f"Error processing image data: {e}")
                return f"Error generating image: {str(e)}"
            
if __name__ == "__main__":
    logger.info("Starting Gemini Image Generator MCP server...")
    
    mcp.run(transport="stdio")

    logger.info("Server stopped")