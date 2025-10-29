import os
from rich.console import Console
from app.chat_app import ChatApp

class UILauncher:
    """Launch dan manage Textual UI sessions"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def launch_chat_ui(self, chat_handler):
        """Launch Textual chat UI"""
        self._clear_screen()
        self.console.print("[green]Memulai Terai Chat...[/green]")
        
        try:
            # Create and run Textual app
            app = ChatApp(chat_handler)
            app.run()
            
            self.console.print("\n[yellow]Kembali ke menu utama...[/yellow]")
            return True
            
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
            self.console.print("[yellow]Fallback ke mode terminal...[/yellow]")
            return self._launch_fallback_chat(chat_handler)
    
    def _launch_fallback_chat(self, chat_handler):
        """Fallback ke terminal mode"""
        self.console.print("\n[green]Terminal Chat Mode[/green]")
        self.console.print("[yellow]Ketik 'quit' untuk kembali[/yellow]\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() == 'quit':
                    break
                    
                if not user_input:
                    continue
                
                response = chat_handler._get_ai_response(user_input)
                if response:
                    self.console.print(f"AI: {response}\n")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"Error: {e}\n")
        
        return True
    
    def _clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
