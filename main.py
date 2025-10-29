#!/usr/bin/env python3
"""
Terminal AI - Modern Hybrid AI Chat Assistant dengan Textual UI
Author: Aidomx
Version: 1.0
"""

import sys
from rich.console import Console

# Import modular components
from config.settings import Settings
from clients import ClientManager
from handlers.chat_handler import ChatHandler

def main():
    """Main function"""
    try:
        # Initialize rich console
        console = Console()
        # Load settings
        settings = Settings()
        settings.validate_api_keys()
        # Initialize clients
        client_manager = ClientManager(settings, console)
        # Initialize chat handler
        chat_handler = ChatHandler(client_manager, console, settings)
        # Show welcome
        chat_handler.print_welcome()
        # Main menu loop
        while True:
            try:
                user_input = input("\n> ").strip()
                should_continue = chat_handler.process_user_input(user_input)
                if not should_continue:
                    break
            except KeyboardInterrupt:
                console.print("\n\n👋 [bold yellow]Sampai jumpa![/bold yellow]")
                break
            except Exception as e:
                console.print(f"\n❌ [red]Error: {e}[/red]")
                console.print("🔄 [yellow]Silakan coba lagi...[/yellow]")
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
