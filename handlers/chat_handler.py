import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from models.chat_models import ChatHistory

# Import modular components
from .command_handler import CommandHandler
from .provider_manager import ProviderManager
from .ui_launcher import UILauncher
from .session_manager import SessionManager

class ChatHandler:
    """Main coordinator untuk chat interactions"""
    
    def __init__(self, client_manager, console: Console, settings):
        self.client_manager = client_manager
        self.console = console
        self.settings = settings
        
        # Initialize modular components
        self.provider_manager = ProviderManager(client_manager, console)
        self.command_handler = CommandHandler(console, self)
        self.ui_launcher = UILauncher(console)
        self.session_manager = SessionManager(settings)
    
    def print_welcome(self):
        """Print simple welcome message"""
        self._clear_screen()
        
        welcome_text = """
[bold cyan]
╔══════════════════════════════════════╗
║             TERMINAL AI              ║
║          (Terai - Terminal AI)       ║
╚══════════════════════════════════════╝
[/bold cyan]

Selamat datang di Terai!
Ketik 'help' untuk melihat informasi
"""
        self.console.print(welcome_text)
    
    def start_chat_session(self):
        """Start chat session dengan modern UI"""
        return self.ui_launcher.launch_chat_ui(self)
    
    def _get_ai_response(self, user_input: str) -> str:
        """Get AI response (untuk Textual UI)"""
        return self.session_manager.get_ai_response(
            self.client_manager,
            self.provider_manager.current_provider,
            self.provider_manager.current_model,
            user_input
        )
    
    def process_user_input(self, user_input: str):
        """Process user input in main menu"""
        user_input = user_input.strip().lower()
        
        if user_input == 'quit':
            self.console.print("\n👋 [bold yellow]Terima kasih telah menggunakan Terai![/bold yellow]")
            return False
            
        elif user_input == 'startchat':
            self.start_chat_session()
            self.print_welcome()  # Show welcome again after chat
            return True
            
        elif user_input == 'model':
            self.provider_manager.change_model()
            return True
            
        elif user_input == 'provider':
            self.provider_manager.change_provider()
            return True
            
        elif user_input == 'config':
            self.command_handler.show_config(
                self.provider_manager.current_provider,
                self.provider_manager.current_model,
                self.session_manager.use_markdown,
                len(self.session_manager.history.messages)
            )
            return True
            
        elif user_input == 'help':
            self.command_handler.show_help()
            return True
            
        elif user_input:
            self.command_handler.show_unknown_command()
            return True
            
        return True
    
    # Property accessors untuk modular components
    @property
    def current_provider(self):
        return self.provider_manager.current_provider
    
    @property
    def current_model(self):
        return self.provider_manager.current_model
    
    @property
    def history(self):
        return self.session_manager.history
    
    @property
    def use_markdown(self):
        return self.session_manager.use_markdown
    
    def _clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
