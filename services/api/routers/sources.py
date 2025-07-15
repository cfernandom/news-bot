"""
Sources functionality - Refactored modular version with backward compatibility.
This module maintains the original API while using the new modular structure.
"""

# Import the main router from the modular structure
from .sources import router

# Export for backward compatibility
__all__ = ["router"]
