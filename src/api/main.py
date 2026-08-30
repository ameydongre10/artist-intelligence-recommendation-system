"""
FastAPI Application Entry Point.
Provides REST APIs for Artist Intelligence, Hirer Intent, Recommendations, and Re-Ranking.
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.api.config import get_settings
from src.api.routes import (
    health_router,
    dataset_router,
    artists_router,
    hirers_router,
    recommendations_router
)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Production-grade Decision Intelligence and Recommendation Engine API for creative artists.\n\n"
        "Strictly implements epistemic isolation (DEMONSTRATED_EVIDENCE vs CLAIM vs ASSUMPTION vs UNKNOWN), "
        "transparent explainable scoring, evidence citations, comparative trade-offs, and follow-up re-ranking."
    ),
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Formats standard HTTP errors with structured JSON payload."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formats schema validation errors clearly."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Safely captures unhandled exceptions without leaking Python stack traces
    or sensitive server directory paths to clients.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred while processing the request.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )


# Root Endpoint
@app.get("/", tags=["Root"])
def root():
    """API Welcome and Quick Navigation."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "documentation": "/docs",
        "health_check": "/api/health",
        "dataset_summary": "/api/dataset/summary",
        "artists_endpoint": "/api/artists",
        "hirer_briefs_endpoint": "/api/hirer-briefs",
        "recommendations_endpoint": "/api/recommendations"
    }


# Include Modular API Routers
app.include_router(health_router)
app.include_router(dataset_router)
app.include_router(artists_router)
app.include_router(hirers_router)
app.include_router(recommendations_router)
