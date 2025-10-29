from rich.console import Console
from rich.panel import Panel

class CommandHandler:
    """Handle semua perintah di main menu"""
    
    def __init__(self, console: Console, chat_handler):
        self.console = console
        self.chat_handler = chat_handler
    
    def show_help(self):
        """Show help information"""
        help_text = """
[bold cyan]📖 Bantuan Terai:[/bold cyan]

[bold green]Perintah Utama:[/bold green]
  • [cyan]startchat[/cyan] - Memulai obrolan dengan AI
  • [cyan]model[/cyan] - Mengubah model AI
  • [cyan]provider[/cyan] - Mengganti provider AI
  • [cyan]config[/cyan] - Melihat konfigurasi saat ini
  • [cyan]help[/cyan] - Menampilkan bantuan ini
  • [cyan]quit[/cyan] - Keluar dari aplikasi

[bold green]Fitur Chat UI:[/bold green]
  • [cyan]TextArea[/cyan] - Input multi-line
  • [cyan]Enter[/cyan] - Baris baru
  • [cyan]Ctrl+J[/cyan] - Kirim pesan
  • [cyan]Tombol Kirim[/cyan] - Alternatif kirim pesan
  • [cyan]Markdown[/cyan] - Output rapi dengan formatting
  • [cyan]Scroll Area[/cyan] - History chat bisa di-scroll

[bold yellow]Ketik 'startchat' untuk memulai![/bold yellow]
"""
        self.console.print(Panel(help_text, title="🆘 Help", border_style="blue"))
    
    def show_config(self, current_provider: str, current_model: str, use_markdown: bool, history_length: int):
        """Show current configuration"""
        config_text = f"""
[bold cyan]⚙️ Konfigurasi Saat Ini:[/bold cyan]

  • [yellow]Provider:[/yellow] {current_provider.upper()}
  • [yellow]Model:[/yellow] {current_model}
  • [yellow]Markdown:[/yellow] {'ON' if use_markdown else 'OFF'}
  • [yellow]History:[/yellow] {history_length} pesan
  • [yellow]UI Mode:[/yellow] Textual (Modern)

[green]Gunakan 'model' atau 'provider' untuk mengubah konfigurasi[/green]
"""
        self.console.print(Panel(config_text, title="⚙️ Configuration", border_style="green"))
    
    def show_unknown_command(self):
        """Show unknown command message"""
        self.console.print("[red]Perintah tidak dikenali. Ketik 'help' untuk bantuan.[/red]")
