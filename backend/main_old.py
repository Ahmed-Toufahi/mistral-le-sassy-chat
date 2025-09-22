from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from typing import Dict, Any
import asyncio
import random
from datetime import datetime
import os
from dotenv import load_dotenv

from cat_ai import CatAI
from models import CatState, ChatMessage, CatResponse

load_dotenv()

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cat_ai = CatAI("kzxQQQu80nL5OHi9l79EJEw7Twp84LNI")
cat_state = CatState()

@app.get("/")
async def root():
    return {"message": "Mistral le Chat Backend"}

@app.get("/api/cat/state")
async def get_cat_state():
    return cat_state.to_dict()

@app.post("/api/chat")
async def chat_with_cat(message: ChatMessage):
    response = await cat_ai.respond_to_chat(message.text, cat_state)
    
    cat_state.update_from_response(response)
    
    # Prepare complete response for both WebSocket and API return
    response_data = {
        'text': response.text,
        'action': response.action,
        'thought': response.thought,
        'mood': response.mood,
        'new_position': response.new_position.to_dict() if response.new_position else None,
        'state': cat_state.to_dict()
    }
    
    await sio.emit('cat_response', response_data)
    
    return response_data

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@app.on_event("startup")
async def startup_event():
    # Autonomous behavior completely removed
    pass

# Mount the Socket.IO app
socket_app = socketio.ASGIApp(sio, app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)