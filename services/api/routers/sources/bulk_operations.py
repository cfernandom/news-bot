"""
Bulk operations functionality for sources.
Handles bulk compliance checks and batch operations.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.models import NewsSource, ValidationStatus

from .shared import (
    SourceCreateRequest,
    get_db_session,
    log_compliance_action,
    validate_source_compliance,
)

router = APIRouter()


@router.post("/bulk-compliance-check")
async def bulk_compliance_check(
    source_ids: List[int] = None,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Perform bulk compliance check on multiple sources.

    Args:
        source_ids: List of source IDs to check (if None, check all sources)
        session: Database session
    """
    # Get sources to check
    query = select(NewsSource).filter(NewsSource.is_active == True)
    if source_ids:
        query = query.filter(NewsSource.id.in_(source_ids))

    result = await session.execute(query)
    sources = result.scalars().all()

    if not sources:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sources found to check",
        )

    compliance_results = []
    updated_sources = []

    for source in sources:
        try:
            # Create validation request
            validation_request = SourceCreateRequest(
                name=source.name,
                base_url=source.base_url,
                language=source.language,
                country=source.country,
                extractor_class=source.extractor_class,
                robots_txt_url=source.robots_txt_url,
                terms_of_service_url=source.terms_of_service_url,
                legal_contact_email=source.legal_contact_email,
                crawl_delay_seconds=source.crawl_delay_seconds,
                fair_use_basis=source.fair_use_basis,
            )

            # Validate compliance
            compliance_result = await validate_source_compliance(validation_request)

            # Update source status if changed
            new_status = (
                ValidationStatus.COMPLIANT
                if compliance_result.is_compliant
                else ValidationStatus.NON_COMPLIANT
            )

            if source.validation_status != new_status:
                source.validation_status = new_status
                source.updated_at = datetime.now(timezone.utc)
                updated_sources.append(source.id)

                # Log compliance action
                await log_compliance_action(
                    session,
                    source.id,
                    "bulk_compliance_check",
                    {
                        "compliance_result": compliance_result.dict(),
                        "previous_status": source.validation_status.value,
                        "new_status": new_status.value,
                        "batch_operation": True,
                    },
                )

            compliance_results.append(
                {
                    "source_id": source.id,
                    "source_name": source.name,
                    "is_compliant": compliance_result.is_compliant,
                    "violations": compliance_result.violations,
                    "previous_status": source.validation_status.value,
                    "new_status": new_status.value,
                    "status_changed": source.validation_status != new_status,
                }
            )

        except Exception as e:
            compliance_results.append(
                {
                    "source_id": source.id,
                    "source_name": source.name,
                    "is_compliant": False,
                    "violations": [f"Compliance check failed: {str(e)}"],
                    "previous_status": source.validation_status.value,
                    "new_status": ValidationStatus.NON_COMPLIANT.value,
                    "status_changed": False,
                    "error": str(e),
                }
            )

    # Commit all changes
    await session.commit()

    # Generate summary statistics
    total_checked = len(compliance_results)
    compliant_count = sum(1 for result in compliance_results if result["is_compliant"])
    status_changed_count = sum(
        1 for result in compliance_results if result["status_changed"]
    )

    return {
        "summary": {
            "total_sources_checked": total_checked,
            "compliant_sources": compliant_count,
            "non_compliant_sources": total_checked - compliant_count,
            "compliance_rate": (
                (compliant_count / total_checked * 100) if total_checked > 0 else 0
            ),
            "status_changes": status_changed_count,
            "updated_sources": updated_sources,
        },
        "detailed_results": compliance_results,
        "check_completed_at": datetime.now(timezone.utc),
    }


@router.post("/bulk-activate")
async def bulk_activate_sources(
    source_ids: List[int],
    session: AsyncSession = Depends(get_db_session),
):
    """
    Bulk activate multiple sources.

    Args:
        source_ids: List of source IDs to activate
        session: Database session
    """
    if not source_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No source IDs provided",
        )

    # Update sources
    update_query = (
        update(NewsSource)
        .where(NewsSource.id.in_(source_ids))
        .values(is_active=True, updated_at=datetime.now(timezone.utc))
    )

    result = await session.execute(update_query)
    updated_count = result.rowcount
    await session.commit()

    # Log bulk action
    for source_id in source_ids:
        await log_compliance_action(
            session,
            source_id,
            "bulk_activated",
            {
                "batch_operation": True,
                "total_sources_in_batch": len(source_ids),
            },
        )

    return {
        "message": f"Successfully activated {updated_count} sources",
        "activated_source_ids": source_ids,
        "total_activated": updated_count,
        "operation_completed_at": datetime.now(timezone.utc),
    }


@router.post("/bulk-deactivate")
async def bulk_deactivate_sources(
    source_ids: List[int],
    session: AsyncSession = Depends(get_db_session),
):
    """
    Bulk deactivate multiple sources.

    Args:
        source_ids: List of source IDs to deactivate
        session: Database session
    """
    if not source_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No source IDs provided",
        )

    # Update sources
    update_query = (
        update(NewsSource)
        .where(NewsSource.id.in_(source_ids))
        .values(is_active=False, updated_at=datetime.now(timezone.utc))
    )

    result = await session.execute(update_query)
    updated_count = result.rowcount
    await session.commit()

    # Log bulk action
    for source_id in source_ids:
        await log_compliance_action(
            session,
            source_id,
            "bulk_deactivated",
            {
                "batch_operation": True,
                "total_sources_in_batch": len(source_ids),
            },
        )

    return {
        "message": f"Successfully deactivated {updated_count} sources",
        "deactivated_source_ids": source_ids,
        "total_deactivated": updated_count,
        "operation_completed_at": datetime.now(timezone.utc),
    }
