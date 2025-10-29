from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Header, Static, TextArea
from textual.reactive import reactive
from textual import events
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
import asyncio

class ChatMessage(Static):
    """Widget untuk menampilkan pesan chat"""

    def __init__(self, message: str, is_user: bool = False, provider: str = ""):
        super().__init__()
        self.message = message
        self.is_user = is_user
        self.provider = provider

    def render(self) -> Panel:
        """Render chat message dengan markdown"""
        if self.is_user:
            # Gunakan Text untuk pesan pengguna
            content = Text(f"👤 Anda:\n{self.message}", style="green")
            return Panel(content, border_style="green")
        else:
            provider_tag = f" ({self.provider.upper()})" if self.provider else ""
            try:
                # Gunakan Markdown untuk pesan AI
                full_content = f"🤖 AI{provider_tag}:\n\n{self.message}"
                md_content = Markdown(full_content)
                return Panel(md_content, border_style="blue")
            except Exception:
                # Fallback jika rendering Markdown gagal
                content = Text(f"🤖 AI{provider_tag}: {self.message}", style="cyan")
                return Panel(content, border_style="blue")

class ChatArea(VerticalScroll):
    """Area untuk menampilkan history chat"""
    def add_message(self, message: str, is_user: bool = False, provider: str = ""):
        """Tambahkan pesan ke chat area"""
        chat_message = ChatMessage(message, is_user, provider)
        self.mount(chat_message)
        # Scroll ke akhir setelah menambahkan pesan
        self.scroll_end(animate=False)

# Dummy ChatHandler untuk membuat aplikasi bisa berjalan
class DummyChatHandler:
    def __init__(self):
        self.current_provider = "gemini"
        self.current_model = "flash"

    def _get_ai_response(self, user_message: str) -> str:
        # Simulasi respons AI
        return f"Saya menerima pesan Anda: '{user_message}'. Respons ini berasal dari {self.current_provider.upper()} model {self.current_model}."

class ChatApp(App):
    """Aplikasi Chat dengan Textual - Working Ctrl+Enter"""
    CSS_PATH = "style.css"
    current_provider = reactive("")
    current_model = reactive("")
    chat_handler = None
    welcome_shown = False

    def __init__(self, chat_handler, **kwargs):
        super().__init__(**kwargs)
        self.chat_handler = chat_handler
        # Inisialisasi reactive state
        self.current_provider = chat_handler.current_provider
        self.current_model = chat_handler.current_model

    def compose(self) -> ComposeResult:
        """Compose the app UI"""
        yield Header()
        yield ChatArea(id="chat-area")

        with Container(id="input-container"):
            yield TextArea(
                placeholder="Apa yang anda butuhkan?",
                id="text-input",
                show_line_numbers=False
            )
            with Container(id="btn-container"):
              yield Button(
                  "➤",
                  id="send-button",
                  classes="send-button"
              )

    def on_mount(self) -> None:
        """Called when app starts"""
        self.title = "Terai"
        self.sub_title = f"{self.current_model} • ctrl+q (exit)"

        # Focus on textarea
        textarea = self.query_one("#text-input", TextArea)
        textarea.focus()

        # Add welcome message hanya sekali di awal
        if not self.welcome_shown:
            chat_area = self.query_one("#chat-area")
            # Pastikan Static welcome message tidak memiliki class "thinking"
            welcome_msg = "Selamat datang! Saya adalah asisten AI Anda. Apa yang bisa saya bantu hari ini?"
            welcome_static = Static(welcome_msg, classes="welcome-message")
            chat_area.mount(welcome_static)
            self.welcome_shown = True
            chat_area.scroll_end(animate=False)

    async def on_key(self, event: events.Key) -> None:
        """Handle Ctrl+Enter untuk kirim pesan"""
        # Cek jika Ctrl+Enter ditekan
        if event.key == "ctrl+j" or event.key == "ctrl+enter":
            await self.send_message()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handler saat tombol diklik."""
        if event.button.id == "send-button":
            # Panggil handler kirim pesan
            asyncio.create_task(self.send_message())

    async def send_message(self) -> None:
        """Handle message sending"""
        textarea = self.query_one("#text-input", TextArea)
        message = textarea.text.strip()

        if not message:
            return

        # Clear textarea
        textarea.text = ""

        # Add user message to chat
        chat_area = self.query_one("#chat-area")
        chat_area.add_message(message, is_user=True)

        # Show thinking indicator
        thinking_msg = Static("🤖 AI sedang mengetik...", classes="thinking")
        chat_area.mount(thinking_msg)
        chat_area.scroll_end(animate=False)

        # Get AI response
        await self.get_ai_response(message, thinking_msg)

    async def get_ai_response(self, user_message: str, thinking_msg: Static) -> None:
        """Get AI response asynchronously"""
        chat_area = self.query_one("#chat-area")

        try:
            # Hapus pesan 'sedang mengetik'
            thinking_msg.remove()
            response = await asyncio.get_event_loop().run_in_executor(
                None, self._get_sync_response, user_message
            )

            if response:
                chat_area.add_message(response, is_user=False, provider=self.current_provider)
            else:
                 chat_area.add_message("Tidak ada respons dari AI.", is_user=False, provider=self.current_provider)

        except Exception as e:
            thinking_msg.remove()
            chat_area.add_message(f"Error: {str(e)}", is_user=False, provider=self.current_provider)

    def _get_sync_response(self, user_message: str) -> str:
        # Panggil metode dari chat_handler
        return self.chat_handler._get_ai_response(user_message)

if __name__ == "__main__":
    # Inisialisasi handler dummy
    handler = DummyChatHandler()
    app = ChatApp(chat_handler=handler)
    app.run()


