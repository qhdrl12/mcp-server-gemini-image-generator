import asyncio

from . import server


def main() -> None:
    """Start the MCP server."""
    server.main()

__all__ = [
    "main",
    "server",
]