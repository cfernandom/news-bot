"""
FastAPI main application for PreventIA News Analytics Dashboard.
"""

import os
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from services.api.routers import (
    analytics,
    articles,
    auth,
    automation,
    exports,
    legacy,
    nlp,
    sources,
)
from services.data.database.connection import DatabaseManager


# Application lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    db_manager = DatabaseManager()
    await db_manager.initialize()
    app.state.db_manager = db_manager

    # Initialize authentication system
    from services.api.auth.startup import initialize_auth_system

    await initialize_auth_system()

    print("✅ FastAPI application started successfully")
    print("🔌 Database connection established")
    print("🔐 Authentication system initialized")

    yield

    # Shutdown
    if hasattr(app.state, "db_manager"):
        await app.state.db_manager.close()
    print("🔴 FastAPI application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="PreventIA News Analytics API",
    description="REST API for breast cancer news analytics and sentiment analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware for React dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(articles.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(nlp.router, prefix="/api")
app.include_router(automation.router, prefix="/api")
app.include_router(sources.router)

# Include legacy API routers
app.include_router(legacy.router)
app.include_router(exports.router)
app.include_router(auth.router)


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for monitoring."""
    try:
        # Test database connection
        if not hasattr(app.state, "db_manager"):
            db_manager = DatabaseManager()
            await db_manager.initialize()
            app.state.db_manager = db_manager
        else:
            db_manager = app.state.db_manager

        is_healthy = await db_manager.health_check()

        # Get basic stats
        stats = await db_manager.execute_sql(
            "SELECT COUNT(*) as article_count FROM articles"
        )
        article_count = stats[0]["article_count"] if stats else 0

        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "database": "connected" if is_healthy else "disconnected",
            "articles_count": article_count,
            "version": "1.0.0",
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e), "version": "1.0.0"},
        )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "PreventIA News Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Run the application
if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    reload = os.getenv("API_RELOAD", "true").lower() == "true"

    uvicorn.run(
        "services.api.main:app", host=host, port=port, reload=reload, log_level="info"
    )
