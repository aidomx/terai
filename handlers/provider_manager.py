from rich.console import Console

class ProviderManager:
    """Manage AI providers dan model selection"""
    
    def __init__(self, client_manager, console: Console):
        self.client_manager = client_manager
        self.console = console
        self.current_provider = list(client_manager.clients.keys())[0]
        self.current_model = self._get_default_model()
    
    def _get_default_model(self):
        """Get default model for current provider"""
        client = self.client_manager.get_client(self.current_provider)
        return list(client.available_models.values())[0]["name"]
    
    def get_available_providers(self):
        """Get available providers"""
        return self.client_manager.get_available_providers()
    
    def change_provider(self):
        """Change AI provider"""
        providers = self.get_available_providers()
        
        if len(providers) <= 1:
            self.console.print("ℹ️ [yellow]Hanya satu provider yang tersedia[/yellow]")
            return False
        
        self.console.print("\n[bold cyan]🔄 Ganti Provider AI:[/bold cyan]")
        for key, provider in providers.items():
            status = " ✅" if provider == self.current_provider else ""
            self.console.print(f"  [yellow]{key}.[/yellow] {provider.upper()}{status}")
        
        choice = input("\nPilih provider atau 'cancel': ").strip()
        
        if choice in providers:
            self.current_provider = providers[choice]
            # Reset to default model for new provider
            client = self.client_manager.get_client(self.current_provider)
            self.current_model = list(client.available_models.values())[0]["name"]
            self.console.print(f"🔄 [green]Berhasil ganti ke: {self.current_provider.upper()}[/green]")
            return True
        elif choice.lower() == 'cancel':
            self.console.print("❌ [yellow]Batal mengganti provider[/yellow]")
            return False
        else:
            self.console.print("❌ [red]Pilihan tidak valid![/red]")
            return False
    
    def change_model(self):
        """Change AI model"""
        client = self.client_manager.get_client(self.current_provider)
        if not client:
            self.console.print("❌ [red]Tidak ada provider yang aktif[/red]")
            return False
        
        models = client.available_models
        self.console.print(f"\n[bold cyan]🤖 Model {self.current_provider.upper()} yang Tersedia:[/bold cyan]")
        for key, model_info in models.items():
            status = " ✅" if model_info["name"] == self.current_model else ""
            self.console.print(f"  [yellow]{key}.[/yellow] {model_info['name']} - {model_info['description']}{status}")
        
        choice = input("\nPilih model atau 'cancel': ").strip()
        
        if choice in models:
            self.current_model = models[choice]["name"]
            self.console.print(f"🔄 [green]Berhasil ganti model ke: {self.current_model}[/green]")
            return True
        elif choice.lower() == 'cancel':
            self.console.print("❌ [yellow]Batal mengganti model[/yellow]")
            return False
        else:
            self.console.print("❌ [red]Pilihan tidak valid![/red]")
            return False
