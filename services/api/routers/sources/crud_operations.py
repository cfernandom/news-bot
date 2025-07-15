"""
CRUD operations for sources.
Handles basic Create, Read, Update, Delete operations for news sources.
"""

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.models import NewsSource, ValidationStatus

from .shared import (
    SourceCreateRequest,
    SourceResponse,
    SourceUpdateRequest,
    get_db_session,
    log_compliance_action,
    validate_source_compliance,
)

router = APIRouter()


@router.post("/", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
    source_data: SourceCreateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Create a new news source with mandatory compliance validation.

    This endpoint enforces compliance-first approach by validating all legal
    requirements before allowing source creation.
    """
    # Validate compliance before creation
    compliance_result = await validate_source_compliance(source_data)

    if not compliance_result.is_compliant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Source does not meet compliance requirements",
                "violations": compliance_result.violations,
                "compliance_result": compliance_result.dict(),
            },
        )

    # Create the source
    new_source = NewsSource(
        name=source_data.name,
        base_url=str(source_data.base_url),
        language=source_data.language,
        country=source_data.country,
        extractor_class=source_data.extractor_class,
        robots_txt_url=(
            str(source_data.robots_txt_url) if source_data.robots_txt_url else None
        ),
        terms_of_service_url=(
            str(source_data.terms_of_service_url)
            if source_data.terms_of_service_url
            else None
        ),
        legal_contact_email=source_data.legal_contact_email,
        crawl_delay_seconds=source_data.crawl_delay_seconds,
        fair_use_basis=source_data.fair_use_basis,
        validation_status=ValidationStatus.COMPLIANT,
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )

    session.add(new_source)
    await session.commit()
    await session.refresh(new_source)

    # Log compliance action
    await log_compliance_action(
        session,
        new_source.id,
        "source_created",
        {
            "compliance_result": compliance_result.dict(),
            "source_name": source_data.name,
        },
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
    """
    Retrieve all news sources with optional filtering.

    Args:
        skip: Number of sources to skip
        limit: Maximum number of sources to return
        is_active: Filter by active status (None=all, True=active, False=inactive)
        language: Filter by language
        country: Filter by country
        session: Database session
    """
    query = select(NewsSource)

    if is_active is not None:
        query = query.filter(NewsSource.is_active == is_active)

    if language:
        query = query.filter(NewsSource.language == language)

    if country:
        query = query.filter(NewsSource.country == country)

    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    sources = result.scalars().all()

    return [SourceResponse.from_orm(source) for source in sources]


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: int, session: AsyncSession = Depends(get_db_session)):
    """
    Retrieve a specific news source by ID.

    Args:
        source_id: Source ID to retrieve
        session: Database session
    """
    query = select(NewsSource).filter(NewsSource.id == source_id)
    result = await session.execute(query)
    source = result.scalar_one_or_none()

    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )

    return SourceResponse.from_orm(source)


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    source_data: SourceUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Update an existing news source with compliance re-validation.

    Args:
        source_id: Source ID to update
        source_data: Updated source data
        session: Database session
    """
    # Check if source exists
    query = select(NewsSource).filter(NewsSource.id == source_id)
    result = await session.execute(query)
    existing_source = result.scalar_one_or_none()

    if not existing_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )

    # Prepare update data
    update_data = {}
    for field, value in source_data.dict(exclude_unset=True).items():
        if field in ["base_url", "robots_txt_url", "terms_of_service_url"] and value:
            update_data[field] = str(value)
        elif value is not None:
            update_data[field] = value

    if update_data:
        # Re-validate compliance if critical fields changed
        compliance_fields = [
            "base_url",
            "robots_txt_url",
            "terms_of_service_url",
            "legal_contact_email",
        ]
        if any(field in update_data for field in compliance_fields):
            # Create a validation request with merged data
            merged_data = existing_source.__dict__.copy()
            merged_data.update(update_data)

            # Convert to SourceCreateRequest for validation
            validation_request = SourceCreateRequest(
                name=merged_data.get("name"),
                base_url=merged_data.get("base_url"),
                language=merged_data.get("language", "es"),
                country=merged_data.get("country"),
                extractor_class=merged_data.get("extractor_class"),
                robots_txt_url=merged_data.get("robots_txt_url"),
                terms_of_service_url=merged_data.get("terms_of_service_url"),
                legal_contact_email=merged_data.get("legal_contact_email"),
                crawl_delay_seconds=merged_data.get("crawl_delay_seconds", 2),
                fair_use_basis=merged_data.get("fair_use_basis"),
            )

            compliance_result = await validate_source_compliance(validation_request)
            if not compliance_result.is_compliant:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Updated source does not meet compliance requirements",
                        "violations": compliance_result.violations,
                    },
                )

            update_data["validation_status"] = ValidationStatus.COMPLIANT

        update_data["updated_at"] = datetime.now(timezone.utc)

        # Update the source
        update_query = (
            update(NewsSource).where(NewsSource.id == source_id).values(**update_data)
        )
        await session.execute(update_query)
        await session.commit()

        # Log compliance action
        await log_compliance_action(
            session,
            source_id,
            "source_updated",
            {
                "updated_fields": list(update_data.keys()),
                "source_name": existing_source.name,
            },
        )

    # Return updated source
    return await get_source(source_id, session)


@router.delete("/{source_id}")
async def delete_source(
    source_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Delete a news source (soft delete by setting is_active to False).

    Args:
        source_id: Source ID to delete
        session: Database session
    """
    # Check if source exists
    query = select(NewsSource).filter(NewsSource.id == source_id)
    result = await session.execute(query)
    existing_source = result.scalar_one_or_none()

    if not existing_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )

    # Soft delete (set is_active to False)
    update_query = (
        update(NewsSource)
        .where(NewsSource.id == source_id)
        .values(is_active=False, updated_at=datetime.now(timezone.utc))
    )
    await session.execute(update_query)
    await session.commit()

    # Log compliance action
    await log_compliance_action(
        session,
        source_id,
        "source_deleted",
        {
            "source_name": existing_source.name,
            "deletion_type": "soft_delete",
        },
    )

    return {"message": f"Source {source_id} has been deactivated successfully"}
