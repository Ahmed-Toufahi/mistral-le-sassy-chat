# Backend Structure

This backend follows a clean, modular architecture with proper separation of concerns.

## Directory Structure

```
backend/
├── api/                    # API routes and endpoints
│   ├── __init__.py
│   └── cat_routes.py      # Cat-related API endpoints
├── core/                   # Core application components
│   ├── __init__.py
│   ├── models.py          # Pydantic models and data structures
│   └── websocket.py       # WebSocket connection management
├── services/               # Business logic and external services
│   ├── __init__.py
│   ├── cat_service.py     # Cat state and interaction management
│   └── mistral_ai_service.py  # Mistral AI API integration
├── config/                 # Configuration and settings
│   ├── __init__.py
│   └── settings.py        # Application settings and environment variables
├── utils/                  # Utility functions and helpers
│   ├── __init__.py
│   └── helpers.py         # Common utility functions
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── Dockerfile            # Docker configuration
```

## Key Components

### API Layer (`api/`)
- **cat_routes.py**: Contains all cat-related endpoints including chat and state management
- Clean FastAPI router structure with proper HTTP methods and response models

### Core Layer (`core/`)
- **models.py**: Pydantic models for type safety and validation
- **websocket.py**: WebSocket manager for real-time communication with frontend

### Services Layer (`services/`)
- **cat_service.py**: Manages cat state and coordinates interactions
- **mistral_ai_service.py**: Handles all Mistral AI API communication and response processing

### Configuration (`config/`)
- **settings.py**: Centralized configuration management with environment variables

### Utilities (`utils/`)
- **helpers.py**: Common utility functions used across the application

## Benefits of This Structure

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Maintainability**: Easy to locate and modify specific functionality
3. **Testability**: Each component can be tested independently
4. **Scalability**: Easy to add new features without affecting existing code
5. **Clean Imports**: Clear dependency structure and import statements

## Running the Application

```bash
cd backend
python main.py
```

The application will start on `http://0.0.0.0:8000` with WebSocket support.

## Environment Variables

- `MISTRAL_API_KEY`: Your Mistral AI API key (currently hardcoded in settings.py)

## API Endpoints

- `GET /api/`: Health check
- `GET /api/cat/state`: Get current cat state
- `POST /api/chat`: Send chat message to cat

## WebSocket Events

- `connect`: Client connection
- `disconnect`: Client disconnection  
- `cat_response`: Cat response to chat messages