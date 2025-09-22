"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from core.websocket import websocket_manager
from api.cat_routes import router as cat_router

# Create FastAPI application
app = FastAPI(title="Mistral le Chat Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include routers
app.include_router(cat_router)

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("🐱 Mistral le Chat Backend started successfully!")
    print(f"🚀 Server running on http://{settings.HOST}:{settings.PORT}")

# Create the ASGI app with WebSocket support
socket_app = websocket_manager.get_asgi_app(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host=settings.HOST, port=settings.PORT)