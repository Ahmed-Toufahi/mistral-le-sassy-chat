"""
Cat service for managing cat state and interactions
"""
from core.models import CatState, CatResponse
from services.mistral_ai_service import MistralAIService

class CatService:
    def __init__(self):
        self.cat_state = CatState()
        self.ai_service = MistralAIService()
    
    def get_cat_state(self) -> CatState:
        """Get current cat state"""
        return self.cat_state
    
    async def chat_with_cat(self, message: str) -> CatResponse:
        """Process chat message and update cat state"""
        response = await self.ai_service.respond_to_chat(message, self.cat_state)
        
        self.cat_state.update_from_response(response)
        
        return response