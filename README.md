# Gemini Image Generator MCP Server

Generate high-quality images from text prompts using Google's Gemini model through the MCP protocol.

## Overview

This MCP server allows any AI assistant to generate images using Google's Gemini AI model. The server handles prompt engineering, text-to-image conversion, filename generation, and local image storage, making it easy to create and manage AI-generated images through any MCP client.

## Features

- Text-to-image generation using Gemini 2.0 Flash
- Automatic intelligent filename generation based on prompts
- Local image storage with configurable output path
- Strict text exclusion from generated images
- High-resolution image output

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
                "/Users/bongkilee/Project/mcp-servers/gemini-image-generator",
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

Once installed and configured, you can ask Claude to generate images using prompts like:

- "Generate an image of a sunset over mountains"
- "Create an illustration of a futuristic cityscape"
- "Make a picture of a cat wearing sunglasses"

The generated images will be saved to your configured output path and displayed in Claude.

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
