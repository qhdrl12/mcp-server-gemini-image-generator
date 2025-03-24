# Gemini Image Generator MCP Server

Generate high-quality images from text prompts using Google's Gemini model through the MCP protocol.

## Overview

This MCP server allows any AI assistant to generate images using Google's Gemini AI model. The server handles prompt engineering, text-to-image conversion, filename generation, and local image storage, making it easy to create and manage AI-generated images through any MCP client.

## Features

- Text-to-image generation using Gemini 2.0 Flash
- Image-to-image transformation based on text prompts
- Support for both file-based and base64-encoded images
- Automatic intelligent filename generation based on prompts
- Automatic translation of non-English prompts
- Local image storage with configurable output path
- Strict text exclusion from generated images
- High-resolution image output

## Available MCP Tools

The server provides the following MCP tools for AI assistants:

### 1. `generate_image_from_text`

Creates a new image from a text prompt description.

```
generate_image_from_text(prompt: str) -> str
```

**Parameters:**
- `prompt`: Text description of the image you want to generate

**Returns:**
- Path to the generated image file

**Example:**
- "Generate an image of a sunset over mountains"
- "Create a photorealistic flying pig in a sci-fi city"

### 2. `transform_image_from_encoded`

Transforms an existing image based on a text prompt using base64-encoded image data.

```
transform_image_from_encoded(encoded_image: str, prompt: str) -> str
```

**Parameters:**
- `encoded_image`: Base64 encoded image data with format header (must be in format: "data:image/[format];base64,[data]")
- `prompt`: Text description of how you want to transform the image

**Returns:**
- Path to the transformed image file

**Example:**
- "Add snow to this landscape"
- "Change the background to a beach"

### 3. `transform_image_from_file`

Transforms an existing image file based on a text prompt.

```
transform_image_from_file(image_file_path: str, prompt: str) -> str
```

**Parameters:**
- `image_file_path`: Path to the image file to be transformed
- `prompt`: Text description of how you want to transform the image

**Returns:**
- Path to the transformed image file

**Example:**
- "Add a llama next to the person in this image"
- "Make this daytime scene look like night time"

## Setup

### Prerequisites

- Python 3.11+
- Google AI API key (Gemini)
- MCP host application (Claude Desktop App, Cursor, or other MCP-compatible clients)

### Getting a Gemini API Key

1. Visit [Google AI Studio API Keys page](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your new API key for use in the configuration
5. Note: The API key provides a certain quota of free usage per month. You can check your usage in the Google AI Studio

### Installation

1. Clone the repository:
```
git clone https://github.com/your-username/gemini-image-generator.git
cd gemini-image-generator
```

2. Create a virtual environment and install dependencies:
```
# Using regular venv
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Or using uv
uv venv
source .venv/bin/activate
uv pip install -e .
```

3. Copy the example environment file and add your API key:
```
cp .env.example .env
```

4. Edit the `.env` file to include your Google Gemini API key and preferred output path:
```
GEMINI_API_KEY="your-gemini-api-key-here"
OUTPUT_IMAGE_PATH="/path/to/save/images"
```

### Configure Claude Desktop

Add the following to your `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
    "mcpServers": {
        "gemini-image-generator": {
            "command": "uv",
            "args": [
                "--directory",
                "/absolute/path/to/gemini-image-generator",
                "run",
                "server.py"
            ],
            "env": {
                "GEMINI_API_KEY": "GEMINI_API_KEY",
                "OUTPUT_IMAGE_PATH": "OUTPUT_IMAGE_PATH"
            }
        }
    }
}
```

## Usage

Once installed and configured, you can ask Claude to generate or transform images using prompts like:

### Generating New Images
- "Generate an image of a sunset over mountains"
- "Create an illustration of a futuristic cityscape"
- "Make a picture of a cat wearing sunglasses"

### Transforming Existing Images
- "Transform this image by adding snow to the scene"
- "Edit this photo to make it look like it was taken at night"
- "Add a dragon flying in the background of this picture"

The generated/transformed images will be saved to your configured output path and displayed in Claude.

## Testing

You can test the application by running the FastMCP development server:

```
fastmcp dev server.py
```

This command starts a local development server and makes the MCP Inspector available at http://localhost:5173/. 
The MCP Inspector provides a convenient web interface where you can directly test the image generation tool without needing to use Claude or another MCP client. 
You can enter text prompts, execute the tool, and see the results immediately, which is helpful for development and debugging.

## License

MIT License
