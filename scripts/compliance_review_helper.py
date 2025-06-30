#!/usr/bin/env python3
"""
Compliance Review Helper for PreventIA News Analytics
Helps review and update legal status of articles systematically.

Usage:
    python scripts/compliance_review_helper.py [--action] [--limit N]

Actions:
    --preview: Show articles needing review
    --approve-all: Mark all as approved for academic research use
    --remove-content: Remove full content, keep only summaries
    --set-fair-use: Mark articles as fair use for academic research
"""

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.data.database.connection import DatabaseManager


class ComplianceReviewHelper:
    """Helper for systematic compliance review of articles."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def preview_articles_needing_review(self, limit: int = 10):
        """Show sample of articles that need legal review."""
        query = """
            SELECT
                a.id,
                a.title,
                a.url,
                ns.name as source_name,
                a.scraped_at,
                a.legal_review_status,
                a.copyright_status,
                LENGTH(a.content) as content_length
            FROM articles a
            JOIN news_sources ns ON a.source_id = ns.id
            WHERE a.legal_review_status = 'needs_review'
            ORDER BY a.scraped_at DESC
            LIMIT $1
        """

        articles = await self.db_manager.execute_sql(query, limit)

        print(f"\n📋 ARTÍCULOS QUE REQUIEREN REVISIÓN LEGAL (showing {len(articles)}):")
        print("=" * 80)

        for article in articles:
            print(f"\nID: {article['id']}")
            print(f"Título: {article['title'][:100]}...")
            print(f"Fuente: {article['source_name']}")
            print(f"URL: {article['url']}")
            print(f"Contenido: {article['content_length']:,} caracteres")
            print(f"Scraped: {article['scraped_at']}")
            print("-" * 80)

    async def get_compliance_summary(self):
        """Get overall compliance summary."""
        # Total articles by status
        status_query = """
            SELECT
                legal_review_status,
                COUNT(*) as count,
                AVG(LENGTH(content)) as avg_content_length
            FROM articles
            GROUP BY legal_review_status
        """

        # Sources summary
        sources_query = """
            SELECT
                ns.name,
                COUNT(a.id) as article_count,
                ns.scraping_allowed,
                ns.crawl_delay_seconds
            FROM news_sources ns
            LEFT JOIN articles a ON ns.id = a.source_id
            GROUP BY ns.id, ns.name, ns.scraping_allowed, ns.crawl_delay_seconds
            ORDER BY article_count DESC
        """

        status_data = await self.db_manager.execute_sql(status_query)
        sources_data = await self.db_manager.execute_sql(sources_query)

        print("\n📊 RESUMEN DE CUMPLIMIENTO LEGAL")
        print("=" * 60)

        print("\n🔍 Estado de Revisión Legal:")
        total_articles = sum(row["count"] for row in status_data)
        for row in status_data:
            percentage = (row["count"] / total_articles) * 100
            avg_length = int(row["avg_content_length"] or 0)
            print(
                f"  {row['legal_review_status']}: {row['count']} artículos ({percentage:.1f}%) - {avg_length:,} chars promedio"
            )

        print(f"\n📈 Total de artículos: {total_articles}")

        print("\n🌐 Fuentes de Noticias:")
        for row in sources_data:
            scraping_status = (
                "✅ Permitido"
                if row["scraping_allowed"]
                else "❌ Bloqueado"
                if row["scraping_allowed"] is False
                else "❓ Desconocido"
            )
            print(
                f"  {row['name']}: {row['article_count']} artículos - {scraping_status} - Delay: {row['crawl_delay_seconds']}s"
            )

    async def approve_for_academic_research(self, limit: int = None):
        """Mark articles as approved for academic research use (fair use)."""
        print(f"\n🎓 APROBANDO ARTÍCULOS PARA USO ACADÉMICO...")

        # Update query
        update_query = """
            UPDATE articles
            SET
                legal_review_status = 'approved',
                copyright_status = 'fair_use',
                fair_use_basis = 'Academic research and educational use under Colombian Law 1581/2012 and international fair use doctrine. Non-commercial analysis for breast cancer awareness research at UCOMPENSAR.',
                updated_at = CURRENT_TIMESTAMP
            WHERE legal_review_status = 'needs_review'
        """

        if limit:
            update_query += f" AND id IN (SELECT id FROM articles WHERE legal_review_status = 'needs_review' LIMIT {limit})"

        # Count first
        count_query = """
            SELECT COUNT(*) FROM articles WHERE legal_review_status = 'needs_review'
        """

        if limit:
            count_query += f" AND id IN (SELECT id FROM articles WHERE legal_review_status = 'needs_review' LIMIT {limit})"

        count_result = await self.db_manager.execute_sql_scalar(count_query)

        print(f"Se aprobarán {count_result} artículos para uso académico...")
        confirm = input("¿Continuar? (y/N): ")

        if confirm.lower() == "y":
            async with self.db_manager.get_connection() as conn:
                await conn.execute(update_query)

            print(f"✅ {count_result} artículos aprobados para uso académico")

            # Log the action
            await self._log_compliance_action(
                "bulk_approval",
                f"Approved {count_result} articles for academic research use",
            )
        else:
            print("❌ Operación cancelada")

    async def remove_full_content_keep_summaries(self, limit: int = None):
        """Remove full content from articles, keeping only summaries and metadata."""
        print(f"\n🗑️  ELIMINANDO CONTENIDO COMPLETO, MANTENIENDO RESÚMENES...")

        # First, let's see what we're working with
        content_query = """
            SELECT
                COUNT(*) as total_articles,
                COUNT(CASE WHEN content IS NOT NULL AND LENGTH(content) > 100 THEN 1 END) as articles_with_content,
                COUNT(CASE WHEN summary IS NOT NULL AND LENGTH(summary) > 50 THEN 1 END) as articles_with_summary,
                AVG(LENGTH(content)) as avg_content_length,
                AVG(LENGTH(summary)) as avg_summary_length
            FROM articles
            WHERE legal_review_status = 'needs_review'
        """

        stats = await self.db_manager.execute_sql_one(content_query)

        print(f"📊 Estadísticas actuales:")
        print(f"  Total artículos: {stats['total_articles']}")
        print(f"  Con contenido completo: {stats['articles_with_content']}")
        print(f"  Con resumen: {stats['articles_with_summary']}")
        print(
            f"  Longitud promedio contenido: {int(stats['avg_content_length'] or 0):,} caracteres"
        )
        print(
            f"  Longitud promedio resumen: {int(stats['avg_summary_length'] or 0):,} caracteres"
        )

        confirm = input(
            "\n¿Eliminar contenido completo y mantener solo resúmenes? (y/N): "
        )

        if confirm.lower() == "y":
            update_query = """
                UPDATE articles
                SET
                    content = NULL,
                    content_type = 'summary',
                    copyright_status = 'cleared',
                    legal_review_status = 'approved',
                    fair_use_basis = 'Content removed, only metadata and summary retained for academic research compliance',
                    updated_at = CURRENT_TIMESTAMP
                WHERE legal_review_status = 'needs_review'
                  AND content IS NOT NULL
            """

            if limit:
                update_query += f" AND id IN (SELECT id FROM articles WHERE legal_review_status = 'needs_review' LIMIT {limit})"

            async with self.db_manager.get_connection() as conn:
                result = await conn.execute(update_query)

            print(f"✅ Contenido completo eliminado de los artículos")
            print(f"✅ Artículos actualizados a estado 'approved' con solo resúmenes")

            # Log the action
            await self._log_compliance_action(
                "content_removal",
                f"Removed full content from articles, keeping only summaries for compliance",
            )
        else:
            print("❌ Operación cancelada")

    async def _log_compliance_action(self, action: str, details: str):
        """Log compliance actions for audit trail."""
        import json

        audit_query = """
            INSERT INTO compliance_audit_log
            (table_name, record_id, action, status, details, performed_by)
            VALUES ($1, $2, $3, $4, $5, $6)
        """

        details_json = json.dumps(
            {
                "action": action,
                "details": details,
                "timestamp": datetime.now().isoformat(),
                "performed_by": "compliance_review_helper",
            }
        )

        async with self.db_manager.get_connection() as conn:
            await conn.execute(
                audit_query,
                "articles",
                0,
                action,
                "completed",
                details_json,
                "compliance_helper",
            )


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Compliance Review Helper for PreventIA"
    )
    parser.add_argument(
        "--action",
        choices=["preview", "approve-all", "remove-content", "summary"],
        default="summary",
        help="Action to perform",
    )
    parser.add_argument("--limit", type=int, help="Limit number of articles to process")

    args = parser.parse_args()

    # Initialize database
    db_manager = DatabaseManager()
    await db_manager.initialize()

    try:
        helper = ComplianceReviewHelper(db_manager)

        if args.action == "summary":
            await helper.get_compliance_summary()
            await helper.preview_articles_needing_review(5)

        elif args.action == "preview":
            await helper.preview_articles_needing_review(args.limit or 20)

        elif args.action == "approve-all":
            await helper.approve_for_academic_research(args.limit)

        elif args.action == "remove-content":
            await helper.remove_full_content_keep_summaries(args.limit)

        print(f"\n✅ Acción '{args.action}' completada")

    finally:
        await db_manager.close()


if __name__ == "__main__":
    asyncio.run(main())
