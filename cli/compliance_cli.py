"""
Compliance management CLI tools for PreventIA News Analytics
Command-line interface for legal compliance monitoring and validation
"""

from datetime import datetime, timedelta
from typing import List, Optional

import click
from sqlalchemy import func, select

from services.data.database.models import ComplianceAuditLog, LegalNotice, NewsSource

from .base import BaseCLI, async_command, common_options


class ComplianceCLI(BaseCLI):
    """CLI for compliance management and monitoring"""

    def __init__(self):
        super().__init__()

    async def get_compliance_dashboard(self) -> dict:
        """Get compliance dashboard overview"""
        async with self.db_manager.get_session() as session:
            # Total sources
            total_query = select(func.count(NewsSource.id)).where(
                NewsSource.status != "deleted"
            )
            total_result = await session.execute(total_query)
            total_sources = total_result.scalar() or 0

            # Compliant sources
            compliant_query = select(func.count(NewsSource.id)).where(
                NewsSource.robots_txt_compliant == True,
                NewsSource.legal_contact_verified == True,
                NewsSource.terms_acceptable == True,
                NewsSource.fair_use_documented == True,
                NewsSource.data_minimization_applied == True,
                NewsSource.status != "deleted",
            )
            compliant_result = await session.execute(compliant_query)
            compliant_sources = compliant_result.scalar() or 0

            # Pending review
            pending_query = select(func.count(NewsSource.id)).where(
                NewsSource.legal_review_status == "pending",
                NewsSource.status != "deleted",
            )
            pending_result = await session.execute(pending_query)
            pending_review = pending_result.scalar() or 0

            # High risk sources
            high_risk_query = select(func.count(NewsSource.id)).where(
                NewsSource.risk_level.in_(["high", "critical"]),
                NewsSource.status != "deleted",
            )
            high_risk_result = await session.execute(high_risk_query)
            high_risk_sources = high_risk_result.scalar() or 0

            # Recent violations (last 30 days)
            violations_query = select(func.count(ComplianceAuditLog.id)).where(
                ComplianceAuditLog.action == "validate",
                ComplianceAuditLog.performed_at >= datetime.now() - timedelta(days=30),
                ComplianceAuditLog.risk_assessment.in_(["high", "critical"]),
            )
            violations_result = await session.execute(violations_query)
            recent_violations = violations_result.scalar() or 0

            # Compliance rate
            compliance_rate = (
                (compliant_sources / total_sources) if total_sources > 0 else 0.0
            )

            return {
                "total_sources": total_sources,
                "compliant_sources": compliant_sources,
                "non_compliant_sources": total_sources - compliant_sources,
                "compliance_rate": compliance_rate,
                "pending_review": pending_review,
                "high_risk_sources": high_risk_sources,
                "recent_violations": recent_violations,
                "last_updated": datetime.now().isoformat(),
            }

    async def get_non_compliant_sources(self) -> List[dict]:
        """Get list of non-compliant sources"""
        async with self.db_manager.get_session() as session:
            query = select(NewsSource).where(
                ~(
                    (NewsSource.robots_txt_compliant == True)
                    & (NewsSource.legal_contact_verified == True)
                    & (NewsSource.terms_acceptable == True)
                    & (NewsSource.fair_use_documented == True)
                    & (NewsSource.data_minimization_applied == True)
                ),
                NewsSource.status != "deleted",
            )

            result = await session.execute(query)
            sources = result.scalars().all()

            non_compliant_data = []
            for source in sources:
                violations = []
                if not source.robots_txt_compliant:
                    violations.append("robots.txt non-compliant")
                if not source.legal_contact_verified:
                    violations.append("legal contact not verified")
                if not source.terms_acceptable:
                    violations.append("terms of service not acceptable")
                if not source.fair_use_documented:
                    violations.append("fair use not documented")
                if not source.data_minimization_applied:
                    violations.append("data minimization not applied")

                non_compliant_data.append(
                    {
                        "id": source.id,
                        "name": source.name,
                        "base_url": source.base_url,
                        "risk_level": source.risk_level or "unknown",
                        "violations": violations,
                        "last_checked": (
                            source.compliance_last_checked.isoformat()
                            if source.compliance_last_checked
                            else None
                        ),
                        "legal_review_status": source.legal_review_status,
                    }
                )

            return non_compliant_data

    async def validate_all_sources(self, force: bool = False) -> dict:
        """Validate compliance for all sources"""
        async with self.db_manager.get_session() as session:
            query = select(NewsSource).where(
                NewsSource.status.in_(["active", "inactive"])
            )
            result = await session.execute(query)
            sources = result.scalars().all()

            validated_count = 0
            violation_count = 0
            errors = []

            for source in sources:
                try:
                    # Skip if recently validated (unless force)
                    if not force and source.compliance_last_checked:
                        days_since_check = (
                            datetime.now() - source.compliance_last_checked
                        ).days
                        if days_since_check < 1:  # Skip if checked within 24 hours
                            continue

                    self.log(f"Validating: {source.name}", "info")

                    # Basic compliance checks
                    violations = []

                    # Check robots.txt compliance
                    if not source.robots_txt_url:
                        violations.append("Missing robots.txt URL")
                        source.robots_txt_compliant = False
                    else:
                        source.robots_txt_compliant = True

                    # Check legal contact
                    if not source.legal_contact_email:
                        violations.append("Missing legal contact email")
                        source.legal_contact_verified = False
                    else:
                        source.legal_contact_verified = True

                    # Check fair use documentation
                    if not source.fair_use_basis or len(source.fair_use_basis) < 50:
                        violations.append("Insufficient fair use documentation")
                        source.fair_use_documented = False
                    else:
                        source.fair_use_documented = True

                    # Check terms of service
                    if not source.terms_of_service_url:
                        violations.append("Missing terms of service URL")
                        source.terms_acceptable = False
                    else:
                        source.terms_acceptable = True

                    # Data minimization is enforced by design
                    source.data_minimization_applied = True

                    # Update risk level
                    if len(violations) == 0:
                        source.risk_level = "low"
                    elif len(violations) <= 2:
                        source.risk_level = "medium"
                    else:
                        source.risk_level = "high"

                    # Update compliance timestamp
                    source.compliance_last_checked = datetime.now()

                    # Log compliance action
                    audit_entry = ComplianceAuditLog(
                        table_name="news_sources",
                        record_id=source.id,
                        action="validate",
                        new_values={
                            "violations": violations,
                            "risk_level": source.risk_level,
                        },
                        legal_basis="Compliance validation for academic research",
                        compliance_notes=f"Found {len(violations)} violations",
                        risk_assessment=source.risk_level,
                        performed_by="cli_system",
                        performed_at=datetime.now(),
                    )
                    session.add(audit_entry)

                    validated_count += 1
                    if violations:
                        violation_count += 1

                except Exception as e:
                    error_msg = f"Error validating {source.name}: {str(e)}"
                    errors.append(error_msg)
                    self.log(error_msg, "error")

            await session.commit()

            self.log(f"Validated {validated_count} sources", "success")
            if violation_count > 0:
                self.log(f"Found violations in {violation_count} sources", "warning")

            return {
                "validated_count": validated_count,
                "violation_count": violation_count,
                "error_count": len(errors),
                "errors": errors,
                "validation_timestamp": datetime.now().isoformat(),
            }

    async def get_audit_trail(self, limit: int = 100, days: int = 30) -> List[dict]:
        """Get compliance audit trail"""
        async with self.db_manager.get_session() as session:
            query = (
                select(ComplianceAuditLog)
                .where(
                    ComplianceAuditLog.performed_at
                    >= datetime.now() - timedelta(days=days)
                )
                .order_by(ComplianceAuditLog.performed_at.desc())
                .limit(limit)
            )

            result = await session.execute(query)
            audit_entries = result.scalars().all()

            audit_data = []
            for entry in audit_entries:
                audit_data.append(
                    {
                        "id": entry.id,
                        "table_name": entry.table_name,
                        "record_id": entry.record_id,
                        "action": entry.action,
                        "performed_by": entry.performed_by,
                        "performed_at": entry.performed_at.isoformat(),
                        "risk_assessment": entry.risk_assessment,
                        "compliance_notes": entry.compliance_notes,
                        "legal_basis": entry.legal_basis,
                    }
                )

            return audit_data

    async def create_legal_notice(
        self,
        source_id: int,
        notice_type: str,
        title: str,
        content: str,
        effective_date: datetime,
        expiration_date: Optional[datetime] = None,
    ) -> dict:
        """Create a legal notice for a source"""
        async with self.db_manager.get_session() as session:
            # Verify source exists
            source_query = select(NewsSource).where(NewsSource.id == source_id)
            source_result = await session.execute(source_query)
            source = source_result.scalar()

            if not source:
                raise click.ClickException(f"Source with ID {source_id} not found")

            notice = LegalNotice(
                source_id=source_id,
                notice_type=notice_type,
                title=title,
                content=content,
                effective_date=effective_date.date(),
                expiration_date=expiration_date.date() if expiration_date else None,
                status="active",
                legal_contact="cli_system",
            )

            session.add(notice)
            await session.commit()
            await session.refresh(notice)

            self.log(f"Created legal notice for source: {source.name}", "success")

            return {
                "notice_id": notice.id,
                "source_id": source_id,
                "source_name": source.name,
                "notice_type": notice_type,
                "title": title,
                "effective_date": notice.effective_date.isoformat(),
                "created_at": notice.created_at.isoformat(),
            }

    async def get_legal_notices(self, source_id: Optional[int] = None) -> List[dict]:
        """Get legal notices"""
        async with self.db_manager.get_session() as session:
            query = select(LegalNotice, NewsSource).join(
                NewsSource, LegalNotice.source_id == NewsSource.id
            )

            if source_id:
                query = query.where(LegalNotice.source_id == source_id)

            query = query.order_by(LegalNotice.created_at.desc())

            result = await session.execute(query)
            notices_data = result.all()

            notices = []
            for notice, source in notices_data:
                notices.append(
                    {
                        "id": notice.id,
                        "source_id": notice.source_id,
                        "source_name": source.name,
                        "notice_type": notice.notice_type,
                        "title": notice.title,
                        "content": notice.content,
                        "status": notice.status,
                        "effective_date": notice.effective_date.isoformat(),
                        "expiration_date": (
                            notice.expiration_date.isoformat()
                            if notice.expiration_date
                            else None
                        ),
                        "created_at": notice.created_at.isoformat(),
                    }
                )

            return notices


# CLI Commands
@click.group()
@click.pass_context
def compliance(ctx):
    """Compliance management and monitoring commands"""
    ctx.ensure_object(dict)
    ctx.obj["cli"] = ComplianceCLI()


@compliance.command()
@common_options
@click.pass_context
@async_command
async def dashboard(ctx, verbose, quiet, format):
    """Show compliance dashboard overview"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    dashboard_data = await cli.get_compliance_dashboard()

    if format == "json":
        click.echo(cli.format_json(dashboard_data))
    else:
        click.echo("\n📊 Compliance Dashboard")
        click.echo(f"  Total Sources: {dashboard_data['total_sources']}")
        click.echo(
            f"  Compliant Sources: {dashboard_data['compliant_sources']} ({dashboard_data['compliance_rate']:.1%})"
        )
        click.echo(f"  Non-Compliant: {dashboard_data['non_compliant_sources']}")
        click.echo(f"  Pending Review: {dashboard_data['pending_review']}")
        click.echo(f"  High Risk Sources: {dashboard_data['high_risk_sources']}")
        click.echo(f"  Recent Violations (30d): {dashboard_data['recent_violations']}")

        # Status indicator
        if dashboard_data["compliance_rate"] >= 0.9:
            status = "🟢 EXCELLENT"
        elif dashboard_data["compliance_rate"] >= 0.7:
            status = "🟡 GOOD"
        else:
            status = "🔴 NEEDS ATTENTION"

        click.echo(f"  Overall Status: {status}")


@compliance.command()
@common_options
@click.pass_context
@async_command
async def violations(ctx, verbose, quiet, format):
    """Show sources with compliance violations"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    violations = await cli.get_non_compliant_sources()

    if format == "json":
        click.echo(cli.format_json({"violations": violations}))
    else:
        if not violations:
            cli.log("No compliance violations found ✅", "success")
            return

        click.echo(f"\n❌ Found {len(violations)} sources with compliance violations:")

        for violation in violations:
            click.echo(f"\n  📰 {violation['name']} (ID: {violation['id']})")
            click.echo(f"     Risk Level: {violation['risk_level'].upper()}")
            click.echo(f"     Violations:")
            for v in violation["violations"]:
                click.echo(f"       - {v}")
            if violation["last_checked"]:
                click.echo(f"     Last Checked: {violation['last_checked']}")


@compliance.command()
@click.option("--force", is_flag=True, help="Force validation even if recently checked")
@common_options
@click.pass_context
@async_command
async def validate_all(ctx, force, verbose, quiet, format):
    """Validate compliance for all sources"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    if not force and not cli.confirm_action(
        "Validate compliance for all sources?", True
    ):
        click.echo("Operation cancelled")
        return

    result = await cli.validate_all_sources(force)

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(f"\n✅ Compliance validation completed")
        click.echo(f"  Validated: {result['validated_count']} sources")
        click.echo(f"  With Violations: {result['violation_count']} sources")

        if result["error_count"] > 0:
            click.echo(f"  Errors: {result['error_count']}")
            if verbose:
                for error in result["errors"]:
                    click.echo(f"    - {error}")


@compliance.command()
@click.option(
    "--limit", type=int, default=100, help="Maximum number of entries to show"
)
@click.option("--days", type=int, default=30, help="Number of days to look back")
@common_options
@click.pass_context
@async_command
async def audit(ctx, limit, days, verbose, quiet, format):
    """Show compliance audit trail"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    audit_data = await cli.get_audit_trail(limit, days)

    if format == "json":
        click.echo(cli.format_json({"audit_trail": audit_data}))
    else:
        if not audit_data:
            cli.log(f"No audit entries found in last {days} days", "warning")
            return

        click.echo(
            f"\n📋 Compliance Audit Trail (last {days} days, {len(audit_data)} entries):"
        )

        headers = ["Date", "Table", "Record ID", "Action", "Risk", "Performed By"]
        rows = [
            [
                entry["performed_at"][:16],
                entry["table_name"],
                entry["record_id"],
                entry["action"],
                entry["risk_assessment"] or "N/A",
                entry["performed_by"],
            ]
            for entry in audit_data
        ]
        click.echo(cli.format_table(rows, headers))


@compliance.command()
@click.argument("source_id", type=int)
@click.argument(
    "notice_type",
    type=click.Choice(
        [
            "fair_use",
            "dmca_notice",
            "takedown_request",
            "legal_review",
            "compliance_warning",
        ]
    ),
)
@click.argument("title")
@click.option("--content", required=True, help="Notice content")
@click.option(
    "--effective-date",
    type=click.DateTime(),
    default=lambda: datetime.now(),
    help="Effective date (YYYY-MM-DD)",
)
@click.option(
    "--expiration-date", type=click.DateTime(), help="Expiration date (YYYY-MM-DD)"
)
@common_options
@click.pass_context
@async_command
async def create_notice(
    ctx,
    source_id,
    notice_type,
    title,
    content,
    effective_date,
    expiration_date,
    verbose,
    quiet,
    format,
):
    """Create a legal notice for a source"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    result = await cli.create_legal_notice(
        source_id=source_id,
        notice_type=notice_type,
        title=title,
        content=content,
        effective_date=effective_date,
        expiration_date=expiration_date,
    )

    if format == "json":
        click.echo(cli.format_json(result))
    else:
        click.echo(f"✅ Created legal notice for source: {result['source_name']}")
        click.echo(f"   Notice ID: {result['notice_id']}")
        click.echo(f"   Type: {result['notice_type']}")
        click.echo(f"   Title: {result['title']}")


@compliance.command()
@click.option("--source-id", type=int, help="Filter by source ID")
@common_options
@click.pass_context
@async_command
async def notices(ctx, source_id, verbose, quiet, format):
    """List legal notices"""
    cli = ctx.obj["cli"]
    cli.verbose = verbose
    cli.quiet = quiet

    notices = await cli.get_legal_notices(source_id)

    if format == "json":
        click.echo(cli.format_json({"notices": notices}))
    else:
        if not notices:
            cli.log("No legal notices found", "warning")
            return

        headers = ["ID", "Source", "Type", "Title", "Status", "Effective Date"]
        rows = [
            [
                n["id"],
                n["source_name"][:20],
                n["notice_type"],
                n["title"][:30],
                n["status"],
                n["effective_date"][:10],
            ]
            for n in notices
        ]
        click.echo(cli.format_table(rows, headers))


if __name__ == "__main__":
    compliance()
