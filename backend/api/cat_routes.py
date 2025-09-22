"""
Cat API endpoints for chat and state management
"""
from fastapi import APIRouter
from core.models import ChatMessage, CatState
from services.cat_service import CatService
from core.websocket import websocket_manager

router = APIRouter(prefix="/api", tags=["cat"])

cat_service = CatService()

@router.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Mistral le Chat Backend"}

@router.get("/cat/state")
async def get_cat_state():
    """Get current cat state"""
    return cat_service.get_cat_state().to_dict()

@router.post("/chat")
async def chat_with_cat(message: ChatMessage):
    """Chat with the cat and get response"""
    response = await cat_service.chat_with_cat(message.text)
    
    response_data = {
        'text': response.text,
        'action': response.action,
        'thought': response.thought,
        'mood': response.mood,
        'new_position': response.new_position.to_dict() if response.new_position else None,
        'state': cat_service.get_cat_state().to_dict()
    }
    
    await websocket_manager.broadcast('cat_response', response_data)
    
    return response_data