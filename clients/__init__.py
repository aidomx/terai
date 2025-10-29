# clients/__init__.py
from .base_client import BaseAIClient
from .gemini_client import GeminiClient
from .openai_client import OpenAIClientWrapper

class ClientManager:
    """Manager for all AI clients"""
    
    def __init__(self, settings, console):
        self.settings = settings
        self.console = console
        self.clients = {}
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize available clients"""
        if self.settings.gemini_api_key:
            try:
                self.clients["gemini"] = GeminiClient(
                    self.settings.gemini_api_key, 
                    self.console
                )
                self.console.print("✅ Gemini client initialized")
            except Exception as e:
                self.console.print(f"❌ Gemini setup failed: {e}")
        
        if self.settings.openai_api_key:
            try:
                self.clients["openai"] = OpenAIClientWrapper(
                    self.settings.openai_api_key,
                    self.console
                )
                self.console.print("✅ OpenAI client initialized")
            except Exception as e:
                self.console.print(f"❌ OpenAI setup failed: {e}")
        
        if not self.clients:
            raise ValueError("No AI providers configured!")
    
    def get_available_providers(self):
        """Get available providers"""
        return {str(i+1): name for i, name in enumerate(self.clients.keys())}
    
    def get_client(self, provider: str):
        """Get client by provider name"""
        return self.clients.get(provider)

__all__ = [
    'BaseAIClient',
    'GeminiClient', 
    'OpenAIClientWrapper',
    'ClientManager'
]
