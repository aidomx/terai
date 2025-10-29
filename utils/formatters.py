from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text
from typing import Generator, Any

def format_markdown_stream(console: Console, stream: Generator, style: str = "cyan") -> str:
    """Format streaming response with markdown"""
    full_response = ""
    accumulated_text = ""
    
    with Live(console=console, refresh_per_second=10) as live:
        for chunk in stream:
            text_chunk = extract_text_from_chunk(chunk)
            if text_chunk:
                full_response += text_chunk
                accumulated_text += text_chunk
                try:
                    md = Markdown(accumulated_text)
                    live.update(md)
                except Exception:
                    live.update(Text(accumulated_text, style=style))
        
        # Final render
        md = Markdown(full_response)
        live.update(md)
    
    return full_response

def format_plain_stream(console: Console, stream: Generator, style: str = "cyan") -> str:
    """Format streaming response as plain text"""
    full_response = ""
    
    console.print(f"[italic {style}]", end="")
    for chunk in stream:
        text_chunk = extract_text_from_chunk(chunk)
        if text_chunk:
            print(text_chunk, end="", flush=True)
            full_response += text_chunk
    console.print(f"[/italic {style}]")
    
    return full_response

def extract_text_from_chunk(chunk: Any) -> str:
    """Extract text from different AI provider chunks"""
    # Gemini chunks
    if hasattr(chunk, 'text') and chunk.text:
        return chunk.text
    
    # OpenAI chunks
    if (hasattr(chunk, 'choices') and 
        chunk.choices and 
        hasattr(chunk.choices[0].delta, 'content') and 
        chunk.choices[0].delta.content is not None):
        return chunk.choices[0].delta.content
    
    return ""
