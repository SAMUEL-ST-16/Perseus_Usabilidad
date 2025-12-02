"""
Perseus Backend - FastAPI Application
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import PerseusException
from app.routers import requirements
from app.services.huggingface_service import huggingface_service

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("=" * 60)
    logger.info("Starting Perseus Backend API")
    logger.info("=" * 60)

    # Preload models
    try:
        logger.info("Preloading HuggingFace models...")
        _ = huggingface_service.binary_pipeline
        logger.info("✓ Binary model loaded")
        _ = huggingface_service.multiclass_pipeline
        logger.info("✓ Multiclass model loaded")
        logger.info("All models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to preload models: {str(e)}")
        logger.warning("Models will be loaded on first request")

    logger.info(f"API listening on {settings.HOST}:{settings.PORT}")
    logger.info("=" * 60)

    yield

    # Shutdown
    logger.info("Shutting down Perseus Backend API")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# ========== CORS Middleware ==========

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== Exception Handlers ==========

@app.exception_handler(PerseusException)
async def perseus_exception_handler(request: Request, exc: PerseusException):
    """Handle custom Perseus exceptions"""
    logger.error(f"Perseus Exception: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": str(exc)
        }
    )


# ========== Routers ==========

# Include requirements router with prefix
app.include_router(
    requirements.router,
    prefix="/api/requirements",
    tags=["Requirements Extraction"]
)


# ========== Root Endpoint ==========

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint for load balancers/monitoring
    """
    return {
        "status": "healthy",
        "service": "perseus-backend",
        "version": settings.API_VERSION
    }


# ========== Run Application ==========

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )
