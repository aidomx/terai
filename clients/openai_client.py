# clients/openai_client.py
from openai import OpenAI as OpenAIClient
from rich.console import Console
from .base_client import BaseAIClient

class OpenAIClientWrapper(BaseAIClient):
    """OpenAI client implementation"""
    
    def __init__(self, api_key: str, console: Console):
        super().__init__(console)
        self.client = OpenAIClient(api_key=api_key)
        self.available_models = self.get_available_models()
    
    def get_available_models(self) -> dict:
        return {
            "1": {"name": "gpt-4o", "description": "Latest GPT-4 model"},
            "2": {"name": "gpt-4o-mini", "description": "Fast & cost-effective"},
            "3": {"name": "gpt-4-turbo", "description": "Previous generation"},
            "4": {"name": "gpt-3.5-turbo", "description": "Legacy model"}
        }
    
    def validate_connection(self) -> bool:
        try:
            test_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception:
            return False
    
    def stream_response(self, messages, model: str, use_markdown: bool = True):
        """Stream response from OpenAI"""
        from handlers.stream_handler import StreamHandler  # Import di dalam method
        
        stream_handler = StreamHandler(self.console)
        
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                stream=True
            )
            
            return stream_handler.handle_openai_stream(stream, use_markdown)
            
        except Exception as e:
            self.console.print(f"❌ [red]OpenAI Error: {e}[/red]")
            return None
