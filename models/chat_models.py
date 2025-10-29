from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str

@dataclass
class ChatHistory:
    messages: List[Message]
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, role: str, content: str):
        """Add a message to history"""
        self.messages.append(Message(role=role, content=content))
    
    def get_recent_messages(self, max_exchanges: int = 10) -> List[Message]:
        """Get recent messages (last n exchanges)"""
        return self.messages[-(max_exchanges * 2):]
    
    def clear(self):
        """Clear chat history"""
        self.messages.clear()
    
    def to_gemini_format(self) -> List[str]:
        """Convert to Gemini format"""
        return [msg.content for msg in self.messages]
    
    def to_openai_format(self) -> List[Dict[str, str]]:
        """Convert to OpenAI format"""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    @property
    def length(self) -> int:
        return len(self.messages)
