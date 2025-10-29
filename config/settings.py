import os
from dotenv import load_dotenv

class Settings:
    """Application settings and configuration"""
    
    def __init__(self):
        load_dotenv()
        
        # API Keys
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Default models
        self.default_gemini_model = "gemini-2.0-flash"
        self.default_openai_model = "gpt-4o"
        
        # Chat settings
        self.max_history_length = 20  # 10 exchanges
        self.temperature = 0.7
        self.max_tokens = 2000
        
        # UI settings
        self.default_markdown = True
        self.refresh_rate = 10  # for live display

    def validate_api_keys(self):
        """Validate that at least one API key is present"""
        if not self.gemini_api_key and not self.openai_api_key:
            raise ValueError("No API keys found! Please set GEMINI_API_KEY or OPENAI_API_KEY")
        return True
