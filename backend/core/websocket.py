"""
WebSocket connection management
"""
import socketio
from config.settings import settings

class WebSocketManager:
    def __init__(self):
        self.sio = socketio.AsyncServer(
            async_mode='asgi', 
            cors_allowed_origins=settings.WEBSOCKET_CORS_ORIGINS
        )
        self._setup_events()
    
    def _setup_events(self):
        """Setup WebSocket event handlers"""
        
        @self.sio.event
        async def connect(sid, environ):
            print(f"Client connected: {sid}")

        @self.sio.event
        async def disconnect(sid):
            print(f"Client disconnected: {sid}")
    
    async def broadcast(self, event: str, data: dict):
        """Broadcast data to all connected clients"""
        await self.sio.emit(event, data)
    
    def get_asgi_app(self, fastapi_app):
        """Get the ASGI app with Socket.IO mounted"""
        return socketio.ASGIApp(self.sio, fastapi_app)

websocket_manager = WebSocketManager()