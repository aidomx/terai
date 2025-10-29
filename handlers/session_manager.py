from models.chat_models import ChatHistory

class SessionManager:
    """Manage chat sessions dan history"""
    
    def __init__(self, settings):
        self.settings = settings
        self.history = ChatHistory()
        self.use_markdown = True
    
    def get_ai_response(self, client_manager, provider: str, model: str, user_input: str) -> str:
        """Get AI response untuk chat session"""
        client = client_manager.get_client(provider)
        if not client:
            return "**Error**: Provider tidak tersedia!"
        
        # Prepare messages based on provider
        if provider == "gemini":
            messages = self.history.to_gemini_format() + [user_input]
        else:
            messages = self.history.to_openai_format() + [{"role": "user", "content": user_input}]
        
        # Get response dengan markdown
        full_response = client.stream_response(
            messages, 
            model, 
            self.use_markdown
        )
        
        if full_response:
            # Update history
            self.history.add_message("user", user_input)
            self.history.add_message("assistant", full_response)
            
            # Trim history if too long
            if len(self.history.messages) > self.settings.max_history_length:
                self.history.messages = self.history.messages[-self.settings.max_history_length:]
            
            return full_response
        
        return "**Maaf**, tidak ada response dari AI."
