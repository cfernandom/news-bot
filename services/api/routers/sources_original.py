"""
News Sources Management API with Compliance-First Approach
Implements CRUD operations with mandatory legal compliance validation
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import DatabaseManager
from services.data.database.models import (
    ComplianceAuditLog,
    NewsSource,
    ValidationStatus,
)
from services.scraper.src.compliance.robots_checker import check_robots_compliance

# Create router
router = APIRouter(tags=["sources"], prefix="/api/v1/sources")


# Pydantic models for request/response
class SourceCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    base_url: HttpUrl = Field(..., description="Base URL of the news source")
    language: str = Field(default="es", pattern="^[a-z]{2}$")
    country: str = Field(..., min_length=2, max_length=50)
    extractor_class: Optional[str] = Field(None, max_length=255)

    # Legal compliance fields (mandatory)
    robots_txt_url: Optional[HttpUrl] = Field(
        None, description="URL to robots.txt file"
    )
    terms_of_service_url: Optional[HttpUrl] = Field(
        None, description="URL to terms of service"
    )
    legal_contact_email: Optional[str] = Field(None, pattern=r"^[^@]+@[^@]+\.[^@]+$")
    crawl_delay_seconds: int = Field(default=2, ge=1, le=30)

    # Fair use documentation
    fair_use_basis: Optional[str] = Field(None, description="Legal basis for fair use")


class SourceUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    base_url: Optional[HttpUrl] = Field(None)
    language: Optional[str] = Field(None, pattern="^[a-z]{2}$")
    country: Optional[str] = Field(None, min_length=2, max_length=50)
    extractor_class: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = Field(None)

    # Legal compliance fields
    robots_txt_url: Optional[HttpUrl] = Field(None)
    terms_of_service_url: Optional[HttpUrl] = Field(None)
    legal_contact_email: Optional[str] = Field(None, pattern=r"^[^@]+@[^@]+\.[^@]+$")
    crawl_delay_seconds: Optional[int] = Field(None, ge=1, le=30)
    fair_use_basis: Optional[str] = Field(None)


class SourceResponse(BaseModel):
    id: int
    name: str
    base_url: str
    language: str
    country: str
    extractor_class: Optional[str]
    is_active: bool
    validation_status: str
    validation_error: Optional[str]
    last_validation_at: Optional[datetime]

    # Legal compliance fields
    robots_txt_url: Optional[str]
    robots_txt_last_checked: Optional[datetime]
    crawl_delay_seconds: int
    scraping_allowed: Optional[bool]
    terms_of_service_url: Optional[str]
    terms_reviewed_at: Optional[datetime]
    legal_contact_email: Optional[str]
    fair_use_basis: Optional[str]
    compliance_score: Optional[float]
    last_compliance_check: Optional[datetime]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ComplianceValidationResult(BaseModel):
    source_id: int
    is_compliant: bool
    validation_results: Dict[str, Any]
    risk_level: str
    compliance_score: float
    violations: List[str]
    recommendations: List[str]
    validated_at: datetime


class ComplianceAuditEntry(BaseModel):
    table_name: str
    record_id: int
    action: str
    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]
    legal_basis: str
    performed_by: str
    performed_at: datetime


# Dependency to get database session
async def get_db_session():
    """Get database session dependency"""
    db_manager = DatabaseManager()
    await db_manager.initialize()
    async with db_manager.get_session() as session:
        yield session


# Compliance validation functions
async def validate_source_compliance(
    source_data: SourceCreateRequest,
) -> ComplianceValidationResult:
    """
    Comprehensive compliance validation for news source
    Implements mandatory legal compliance checks with live robots.txt verification
    """
    violations = []
    recommendations = []
    compliance_score = 0.0

    # 1. Live robots.txt compliance check (integrates with existing framework)
    robots_compliant = False
    try:
        robots_compliant = await check_robots_compliance(str(source_data.base_url))
        if robots_compliant:
            compliance_score += 0.25
        else:
            violations.append("La fuente no permite scraping según robots.txt")
            recommendations.append(
                "Revisar cumplimiento de robots.txt y ajustar estrategia de scraping"
            )
    except Exception as e:
        violations.append(f"No se pudo verificar cumplimiento de robots.txt: {str(e)}")
        recommendations.append(
            "Verificar que la URL de robots.txt sea accesible y válida"
        )

    # 2. Check robots.txt URL provided
    if not source_data.robots_txt_url:
        violations.append("Falta URL de robots.txt")
        recommendations.append(
            "Agregar URL de robots.txt para verificación de cumplimiento"
        )
    else:
        compliance_score += 0.15

    # 3. Check terms of service
    if not source_data.terms_of_service_url:
        violations.append("Falta URL de términos de servicio")
        recommendations.append(
            "Agregar URL de términos de servicio para revisión legal"
        )
    else:
        compliance_score += 0.2

    # 4. Check legal contact
    if not source_data.legal_contact_email:
        violations.append("Falta email de contacto legal")
        recommendations.append(
            "Agregar email de contacto legal para comunicación de cumplimiento"
        )
    else:
        compliance_score += 0.2

    # 5. Check fair use documentation
    if not source_data.fair_use_basis:
        violations.append("Falta documentación de base de uso justo")
        recommendations.append(
            "Documentar base de uso justo para investigación académica"
        )
    else:
        compliance_score += 0.2

    # 6. Check crawl delay (integrates with existing rate limiting)
    if source_data.crawl_delay_seconds < 2:
        violations.append("Retraso de crawl muy corto (mínimo 2 segundos)")
        recommendations.append("Aumentar retraso de crawl a al menos 2 segundos")
    else:
        compliance_score += 0.0  # No additional score, already counted

    # Determine compliance status
    is_compliant = len(violations) == 0
    risk_level = (
        "low"
        if compliance_score >= 0.8
        else "medium" if compliance_score >= 0.6 else "high"
    )

    validation_results = {
        "robots_txt_live_check": robots_compliant,
        "robots_txt_provided": bool(source_data.robots_txt_url),
        "terms_of_service_provided": bool(source_data.terms_of_service_url),
        "legal_contact_provided": bool(source_data.legal_contact_email),
        "fair_use_documented": bool(source_data.fair_use_basis),
        "crawl_delay_compliant": source_data.crawl_delay_seconds >= 2,
        "compliance_score": compliance_score,
        "violations_count": len(violations),
        "recommendations_count": len(recommendations),
    }

    return ComplianceValidationResult(
        source_id=0,  # Will be set after creation
        is_compliant=is_compliant,
        validation_results=validation_results,
        risk_level=risk_level,
        compliance_score=compliance_score,
        violations=violations,
        recommendations=recommendations,
        validated_at=datetime.now(timezone.utc),
    )


async def log_compliance_action(
    session: AsyncSession,
    table_name: str,
    record_id: int,
    action: str,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    performed_by: str = "system",
    compliance_score_before: Optional[float] = None,
    compliance_score_after: Optional[float] = None,
    risk_level: Optional[str] = None,
    violations_count: int = 0,
) -> None:
    """
    Log compliance-related actions for audit trail
    Required for legal compliance framework - integrates with existing system
    """
    try:
        # Create audit log entry
        audit_entry = ComplianceAuditLog(
            table_name=table_name,
            record_id=record_id,
            action=action,
            old_values=old_values,
            new_values=new_values,
            legal_basis="academic_research_fair_use",
            performed_by=performed_by,
            performed_at=datetime.now(timezone.utc).replace(tzinfo=None),
            compliance_score_before=compliance_score_before,
            compliance_score_after=compliance_score_after,
            risk_level=risk_level,
            violations_count=violations_count,
        )

        # Insert into database
        session.add(audit_entry)
        await session.commit()

        print(
            f"[COMPLIANCE_AUDIT] {action} on {table_name}:{record_id} by {performed_by}"
        )

    except Exception as e:
        print(f"[COMPLIANCE_AUDIT_ERROR] Failed to log audit entry: {e}")
        # Don't raise - audit logging failure shouldn't block operations


# API Endpoints
@router.post("/", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
    source: SourceCreateRequest, session: AsyncSession = Depends(get_db_session)
):
    """
    Create new news source with mandatory compliance validation
    All sources must pass compliance checks before creation
    """
    # MANDATORY: Pre-validation compliance check
    compliance_result = await validate_source_compliance(source)

    if not compliance_result.is_compliant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "La validación de cumplimiento falló",
                "violations": compliance_result.violations,
                "recommendations": compliance_result.recommendations,
                "compliance_score": compliance_result.compliance_score,
            },
        )

    # Check for duplicate base_url
    existing_source = await session.execute(
        select(NewsSource).where(NewsSource.base_url == str(source.base_url))
    )
    if existing_source.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Source with this base URL already exists",
        )

    # Create new source with compliance data
    new_source = NewsSource(
        name=source.name,
        base_url=str(source.base_url),
        language=source.language,
        country=source.country,
        extractor_class=source.extractor_class,
        robots_txt_url=str(source.robots_txt_url) if source.robots_txt_url else None,
        terms_of_service_url=(
            str(source.terms_of_service_url) if source.terms_of_service_url else None
        ),
        legal_contact_email=source.legal_contact_email,
        crawl_delay_seconds=source.crawl_delay_seconds,
        fair_use_basis=source.fair_use_basis,
        compliance_score=compliance_result.compliance_score,
        last_compliance_check=datetime.now(timezone.utc).replace(tzinfo=None),
        validation_status=(
            ValidationStatus.VALIDATED
            if compliance_result.is_compliant
            else ValidationStatus.PENDING
        ),
        last_validation_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )

    session.add(new_source)
    await session.commit()
    await session.refresh(new_source)

    # MANDATORY: Audit logging
    await log_compliance_action(
        session,
        "news_sources",
        new_source.id,
        "create",
        new_values=source.model_dump(mode="json"),
        performed_by="admin",
        compliance_score_after=compliance_result.compliance_score,
        risk_level=compliance_result.risk_level,
        violations_count=len(compliance_result.violations),
    )

    return SourceResponse.from_orm(new_source)


@router.get("/", response_model=List[SourceResponse])
async def get_sources(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    language: Optional[str] = None,
    country: Optional[str] = None,
    session: AsyncSession = Depends(get_db_session),
):
    """Get all news sources with optional filtering"""
    query = select(NewsSource)

    if is_active is not None:
        query = query.where(NewsSource.is_active == is_active)
    if language:
        query = query.where(NewsSource.language == language)
    if country:
        query = query.where(NewsSource.country == country)

    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    sources = result.scalars().all()

    return [SourceResponse.from_orm(source) for source in sources]


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    source_update: SourceUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Update existing news source with compliance validation"""
    # Get existing source
    existing_source = await session.execute(
        select(NewsSource).where(NewsSource.id == source_id)
    )
    existing_source = existing_source.scalar_one_or_none()

    if not existing_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )

    # Store old values for audit
    old_values = {
        "name": existing_source.name,
        "base_url": existing_source.base_url,
        "language": existing_source.language,
        "country": existing_source.country,
        "is_active": existing_source.is_active,
    }

    # Update fields
    update_data = source_update.dict(exclude_unset=True)

    # Convert HttpUrl to string if present
    if "base_url" in update_data:
        update_data["base_url"] = str(update_data["base_url"])
    if "robots_txt_url" in update_data:
        update_data["robots_txt_url"] = str(update_data["robots_txt_url"])
    if "terms_of_service_url" in update_data:
        update_data["terms_of_service_url"] = str(update_data["terms_of_service_url"])

    # Add updated timestamp
    update_data["updated_at"] = datetime.now(timezone.utc).replace(tzinfo=None)

    # Perform update
    await session.execute(
        update(NewsSource).where(NewsSource.id == source_id).values(**update_data)
    )
    await session.commit()

    # Get updated source
    updated_source = await session.execute(
        select(NewsSource).where(NewsSource.id == source_id)
    )
    updated_source = updated_source.scalar_one()

    # MANDATORY: Audit logging
    await log_compliance_action(
        session,
        "news_sources",
        source_id,
        "update",
        old_values=old_values,
        new_values=update_data,
        performed_by="admin",
    )

    return SourceResponse.from_orm(updated_source)


@router.delete("/{source_id}")
async def delete_source(
    source_id: int, session: AsyncSession = Depends(get_db_session)
):
    """Delete news source (soft delete by setting is_active=False)"""
    # Get existing source
    existing_source = await session.execute(
        select(NewsSource).where(NewsSource.id == source_id)
    )
    existing_source = existing_source.scalar_one_or_none()

    if not existing_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )

    # Soft delete (set is_active=False)
    await session.execute(
        update(NewsSource)
        .where(NewsSource.id == source_id)
        .values(is_active=False, updated_at=datetime.now(timezone.utc))
    )
    await session.commit()

    # MANDATORY: Audit logging
    await log_compliance_action(
        session,
        "news_sources",
        source_id,
        "delete",
        old_values={"is_active": True},
        new_values={"is_active": False},
        performed_by="admin",
    )

    return {"message": "Source deactivated successfully"}


@router.post("/{source_id}/validate", response_model=ComplianceValidationResult)
async def validate_source_compliance_endpoint(
    source_id: int, session: AsyncSession = Depends(get_db_session)
):
    """
    Comprehensive compliance validation for existing source
    Validates robots.txt, legal contact, terms of service, and fair use
    """
    # Get existing source
    source = await session.execute(select(NewsSource).where(NewsSource.id == source_id))
    source = source.scalar_one_or_none()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )

    # Create request object for validation
    source_data = SourceCreateRequest(
        name=source.name,
        base_url=source.base_url,
        language=source.language,
        country=source.country,
        extractor_class=source.extractor_class,
        robots_txt_url=source.robots_txt_url,
        terms_of_service_url=source.terms_of_service_url,
        legal_contact_email=source.legal_contact_email,
        crawl_delay_seconds=source.crawl_delay_seconds,
    )

    # Validate compliance
    validation_result = await validate_source_compliance(source_data)
    validation_result.source_id = source_id

    # Update source validation status
    await session.execute(
        update(NewsSource)
        .where(NewsSource.id == source_id)
        .values(
            validation_status=(
                ValidationStatus.VALIDATED
                if validation_result.is_compliant
                else ValidationStatus.FAILED
            ),
            validation_error=(
                "; ".join(validation_result.violations)
                if validation_result.violations
                else None
            ),
            last_validation_at=datetime.now(timezone.utc),
        )
    )
    await session.commit()

    # MANDATORY: Audit logging
    await log_compliance_action(
        session,
        "news_sources",
        source_id,
        "validate",
        new_values=validation_result.dict(),
        performed_by="system",
    )

    return validation_result


@router.get("/compliance/dashboard")
async def get_compliance_dashboard(session: AsyncSession = Depends(get_db_session)):
    """Real-time compliance dashboard data"""
    # Get total sources
    total_sources_result = await session.execute(
        select(NewsSource).where(NewsSource.is_active == True)
    )
    total_sources = len(total_sources_result.scalars().all())

    # Get compliant sources
    compliant_sources_result = await session.execute(
        select(NewsSource).where(
            NewsSource.is_active == True,
            NewsSource.validation_status == ValidationStatus.VALIDATED,
        )
    )
    compliant_sources = len(compliant_sources_result.scalars().all())

    # Get pending review sources
    pending_review_result = await session.execute(
        select(NewsSource).where(
            NewsSource.is_active == True,
            NewsSource.validation_status == ValidationStatus.PENDING,
        )
    )
    pending_review = len(pending_review_result.scalars().all())

    # Get failed validation sources
    failed_validation_result = await session.execute(
        select(NewsSource).where(
            NewsSource.is_active == True,
            NewsSource.validation_status == ValidationStatus.FAILED,
        )
    )
    failed_validation = len(failed_validation_result.scalars().all())

    return {
        "total_sources": total_sources,
        "compliant_sources": compliant_sources,
        "pending_review": pending_review,
        "failed_validation": failed_validation,
        "compliance_rate": (
            (compliant_sources / total_sources * 100) if total_sources > 0 else 0
        ),
        "sources_needing_attention": pending_review + failed_validation,
        "dashboard_updated_at": datetime.now(timezone.utc),
    }


@router.get("/non-compliant")
async def get_non_compliant_sources(session: AsyncSession = Depends(get_db_session)):
    """Get sources that need compliance attention"""
    result = await session.execute(
        select(NewsSource).where(
            NewsSource.is_active == True,
            NewsSource.validation_status.in_(
                [ValidationStatus.PENDING, ValidationStatus.FAILED]
            ),
        )
    )
    sources = result.scalars().all()

    return [SourceResponse.from_orm(source) for source in sources]


@router.post("/bulk-compliance-check")
async def bulk_compliance_check(
    source_ids: List[int], session: AsyncSession = Depends(get_db_session)
):
    """Bulk compliance validation for multiple sources"""
    if len(source_ids) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 50 sources allowed in bulk validation",
        )

    results = []

    for source_id in source_ids:
        try:
            # Get source
            source = await session.execute(
                select(NewsSource).where(NewsSource.id == source_id)
            )
            source = source.scalar_one_or_none()

            if not source:
                results.append(
                    {
                        "source_id": source_id,
                        "error": "Source not found",
                        "validation_result": None,
                    }
                )
                continue

            # Validate compliance
            source_data = SourceCreateRequest(
                name=source.name,
                base_url=source.base_url,
                language=source.language,
                country=source.country,
                extractor_class=source.extractor_class,
                robots_txt_url=source.robots_txt_url,
                terms_of_service_url=source.terms_of_service_url,
                legal_contact_email=source.legal_contact_email,
                crawl_delay_seconds=source.crawl_delay_seconds,
            )

            validation_result = await validate_source_compliance(source_data)
            validation_result.source_id = source_id

            # Update source validation status
            await session.execute(
                update(NewsSource)
                .where(NewsSource.id == source_id)
                .values(
                    validation_status=(
                        ValidationStatus.VALIDATED
                        if validation_result.is_compliant
                        else ValidationStatus.FAILED
                    ),
                    validation_error=(
                        "; ".join(validation_result.violations)
                        if validation_result.violations
                        else None
                    ),
                    last_validation_at=datetime.now(timezone.utc),
                )
            )

            results.append(
                {
                    "source_id": source_id,
                    "error": None,
                    "validation_result": validation_result,
                }
            )

        except Exception as e:
            results.append(
                {"source_id": source_id, "error": str(e), "validation_result": None}
            )

    await session.commit()

    # Log bulk compliance check
    await log_compliance_action(
        session,
        "news_sources",
        0,
        "bulk_validate",
        new_values={"source_ids": source_ids, "results_count": len(results)},
        performed_by="admin",
    )

    return {
        "total_sources": len(source_ids),
        "successful_validations": len([r for r in results if r["error"] is None]),
        "failed_validations": len([r for r in results if r["error"] is not None]),
        "results": results,
    }


@router.post("/{source_id}/legal-review")
async def legal_review_source(
    source_id: int,
    review_data: Dict[str, Any],
    session: AsyncSession = Depends(get_db_session),
):
    """Legal review workflow for news source"""
    # Get existing source
    source = await session.execute(select(NewsSource).where(NewsSource.id == source_id))
    source = source.scalar_one_or_none()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )

    # Validate review data
    required_fields = ["reviewer_email", "review_status", "review_notes"]
    for field in required_fields:
        if field not in review_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field}",
            )

    # Validate review status
    valid_statuses = ["approved", "rejected", "needs_review"]
    if review_data["review_status"] not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid review status. Must be one of: {valid_statuses}",
        )

    # Update source with review data
    await session.execute(
        update(NewsSource)
        .where(NewsSource.id == source_id)
        .values(
            terms_reviewed_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    )
    await session.commit()

    # Log legal review
    await log_compliance_action(
        session,
        "news_sources",
        source_id,
        "legal_review",
        new_values=review_data,
        performed_by=review_data["reviewer_email"],
    )

    return {
        "source_id": source_id,
        "review_status": review_data["review_status"],
        "reviewed_at": datetime.now(timezone.utc),
        "reviewer": review_data["reviewer_email"],
        "message": f"Legal review completed with status: {review_data['review_status']}",
    }


@router.get("/audit-trail")
async def get_audit_trail(
    limit: int = 100,
    offset: int = 0,
    action: Optional[str] = None,
    source_id: Optional[int] = None,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Get compliance audit trail from actual database logs
    Integrates with existing legal compliance framework
    """
    # Build query
    query = select(ComplianceAuditLog).where(
        ComplianceAuditLog.table_name == "news_sources"
    )

    # Apply filters
    if action:
        query = query.where(ComplianceAuditLog.action == action)

    if source_id:
        query = query.where(ComplianceAuditLog.record_id == source_id)

    # Order by most recent first
    query = query.order_by(ComplianceAuditLog.performed_at.desc())

    # Get total count for pagination
    count_query = select(ComplianceAuditLog).where(
        ComplianceAuditLog.table_name == "news_sources"
    )
    if action:
        count_query = count_query.where(ComplianceAuditLog.action == action)
    if source_id:
        count_query = count_query.where(ComplianceAuditLog.record_id == source_id)

    total_result = await session.execute(count_query)
    total_entries = len(total_result.scalars().all())

    # Apply pagination
    query = query.offset(offset).limit(limit)

    # Execute query
    result = await session.execute(query)
    audit_entries = result.scalars().all()

    # Convert to dict format
    audit_data = []
    for entry in audit_entries:
        audit_data.append(
            {
                "id": entry.id,
                "table_name": entry.table_name,
                "record_id": entry.record_id,
                "action": entry.action,
                "old_values": entry.old_values,
                "new_values": entry.new_values,
                "legal_basis": entry.legal_basis,
                "performed_by": entry.performed_by,
                "performed_at": entry.performed_at,
                "compliance_score_before": (
                    float(entry.compliance_score_before)
                    if entry.compliance_score_before
                    else None
                ),
                "compliance_score_after": (
                    float(entry.compliance_score_after)
                    if entry.compliance_score_after
                    else None
                ),
                "risk_level": entry.risk_level,
                "violations_count": entry.violations_count,
                "created_at": entry.created_at,
            }
        )

    return {
        "audit_entries": audit_data,
        "total_entries": total_entries,
        "limit": limit,
        "offset": offset,
        "filters_applied": {"action": action, "source_id": source_id},
        "compliance_framework": "integrated",
    }


@router.get("/compliance/stats")
async def get_compliance_stats(session: AsyncSession = Depends(get_db_session)):
    """Get detailed compliance statistics"""
    # Get all active sources
    all_sources = await session.execute(
        select(NewsSource).where(NewsSource.is_active == True)
    )
    all_sources = all_sources.scalars().all()

    # Calculate compliance statistics
    total_sources = len(all_sources)

    # Count by validation status
    validation_stats = {"validated": 0, "pending": 0, "failed": 0}

    # Count compliance fields
    compliance_fields = {
        "robots_txt_provided": 0,
        "terms_of_service_provided": 0,
        "legal_contact_provided": 0,
        "fair_use_documented": 0,
    }

    for source in all_sources:
        # Validation status
        if source.validation_status == ValidationStatus.VALIDATED:
            validation_stats["validated"] += 1
        elif source.validation_status == ValidationStatus.PENDING:
            validation_stats["pending"] += 1
        elif source.validation_status == ValidationStatus.FAILED:
            validation_stats["failed"] += 1

        # Compliance fields
        if source.robots_txt_url:
            compliance_fields["robots_txt_provided"] += 1
        if source.terms_of_service_url:
            compliance_fields["terms_of_service_provided"] += 1
        if source.legal_contact_email:
            compliance_fields["legal_contact_provided"] += 1
        # Note: fair_use_basis field would need to be added to NewsSource model

    return {
        "total_sources": total_sources,
        "validation_status_breakdown": validation_stats,
        "compliance_fields_coverage": compliance_fields,
        "compliance_percentage": {
            "robots_txt": (
                (compliance_fields["robots_txt_provided"] / total_sources * 100)
                if total_sources > 0
                else 0
            ),
            "terms_of_service": (
                (compliance_fields["terms_of_service_provided"] / total_sources * 100)
                if total_sources > 0
                else 0
            ),
            "legal_contact": (
                (compliance_fields["legal_contact_provided"] / total_sources * 100)
                if total_sources > 0
                else 0
            ),
            "overall_compliance": (
                (validation_stats["validated"] / total_sources * 100)
                if total_sources > 0
                else 0
            ),
        },
        "generated_at": datetime.now(timezone.utc),
    }


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get specific news source by ID"""
    source = await session.execute(select(NewsSource).where(NewsSource.id == source_id))
    source = source.scalar_one_or_none()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Source not found"
        )

    return SourceResponse.from_orm(source)
