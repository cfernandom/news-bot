"""
Export history and statistics functionality.
Handles export tracking and statistics endpoints.
"""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter

from .shared import export_history

router = APIRouter()


@router.get("/user/exports")
async def get_user_exports(user_id: str = "anonymous", limit: int = 50):
    """
    Get export history for a specific user.

    Args:
        user_id: User identifier (default: anonymous)
        limit: Maximum number of exports to return

    Returns:
        List of user's export history
    """
    user_exports = [
        export for export in export_history if export.get("user_id") == user_id
    ]

    # Sort by timestamp (newest first) and limit
    user_exports.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    return {
        "user_id": user_id,
        "total_exports": len(user_exports),
        "exports": user_exports[:limit],
    }


@router.get("/exports/stats")
async def get_export_stats() -> Dict[str, Any]:
    """
    Get comprehensive export statistics.

    Returns:
        Statistical summary of export activity
    """
    if not export_history:
        return {
            "total_exports": 0,
            "export_types": {},
            "recent_activity": [],
            "top_users": [],
            "total_file_size": 0,
            "average_file_size": 0,
            "date_range": {"first_export": None, "last_export": None},
        }

    # Calculate statistics
    total_exports = len(export_history)

    # Export types distribution
    export_types = {}
    for export in export_history:
        export_type = export.get("type", "Unknown")
        export_types[export_type] = export_types.get(export_type, 0) + 1

    # Recent activity (last 10 exports)
    recent_exports = sorted(
        export_history, key=lambda x: x.get("timestamp", ""), reverse=True
    )[:10]

    # Top users by export count
    user_counts = {}
    total_file_size = 0

    for export in export_history:
        user_id = export.get("user_id", "anonymous")
        user_counts[user_id] = user_counts.get(user_id, 0) + 1
        total_file_size += export.get("file_size", 0)

    top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Date range
    timestamps = [
        export.get("timestamp") for export in export_history if export.get("timestamp")
    ]
    date_range = {
        "first_export": min(timestamps) if timestamps else None,
        "last_export": max(timestamps) if timestamps else None,
    }

    return {
        "total_exports": total_exports,
        "export_types": export_types,
        "recent_activity": recent_exports,
        "top_users": [
            {"user_id": user, "export_count": count} for user, count in top_users
        ],
        "total_file_size": total_file_size,
        "average_file_size": (
            total_file_size / total_exports if total_exports > 0 else 0
        ),
        "date_range": date_range,
        "stats_generated_at": datetime.now().isoformat(),
    }
