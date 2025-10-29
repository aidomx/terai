from rich.console import Console
from typing import Generator, Any
from utils.formatters import format_markdown_stream, format_plain_stream

class StreamHandler:
    """Handle streaming responses from AI providers"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def handle_stream(self, stream: Generator, use_markdown: bool = True, style: str = "cyan") -> str:
        """Handle streaming response with formatting"""
        if use_markdown:
            return format_markdown_stream(self.console, stream, style)
        else:
            return format_plain_stream(self.console, stream, style)
    
    def handle_gemini_stream(self, stream: Generator, use_markdown: bool = True) -> str:
        """Handle Gemini-specific streaming"""
        return self.handle_stream(stream, use_markdown, "cyan")
    
    def handle_openai_stream(self, stream: Generator, use_markdown: bool = True) -> str:
        """Handle OpenAI-specific streaming"""
        return self.handle_stream(stream, use_markdown, "green")
