from abc import ABC, abstractmethod
from rich.console import Console

class BaseAIClient(ABC):
    """Abstract base class for AI clients"""

    def __init__(self, console: Console):
        self.console = console
        self.available_models = {}

    @abstractmethod
    def stream_response(self, messages, model: str, use_markdown: bool = True):
        """Stream response from AI provider"""
        pass

    @abstractmethod
    def get_available_models(self) -> dict:
        """Get available models for this provider"""
        pass

    @abstractmethod
    def validate_connection(self) -> bool:
        """Validate connection to AI service"""
        pass
