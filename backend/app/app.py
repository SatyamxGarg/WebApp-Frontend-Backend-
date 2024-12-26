from mongoengine import connect, get_connection
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.configs import settings
from .routers import root_api_router
from .socket import sio, socketio
from .expection_handler import CustomExceptionHandler

async def on_startup() -> None:
    """Define FastAPI startup event handler."""
    connect(
        db=settings.MONGODB_DATABASE,
        host=settings.MONGODB_HOST,
        port= settings.MONGODB_PORT,
    )    
    conn = get_connection()
    conn.server_info()  # This will raise ServerSelectionTimeoutError if MongoDB is not available
    print("MongoDB connection established successfully", conn)


async def on_shutdown() -> None:
    """Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

    """
    pass


def get_application() -> FastAPI:
    """Initialize FastAPI application.
    
    """
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        docs_url=settings.DOCS_URL,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )

    app.mount("/socket.io", socketio.ASGIApp(sio))

    app.add_middleware( CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"]
    )

    app.include_router(root_api_router)

    # Register the custom exception handlers
    app.add_exception_handler(StarletteHTTPException, CustomExceptionHandler.http_exception_handler)
    app.add_exception_handler(RequestValidationError, CustomExceptionHandler.validation_exception_handler)
    app.add_exception_handler(Exception, CustomExceptionHandler.generic_exception_handler)

    return app