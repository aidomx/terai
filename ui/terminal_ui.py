# ui/terminal_ui.py
import os
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.box import ROUNDED, DOUBLE
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.patch_stdout import patch_stdout

class TerminalUI:
    """Advanced Terminal UI with fixed input and scrollable chat area"""

    def __init__(self, console: Console):
        self.console = console
        self.chat_history: List[Dict[str, Any]] = []
        self.layout = Layout()
        self.setup_layout()
        # Setup prompt session
        self.session = PromptSession()
        self.bindings = KeyBindings()
        self.setup_keybindings()

    def setup_layout(self):
        """Setup Rich layout with chat area and input area"""
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="chat", ratio=1),
            Layout(name="input_area", size=3)
        )
        # Header
        self.layout["header"].update(
            Panel(
                Text("🤖 Terminal AI - Hybrid AI Assistant", style="bold cyan"),
                style="green",
                box=ROUNDED
            )
        )
        # Initial chat area
        self.layout["chat"].update(
            Panel(
                Text("Start chatting with AI...", style="dim"),
                title="💬 Chat",
                border_style="blue",
                box=ROUNDED
            )
        )
        # Input area
        self.layout["input_area"].update(
            Panel(
                Text("Type your message and press ENTER...", style="dim"),
                title="",
                border_style="yellow",
                box=ROUNDED
            )
        )

    def setup_keybindings(self):
        """Setup custom keybindings"""
        @self.bindings.add('c-c')
        def _(event):
            event.app.exit()

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_welcome(self):
        """Display welcome screen"""
        self.clear_screen()
        welcome_text = """
[bold cyan]🤖 Terminal AI - Hybrid AI Assistant[/bold cyan]

[bold yellow]Available Commands:[/bold yellow]
  • Just type to chat with AI
  • [cyan]/quit[/cyan] or [cyan]/q[/cyan] - Exit application
  • [cyan]/clear[/cyan] or [cyan]/c[/cyan] - Clear conversation
  • [cyan]/help[/cyan] or [cyan]/h[/cyan] - Show help
  • [cyan]/model[/cyan] or [cyan]/m[/cyan] - Change AI model
  • [cyan]/provider[/cyan] or [cyan]/p[/cyan] - Switch AI provider
  • [cyan]/markdown on|off[/cyan] - Toggle markdown

[bold green]Press ENTER to start chatting...[/bold green]
"""
        self.console.print(Panel(welcome_text, title="Welcome", style="green", box=DOUBLE))

    def add_message(self, role: str, content: str, provider: str = ""):
        """Add message to chat history"""
        self.chat_history.append({
            "role": role,
            "content": content,
            "provider": provider
        })
        self._update_chat_display()

    def _update_chat_display(self):
        """Update the chat display with current history"""
        chat_content = Text()

        for msg in self.chat_history[-50:]:  # Show last 50 messages
            if msg["role"] == "user":
                chat_content.append("👤 You: ", style="bold green")
                chat_content.append(f"{msg['content']}\n\n", style="white")
            else:
                provider_tag = f" ({msg['provider'].upper()})" if msg["provider"] else ""
                chat_content.append(f"🤖 AI{provider_tag}: ", style="bold blue")
                chat_content.append(f"{msg['content']}\n\n", style="cyan")

        if not self.chat_history:
            chat_content.append("Start chatting with AI...", style="dim")

        self.layout["chat"].update(
            Panel(
                chat_content,
                title="💬 Chat History",
                border_style="blue",
                box=ROUNDED
            )
        )

    def display_chat_interface(self, current_provider: str, current_model: str, use_markdown: bool):
        """Display the main chat interface"""
        self.clear_screen()

        # Update status in header
        status_text = Text()
        status_text.append("🤖 Terminal AI", style="bold cyan")
        status_text.append(" | ")
        status_text.append(f"Provider: {current_provider.upper()}", style="yellow")
        status_text.append(" | ")
        status_text.append(f"Model: {current_model}", style="green")
        status_text.append(" | ")
        status_text.append(f"Markdown: {'ON' if use_markdown else 'OFF'}", style="magenta")
        status_text.append(" | ")
        status_text.append("Type /help for commands", style="dim")

        self.layout["header"].update(
            Panel(status_text, style="green", box=ROUNDED)
        )

        # Display the layout
        self.console.print(self.layout)

    def get_user_input(self) -> str:
        """Get user input with fixed position"""
        try:
            with patch_stdout():
                user_input = self.session.prompt(
                    #HTML('<ansigreen>👤 You:</ansigreen> '),
                    key_bindings=self.bindings
                    #bottom_toolbar=HTML('<style bg="ansiblue" fg="ansiblack"> Press Ctrl+D to exit • Enter to send </style>')
                )
            return user_input.strip()
        except KeyboardInterrupt:
            return "/quit"
        except EOFError:
            return "/quit"

    def show_thinking_indicator(self, provider: str):
        """Show thinking indicator"""
        thinking_text = Text()
        thinking_text.append(f"🤖 {provider.upper()} is thinking...", style="bold yellow")

        self.layout["input_area"].update(
            Panel(thinking_text, title="⚡ Status", border_style="yellow", box=ROUNDED)
        )
        self.console.print(self.layout)

    def show_responding_indicator(self):
        """Show responding indicator"""
        self.layout["input_area"].update(
            Panel(
                Text("AI is responding...", style="dim"),
                title="",
                border_style="yellow",
                box=ROUNDED
            )
        )
        self.console.print(self.layout)

    def restore_input_prompt(self):
        """Restore input prompt after response"""
        self.layout["input_area"].update(
            Panel(
                Text("Type your message...", style="dim"),
                title="",
                border_style="yellow",
                box=ROUNDED
            )
        )
        self.console.print(self.layout)

    def show_message(self, message: str, message_type: str = "info"):
        """Show temporary message"""
        styles = {
            "info": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red"
        }

        self.layout["input_area"].update(
            Panel(
                Text(message, style=styles.get(message_type, "blue")),
                title="💡 Message",
                border_style=styles.get(message_type, "blue"),
                box=ROUNDED
            )
        )
        self.console.print(self.layout)
