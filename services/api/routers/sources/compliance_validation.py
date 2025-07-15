"""
Compliance validation functionality for sources.
Handles compliance checking, dashboard, and statistics.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.models import (
    ComplianceAuditLog,
    NewsSource,
    ValidationStatus,
)

from .shared import (
    ComplianceValidationResult,
    SourceCreateRequest,
    get_db_session,
    log_compliance_action,
    validate_source_compliance,
)

router = APIRouter()


@router.post("/{source_id}/validate", response_model=ComplianceValidationResult)
async def validate_source_compliance_endpoint(
    source_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Validate compliance for a specific source.

    Args:
        source_id: Source ID to validate
        session: Database session
    """
    # Get source
    query = select(NewsSource).filter(NewsSource.id == source_id)
    result = await session.execute(query)
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )

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

    # Update source validation status
    new_status = (
        ValidationStatus.COMPLIANT
        if compliance_result.is_compliant
        else ValidationStatus.NON_COMPLIANT
    )

    if source.validation_status != new_status:
        source.validation_status = new_status
        source.updated_at = datetime.now(timezone.utc)
        await session.commit()

        # Log compliance action
        await log_compliance_action(
            session,
            source_id,
            "compliance_validated",
            {
                "compliance_result": compliance_result.dict(),
                "previous_status": source.validation_status.value,
                "new_status": new_status.value,
            },
        )

    return compliance_result


@router.get("/compliance/dashboard")
async def get_compliance_dashboard(session: AsyncSession = Depends(get_db_session)):
    """
    Get compliance dashboard with comprehensive statistics.

    Returns:
        Dashboard data with compliance metrics and insights
    """
    # Total sources
    total_sources_query = select(func.count(NewsSource.id))
    total_sources_result = await session.execute(total_sources_query)
    total_sources = total_sources_result.scalar()

    # Active sources
    active_sources_query = select(func.count(NewsSource.id)).filter(
        NewsSource.is_active == True
    )
    active_sources_result = await session.execute(active_sources_query)
    active_sources = active_sources_result.scalar()

    # Compliance status distribution
    compliance_stats_query = select(
        NewsSource.validation_status, func.count(NewsSource.id).label("count")
    ).group_by(NewsSource.validation_status)
    compliance_stats_result = await session.execute(compliance_stats_query)
    compliance_stats = {
        row.validation_status: row.count for row in compliance_stats_result
    }

    # Recent compliance actions
    recent_actions_query = (
        select(ComplianceAuditLog)
        .order_by(ComplianceAuditLog.timestamp.desc())
        .limit(10)
    )
    recent_actions_result = await session.execute(recent_actions_query)
    recent_actions = recent_actions_result.scalars().all()

    # Country distribution
    country_stats_query = select(
        NewsSource.country, func.count(NewsSource.id).label("count")
    ).group_by(NewsSource.country)
    country_stats_result = await session.execute(country_stats_query)
    country_stats = {row.country: row.count for row in country_stats_result}

    # Language distribution
    language_stats_query = select(
        NewsSource.language, func.count(NewsSource.id).label("count")
    ).group_by(NewsSource.language)
    language_stats_result = await session.execute(language_stats_query)
    language_stats = {row.language: row.count for row in language_stats_result}

    return {
        "overview": {
            "total_sources": total_sources,
            "active_sources": active_sources,
            "inactive_sources": total_sources - active_sources,
            "compliance_rate": (
                compliance_stats.get(ValidationStatus.COMPLIANT, 0)
                / total_sources
                * 100
                if total_sources > 0
                else 0
            ),
        },
        "compliance_distribution": {
            "compliant": compliance_stats.get(ValidationStatus.COMPLIANT, 0),
            "non_compliant": compliance_stats.get(ValidationStatus.NON_COMPLIANT, 0),
            "pending": compliance_stats.get(ValidationStatus.PENDING, 0),
        },
        "geographic_distribution": {
            "by_country": country_stats,
            "by_language": language_stats,
        },
        "recent_activity": [
            {
                "id": action.id,
                "source_id": action.source_id,
                "action": action.action,
                "timestamp": action.timestamp,
                "reviewer_id": action.reviewer_id,
                "details": action.details,
            }
            for action in recent_actions
        ],
        "generated_at": datetime.now(timezone.utc),
    }


@router.get("/compliance/stats")
async def get_compliance_stats(session: AsyncSession = Depends(get_db_session)):
    """
    Get detailed compliance statistics.

    Returns:
        Comprehensive compliance statistics and trends
    """
    # Basic compliance stats
    total_query = select(func.count(NewsSource.id))
    total_result = await session.execute(total_query)
    total_sources = total_result.scalar()

    compliant_query = select(func.count(NewsSource.id)).filter(
        NewsSource.validation_status == ValidationStatus.COMPLIANT
    )
    compliant_result = await session.execute(compliant_query)
    compliant_sources = compliant_result.scalar()

    # Compliance issues breakdown
    non_compliant_query = select(NewsSource).filter(
        NewsSource.validation_status == ValidationStatus.NON_COMPLIANT
    )
    non_compliant_result = await session.execute(non_compliant_query)
    non_compliant_sources = non_compliant_result.scalars().all()

    # Analyze common compliance issues
    compliance_issues = {
        "missing_robots_txt": 0,
        "missing_legal_contact": 0,
        "missing_terms_of_service": 0,
        "missing_fair_use_basis": 0,
        "insufficient_crawl_delay": 0,
    }

    for source in non_compliant_sources:
        if not source.robots_txt_url:
            compliance_issues["missing_robots_txt"] += 1
        if not source.legal_contact_email:
            compliance_issues["missing_legal_contact"] += 1
        if not source.terms_of_service_url:
            compliance_issues["missing_terms_of_service"] += 1
        if not source.fair_use_basis:
            compliance_issues["missing_fair_use_basis"] += 1
        if source.crawl_delay_seconds < 2:
            compliance_issues["insufficient_crawl_delay"] += 1

    # Recent compliance trends
    recent_audit_query = select(ComplianceAuditLog).filter(
        ComplianceAuditLog.timestamp
        >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    )
    recent_audit_result = await session.execute(recent_audit_query)
    recent_audits = recent_audit_result.scalars().all()

    action_counts = {}
    for audit in recent_audits:
        action_counts[audit.action] = action_counts.get(audit.action, 0) + 1

    return {
        "summary": {
            "total_sources": total_sources,
            "compliant_sources": compliant_sources,
            "non_compliant_sources": total_sources - compliant_sources,
            "compliance_rate": (
                (compliant_sources / total_sources * 100) if total_sources > 0 else 0
            ),
        },
        "compliance_issues": compliance_issues,
        "recent_activity": {
            "today_actions": action_counts,
            "total_today": len(recent_audits),
        },
        "recommendations": [
            f"Focus on {max(compliance_issues, key=compliance_issues.get)} (affects {max(compliance_issues.values())} sources)",
            "Implement automated compliance monitoring",
            "Regular compliance audits recommended",
        ],
        "generated_at": datetime.now(timezone.utc),
    }


@router.get("/non-compliant")
async def get_non_compliant_sources(session: AsyncSession = Depends(get_db_session)):
    """
    Get all non-compliant sources with detailed violation information.

    Returns:
        List of non-compliant sources with violation details
    """
    query = select(NewsSource).filter(
        NewsSource.validation_status == ValidationStatus.NON_COMPLIANT
    )
    result = await session.execute(query)
    non_compliant_sources = result.scalars().all()

    sources_with_violations = []
    for source in non_compliant_sources:
        violations = []

        # Check specific violations
        if not source.robots_txt_url:
            violations.append("Missing robots.txt URL")
        if not source.legal_contact_email:
            violations.append("Missing legal contact email")
        if not source.terms_of_service_url:
            violations.append("Missing terms of service URL")
        if not source.fair_use_basis:
            violations.append("Missing fair use basis documentation")
        if source.crawl_delay_seconds < 2:
            violations.append("Insufficient crawl delay (minimum 2 seconds required)")

        sources_with_violations.append(
            {
                "id": source.id,
                "name": source.name,
                "base_url": source.base_url,
                "country": source.country,
                "language": source.language,
                "validation_status": source.validation_status,
                "violations": violations,
                "created_at": source.created_at,
                "updated_at": source.updated_at,
            }
        )

    return {
        "total_non_compliant": len(sources_with_violations),
        "sources": sources_with_violations,
        "generated_at": datetime.now(timezone.utc),
    }
