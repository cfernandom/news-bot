"""
Legal review functionality for sources.
Handles legal review processes and audit trails.
"""

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.models import (
    ComplianceAuditLog,
    NewsSource,
    ValidationStatus,
)

from .shared import (
    LegalReviewRequest,
    get_db_session,
    log_compliance_action,
)

router = APIRouter()


@router.post("/{source_id}/legal-review")
async def legal_review_source(
    source_id: int,
    review_data: LegalReviewRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Submit legal review for a source.

    Args:
        source_id: Source ID to review
        review_data: Legal review data
        session: Database session
    """
    # Check if source exists
    query = select(NewsSource).filter(NewsSource.id == source_id)
    result = await session.execute(query)
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )

    # Update source based on legal review
    new_status = (
        ValidationStatus.COMPLIANT
        if review_data.legal_approval
        else ValidationStatus.NON_COMPLIANT
    )

    update_query = (
        update(NewsSource)
        .where(NewsSource.id == source_id)
        .values(
            validation_status=new_status,
            updated_at=datetime.now(timezone.utc),
        )
    )
    await session.execute(update_query)
    await session.commit()

    # Log legal review action
    await log_compliance_action(
        session,
        source_id,
        "legal_review_completed",
        {
            "reviewer_id": review_data.reviewer_id,
            "legal_approval": review_data.legal_approval,
            "review_notes": review_data.review_notes,
            "compliance_recommendations": review_data.compliance_recommendations,
            "previous_status": source.validation_status.value,
            "new_status": new_status.value,
        },
        reviewer_id=review_data.reviewer_id,
    )

    return {
        "message": f"Legal review completed for source {source_id}",
        "source_id": source_id,
        "legal_approval": review_data.legal_approval,
        "new_status": new_status.value,
        "reviewer_id": review_data.reviewer_id,
        "review_date": datetime.now(timezone.utc),
    }


@router.get("/audit-trail")
async def get_audit_trail(
    source_id: int = None,
    action: str = None,
    reviewer_id: str = None,
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get compliance audit trail with optional filtering.

    Args:
        source_id: Filter by source ID
        action: Filter by action type
        reviewer_id: Filter by reviewer ID
        limit: Maximum number of records
        offset: Number of records to skip
        session: Database session
    """
    query = select(ComplianceAuditLog)

    # Apply filters
    if source_id:
        query = query.filter(ComplianceAuditLog.source_id == source_id)
    if action:
        query = query.filter(ComplianceAuditLog.action == action)
    if reviewer_id:
        query = query.filter(ComplianceAuditLog.reviewer_id == reviewer_id)

    # Order by timestamp (newest first) and paginate
    query = (
        query.order_by(ComplianceAuditLog.timestamp.desc()).offset(offset).limit(limit)
    )

    result = await session.execute(query)
    audit_logs = result.scalars().all()

    # Get source names for better readability
    source_ids = list(set(log.source_id for log in audit_logs))
    if source_ids:
        sources_query = select(NewsSource.id, NewsSource.name).filter(
            NewsSource.id.in_(source_ids)
        )
        sources_result = await session.execute(sources_query)
        sources_dict = {row.id: row.name for row in sources_result}
    else:
        sources_dict = {}

    audit_trail = []
    for log in audit_logs:
        audit_trail.append(
            {
                "id": log.id,
                "source_id": log.source_id,
                "source_name": sources_dict.get(log.source_id, "Unknown"),
                "action": log.action,
                "details": log.details,
                "reviewer_id": log.reviewer_id,
                "timestamp": log.timestamp,
            }
        )

    return {
        "total_records": len(audit_trail),
        "audit_trail": audit_trail,
        "filters_applied": {
            "source_id": source_id,
            "action": action,
            "reviewer_id": reviewer_id,
        },
        "pagination": {
            "limit": limit,
            "offset": offset,
        },
        "generated_at": datetime.now(timezone.utc),
    }
