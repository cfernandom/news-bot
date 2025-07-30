#!/usr/bin/env python3
"""
init_data.py - Script de inicialización de datos de ejemplo para PreventIA News Analytics
Version: 1.0
Fecha: 29 de Julio de 2025

Este script carga datos de ejemplo en el sistema para demostración y testing.
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Añadir el directorio raíz al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from services.data.database.connection import get_database_connection
from services.data.database.models import (
    Article,
    NewsSource,
    ProcessingStatus,
    SentimentAnalysis,
    SentimentLabel,
    TopicCategory,
    TopicClassification,
    ValidationStatus,
)

# Datos de ejemplo
SAMPLE_SOURCES = [
    {
        "name": "Instituto Nacional del Cáncer",
        "base_url": "https://www.cancer.gov/espanol",
        "language": "es",
        "country": "Estados Unidos",
        "extractor_class": "DefaultExtractor",
        "is_active": True,
        "validation_status": ValidationStatus.VALIDATED,
        "robots_txt_url": "https://www.cancer.gov/robots.txt",
        "crawl_delay_seconds": 2,
        "scraping_allowed": True,
        "terms_of_service_url": "https://www.cancer.gov/policies",
        "fair_use_basis": "Información médica de dominio público para educación y prevención",
        "compliance_score": 0.95,
        "legal_contact_email": "webmaster@cancer.gov",
    },
    {
        "name": "Fundación Española Contra el Cáncer",
        "base_url": "https://www.aecc.es",
        "language": "es",
        "country": "España",
        "extractor_class": "DefaultExtractor",
        "is_active": True,
        "validation_status": ValidationStatus.VALIDATED,
        "robots_txt_url": "https://www.aecc.es/robots.txt",
        "crawl_delay_seconds": 3,
        "scraping_allowed": True,
        "terms_of_service_url": "https://www.aecc.es/aviso-legal",
        "fair_use_basis": "Información educativa sin fines comerciales para prevención médica",
        "compliance_score": 0.92,
        "legal_contact_email": "info@aecc.es",
    },
    {
        "name": "Mayo Clinic - Cáncer de Mama",
        "base_url": "https://www.mayoclinic.org/es/diseases-conditions/breast-cancer",
        "language": "es",
        "country": "Estados Unidos",
        "extractor_class": "DefaultExtractor",
        "is_active": True,
        "validation_status": ValidationStatus.VALIDATED,
        "robots_txt_url": "https://www.mayoclinic.org/robots.txt",
        "crawl_delay_seconds": 2,
        "scraping_allowed": True,
        "terms_of_service_url": "https://www.mayoclinic.org/about-this-site/terms-conditions-use-policy",
        "fair_use_basis": "Información médica educativa para investigación y prevención",
        "compliance_score": 0.98,
        "legal_contact_email": "webmaster@mayoclinic.org",
    },
    {
        "name": "Breast Cancer Research Foundation",
        "base_url": "https://www.bcrf.org",
        "language": "en",
        "country": "Estados Unidos",
        "extractor_class": "DefaultExtractor",
        "is_active": True,
        "validation_status": ValidationStatus.VALIDATED,
        "robots_txt_url": "https://www.bcrf.org/robots.txt",
        "crawl_delay_seconds": 2,
        "scraping_allowed": True,
        "terms_of_service_url": "https://www.bcrf.org/terms-of-use",
        "fair_use_basis": "Información científica para investigación médica sin fines comerciales",
        "compliance_score": 0.94,
        "legal_contact_email": "info@bcrf.org",
    },
    {
        "name": "Asociación Española Contra el Cáncer - Noticias",
        "base_url": "https://www.aecc.es/actualidad/noticias",
        "language": "es",
        "country": "España",
        "extractor_class": "DefaultExtractor",
        "is_active": True,
        "validation_status": ValidationStatus.PENDING,
        "robots_txt_url": "https://www.aecc.es/robots.txt",
        "crawl_delay_seconds": 3,
        "scraping_allowed": True,
        "fair_use_basis": "Noticias de actualidad médica para análisis de tendencias",
        "compliance_score": 0.88,
    },
]

SAMPLE_ARTICLES = [
    {
        "title": "Nuevos avances en la detección precoz del cáncer de mama",
        "content": "Los investigadores han desarrollado una nueva técnica de inteligencia artificial que puede detectar signos tempranos de cáncer de mama con una precisión del 95%. Esta tecnología revolucionaria utiliza algoritmos de aprendizaje profundo para analizar mamografías y identificar patrones sutiles que podrían pasar desapercibidos para el ojo humano. El estudio, publicado en la revista Nature Medicine, analizó más de 100,000 mamografías y demostró que la IA puede reducir significativamente los falsos positivos y negativos en el diagnóstico.",
        "url": "https://www.cancer.gov/espanol/noticias/deteccion-precoz-ia",
        "published_at": datetime.now(timezone.utc) - timedelta(days=2),
        "source_id": 1,
        "processing_status": ProcessingStatus.COMPLETED,
        "sentiment_score": 0.75,
        "sentiment_label": SentimentLabel.POSITIVE,
        "topic_category": TopicCategory.DIAGNOSIS,
        "topic_confidence": 0.92,
    },
    {
        "title": "Testimonio: Mi experiencia con el tratamiento del cáncer de mama",
        "content": "María García, de 45 años, comparte su experiencia personal con el diagnóstico y tratamiento del cáncer de mama. 'Cuando recibí el diagnóstico, sentí que mi mundo se desplomaba. Pero gracias al apoyo de mi familia y el excelente equipo médico, pude superarlo'. García destaca la importancia del apoyo emocional durante el tratamiento y cómo los grupos de apoyo la ayudaron a mantener una actitud positiva. Actualmente, lleva tres años libre de cáncer y se dedica a ayudar a otras mujeres que pasan por la misma situación.",
        "url": "https://www.aecc.es/testimonio-maria-garcia",
        "published_at": datetime.now(timezone.utc) - timedelta(days=5),
        "source_id": 2,
        "processing_status": ProcessingStatus.COMPLETED,
        "sentiment_score": 0.60,
        "sentiment_label": SentimentLabel.POSITIVE,
        "topic_category": TopicCategory.TESTIMONIALS,
        "topic_confidence": 0.89,
    },
    {
        "title": "Efectos secundarios de la quimioterapia: qué esperar",
        "content": "La quimioterapia es uno de los tratamientos más comunes para el cáncer de mama, pero puede causar varios efectos secundarios. Los más frecuentes incluyen fatiga, náuseas, pérdida de cabello y mayor susceptibilidad a infecciones. Es importante que los pacientes estén preparados y sepan qué esperar durante el tratamiento. Los médicos recomiendan mantener una dieta equilibrada, descansar lo suficiente y comunicar cualquier síntoma preocupante al equipo médico. Existen medicamentos y terapias complementarias que pueden ayudar a manejar estos efectos secundarios.",
        "url": "https://www.mayoclinic.org/es/quimioterapia-efectos-secundarios",
        "published_at": datetime.now(timezone.utc) - timedelta(days=7),
        "source_id": 3,
        "processing_status": ProcessingStatus.COMPLETED,
        "sentiment_score": -0.20,
        "sentiment_label": SentimentLabel.NEGATIVE,
        "topic_category": TopicCategory.CHEMOTHERAPY,
        "topic_confidence": 0.87,
    },
    {
        "title": "Investigación promisoria sobre inmunoterapia para cáncer de mama",
        "content": "Un nuevo estudio clínico está investigando el uso de inmunoterapia en combinación con tratamientos tradicionales para el cáncer de mama triple negativo. Los resultados preliminares muestran una mejora significativa en las tasas de supervivencia y una reducción en la progresión de la enfermedad. La inmunoterapia funciona estimulando el sistema inmunológico del paciente para que reconozca y ataque las células cancerosas. Aunque aún está en fase de investigación, los científicos se muestran optimistas sobre el potencial de esta nueva aproximación terapéutica.",
        "url": "https://www.bcrf.org/inmunoterapia-cancer-mama-estudio",
        "published_at": datetime.now(timezone.utc) - timedelta(days=10),
        "source_id": 4,
        "processing_status": ProcessingStatus.COMPLETED,
        "sentiment_score": 0.65,
        "sentiment_label": SentimentLabel.POSITIVE,
        "topic_category": TopicCategory.IMMUNOTHERAPY,
        "topic_confidence": 0.94,
    },
    {
        "title": "Importancia de la autoexploración mamaria mensual",
        "content": "La autoexploración mamaria es una herramienta importante para la detección temprana del cáncer de mama. Las mujeres deben realizarla mensualmente, preferiblemente una semana después de la menstruación. Durante la exploración, se debe buscar cualquier cambio en el tamaño, forma o textura de los senos, así como la presencia de bultos, engrosamiento de la piel o secreción del pezón. Aunque la mayoría de los cambios no son cancerosos, es importante consultar con un médico ante cualquier anomalía. La detección temprana puede mejorar significativamente las opciones de tratamiento y el pronóstico.",
        "url": "https://www.aecc.es/prevencion/autoexploracion-mamaria",
        "published_at": datetime.now(timezone.utc) - timedelta(days=12),
        "source_id": 5,
        "processing_status": ProcessingStatus.COMPLETED,
        "sentiment_score": 0.45,
        "sentiment_label": SentimentLabel.NEUTRAL,
        "topic_category": TopicCategory.PREVENTION,
        "topic_confidence": 0.91,
    },
]


class DataInitializer:
    def __init__(self):
        self.db = None

    async def connect(self):
        """Establecer conexión con la base de datos"""
        try:
            self.db = await get_database_connection()
            print("✅ Conexión a base de datos establecida")
        except Exception as e:
            print(f"❌ Error conectando a base de datos: {e}")
            sys.exit(1)

    async def close(self):
        """Cerrar conexión con la base de datos"""
        if self.db:
            await self.db.close()
            print("✅ Conexión cerrada")

    async def create_sample_sources(self):
        """Crear fuentes de noticias de ejemplo"""
        print("📰 Creando fuentes de noticias de ejemplo...")

        for source_data in SAMPLE_SOURCES:
            try:
                # Verificar si la fuente ya existe
                query = "SELECT id FROM news_sources WHERE base_url = $1"
                existing = await self.db.fetchrow(query, source_data["base_url"])

                if existing:
                    print(f"   ⚠️  Fuente ya existe: {source_data['name']}")
                    continue

                # Insertar nueva fuente
                query = """
                INSERT INTO news_sources (
                    name, base_url, language, country, extractor_class, is_active,
                    validation_status, robots_txt_url, crawl_delay_seconds,
                    scraping_allowed, terms_of_service_url, fair_use_basis,
                    compliance_score, legal_contact_email,
                    last_validation_at, last_compliance_check
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16
                ) RETURNING id
                """

                now = datetime.now(timezone.utc)
                result = await self.db.fetchrow(
                    query,
                    source_data["name"],
                    source_data["base_url"],
                    source_data["language"],
                    source_data["country"],
                    source_data["extractor_class"],
                    source_data["is_active"],
                    source_data["validation_status"],
                    source_data["robots_txt_url"],
                    source_data["crawl_delay_seconds"],
                    source_data["scraping_allowed"],
                    source_data.get("terms_of_service_url"),
                    source_data["fair_use_basis"],
                    source_data["compliance_score"],
                    source_data.get("legal_contact_email"),
                    now,
                    now,
                )

                print(f"   ✅ Creada: {source_data['name']} (ID: {result['id']})")

            except Exception as e:
                print(f"   ❌ Error creando fuente {source_data['name']}: {e}")

    async def create_sample_articles(self):
        """Crear artículos de ejemplo"""
        print("📄 Creando artículos de ejemplo...")

        for article_data in SAMPLE_ARTICLES:
            try:
                # Verificar si el artículo ya existe
                query = "SELECT id FROM articles WHERE url = $1"
                existing = await self.db.fetchrow(query, article_data["url"])

                if existing:
                    print(f"   ⚠️  Artículo ya existe: {article_data['title'][:50]}...")
                    continue

                # Insertar nuevo artículo
                query = """
                INSERT INTO articles (
                    title, content, url, published_at, source_id, processing_status,
                    created_at, updated_at
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8
                ) RETURNING id
                """

                now = datetime.now(timezone.utc)
                result = await self.db.fetchrow(
                    query,
                    article_data["title"],
                    article_data["content"],
                    article_data["url"],
                    article_data["published_at"],
                    article_data["source_id"],
                    article_data["processing_status"],
                    now,
                    now,
                )

                article_id = result["id"]

                # Crear análisis de sentimiento
                sentiment_query = """
                INSERT INTO sentiment_analysis (
                    article_id, sentiment_score, sentiment_label, confidence_score,
                    analyzed_at
                ) VALUES ($1, $2, $3, $4, $5)
                """

                await self.db.execute(
                    sentiment_query,
                    article_id,
                    article_data["sentiment_score"],
                    article_data["sentiment_label"],
                    abs(article_data["sentiment_score"]),
                    now,
                )

                # Crear clasificación de tópico
                topic_query = """
                INSERT INTO topic_classification (
                    article_id, topic_category, confidence_score, classified_at
                ) VALUES ($1, $2, $3, $4)
                """

                await self.db.execute(
                    topic_query,
                    article_id,
                    article_data["topic_category"],
                    article_data["topic_confidence"],
                    now,
                )

                print(
                    f"   ✅ Creado: {article_data['title'][:50]}... (ID: {article_id})"
                )

            except Exception as e:
                print(f"   ❌ Error creando artículo: {e}")

    async def create_demo_analytics(self):
        """Crear datos analíticos adicionales para demostración"""
        print("📊 Creando datos analíticos adicionales...")

        try:
            # Crear algunos registros de auditoría de compliance
            audit_query = """
            INSERT INTO compliance_audit_log (
                source_id, check_type, status, details, checked_at
            ) VALUES ($1, $2, $3, $4, $5)
            """

            now = datetime.now(timezone.utc)
            audit_records = [
                (
                    1,
                    "robots_txt",
                    "passed",
                    "robots.txt encontrado y parseable",
                    now - timedelta(hours=2),
                ),
                (
                    2,
                    "robots_txt",
                    "passed",
                    "robots.txt válido con crawl-delay especificado",
                    now - timedelta(hours=3),
                ),
                (
                    3,
                    "terms_of_service",
                    "passed",
                    "Términos de servicio revisados y compatibles",
                    now - timedelta(hours=4),
                ),
                (
                    4,
                    "fair_use",
                    "passed",
                    "Base de fair use documentada adecuadamente",
                    now - timedelta(hours=5),
                ),
                (
                    5,
                    "robots_txt",
                    "pending",
                    "Verificación de robots.txt programada",
                    now - timedelta(minutes=30),
                ),
            ]

            for record in audit_records:
                await self.db.execute(audit_query, *record)

            print("   ✅ Registros de auditoría de compliance creados")

        except Exception as e:
            print(f"   ❌ Error creando datos analíticos: {e}")

    async def verify_data(self):
        """Verificar que los datos se crearon correctamente"""
        print("🔍 Verificando datos creados...")

        try:
            # Contar fuentes
            sources_count = await self.db.fetchval("SELECT COUNT(*) FROM news_sources")
            print(f"   📰 Fuentes de noticias: {sources_count}")

            # Contar artículos
            articles_count = await self.db.fetchval("SELECT COUNT(*) FROM articles")
            print(f"   📄 Artículos: {articles_count}")

            # Contar análisis de sentimiento
            sentiment_count = await self.db.fetchval(
                "SELECT COUNT(*) FROM sentiment_analysis"
            )
            print(f"   😊 Análisis de sentimiento: {sentiment_count}")

            # Contar clasificaciones de tópico
            topic_count = await self.db.fetchval(
                "SELECT COUNT(*) FROM topic_classification"
            )
            print(f"   🏷️  Clasificaciones de tópico: {topic_count}")

            # Contar registros de auditoría
            audit_count = await self.db.fetchval(
                "SELECT COUNT(*) FROM compliance_audit_log"
            )
            print(f"   📋 Registros de auditoría: {audit_count}")

            print("✅ Verificación completada")

        except Exception as e:
            print(f"❌ Error verificando datos: {e}")


async def main():
    """Función principal"""
    print("🚀 Iniciando carga de datos de ejemplo...")
    print("=" * 50)

    initializer = DataInitializer()

    try:
        await initializer.connect()
        await initializer.create_sample_sources()
        await initializer.create_sample_articles()
        await initializer.create_demo_analytics()
        await initializer.verify_data()

        print("=" * 50)
        print("✅ ¡Datos de ejemplo cargados exitosamente!")
        print("")
        print("🌐 Accede al dashboard en: http://localhost:3000")
        print("🔧 Panel de administración: http://localhost:3000/admin")
        print("📚 Documentación API: http://localhost:8000/docs")

    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        sys.exit(1)
    finally:
        await initializer.close()


if __name__ == "__main__":
    # Verificar que asyncio está disponible
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Inicialización cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error ejecutando script: {e}")
        sys.exit(1)
