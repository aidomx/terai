import sys
from typing import Any, Dict
from rich.console import Console

def handle_error(console: Console, error: Exception, context: str = ""):
    """Handle and display errors consistently"""
    error_msg = f"❌ [red]Error {context}: {str(error)}[/red]"
    console.print(error_msg)
    
def validate_response(response: Any, console: Console) -> bool:
    """Validate AI response"""
    if response is None:
        console.print("🔄 [yellow]No response received. Please try again...[/yellow]")
        return False
    elif isinstance(response, str) and not response.strip():
        console.print("🔄 [yellow]Empty response received. Please try again...[/yellow]")
        return False
    return True

def format_provider_name(provider: str) -> str:
    """Format provider name for display"""
    return provider.upper()

def get_user_input(prompt: str = "👤 You: ") -> str:
    """Get user input with consistent prompt"""
    return input(f"\n{prompt}").strip()

def exit_application(console: Console, message: str = "Goodbye!"):
    """Exit application gracefully"""
    console.print(f"\n👋 [bold yellow]{message}[/bold yellow]")
    sys.exit(0)
