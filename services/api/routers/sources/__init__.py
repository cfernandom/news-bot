"""
Sources router - Modular sources management functionality.
Main entry point that assembles all source-related routers.
"""

from fastapi import APIRouter

from .bulk_operations import router as bulk_router
from .compliance_validation import router as compliance_router
from .crud_operations import router as crud_router
from .legal_review import router as legal_router

# Create main sources router
router = APIRouter(tags=["sources"], prefix="/api/v1/sources")

# Include all sub-routers
router.include_router(crud_router, prefix="")
router.include_router(compliance_router, prefix="")
router.include_router(legal_router, prefix="")
router.include_router(bulk_router, prefix="")

# Export for backward compatibility
__all__ = ["router"]
