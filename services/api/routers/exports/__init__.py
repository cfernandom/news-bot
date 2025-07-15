"""
Export router - Modular exports functionality.
Main entry point that assembles all export-related routers.
"""

from fastapi import APIRouter

from .chart_exports import router as chart_router
from .csv_exports import router as csv_router
from .excel_exports import router as excel_router
from .export_history import router as history_router
from .pdf_exports import router as pdf_router

# Create main exports router
router = APIRouter(tags=["exports"], prefix="/api/v1/exports")

# Include all sub-routers
router.include_router(csv_router, prefix="")
router.include_router(excel_router, prefix="")
router.include_router(chart_router, prefix="")
router.include_router(pdf_router, prefix="")
router.include_router(history_router, prefix="")

# Export for backward compatibility
__all__ = ["router"]
