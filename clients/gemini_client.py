# clients/gemini_client.py
from google import genai as google_genai
from google.genai import types as google_types
from rich.console import Console
from .base_client import BaseAIClient

class GeminiClient(BaseAIClient):
    """Google Gemini client implementation"""
    
    def __init__(self, api_key: str, console: Console):
        super().__init__(console)
        self.client = google_genai.Client(api_key=api_key)
        self.available_models = self.get_available_models()
        
    def get_available_models(self) -> dict:
        return {
            "1": {"name": "gemini-2.0-flash", "description": "Fast & efficient"},
            "2": {"name": "gemini-1.5-flash", "description": "Balanced performance"},
            "3": {"name": "gemini-1.5-pro", "description": "Most capable"},
            "4": {"name": "gemini-2.0-flash-exp", "description": "Experimental"}
        }
    
    def validate_connection(self) -> bool:
        try:
            test_response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents="Hello"
            )
            return True
        except Exception:
            return False
    
    def stream_response(self, messages, model: str, use_markdown: bool = True):
        """Stream response from Gemini"""
        from handlers.stream_handler import StreamHandler  # Import di dalam method
        
        stream_handler = StreamHandler(self.console)
        
        try:
            chunks = self.client.models.generate_content_stream(
                model=model,
                contents=messages,
                config=google_types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=2000,
                )
            )
            
            return stream_handler.handle_gemini_stream(chunks, use_markdown)
            
        except Exception as e:
            self.console.print(f"❌ [red]Gemini Error: {e}[/red]")
            return None
