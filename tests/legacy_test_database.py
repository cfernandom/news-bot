#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a PostgreSQL
"""

import asyncio
import os

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar el database manager
from services.data.database.connection import close_database, db_manager, init_database


async def test_database():
    """Prueba de conexión y consultas básicas"""

    print("🔧 Inicializando conexión a PostgreSQL...")
    try:
        await init_database()
        print("✅ Conexión establecida exitosamente")
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return

    try:
        # Test 1: Versión de PostgreSQL
        print("\n📊 Test 1: Versión de PostgreSQL")
        version = await db_manager.execute_sql_scalar("SELECT version()")
        print(f"✅ Versión: {version}")

        # Test 2: Verificar tablas creadas
        print("\n📊 Test 2: Verificar tablas creadas")
        tables_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
        """
        tables = await db_manager.execute_sql(tables_query)
        print("✅ Tablas encontradas:")
        for table in tables:
            print(f"   - {table['table_name']}")

        # Test 3: Verificar fuentes de noticias insertadas
        print("\n📊 Test 3: Verificar fuentes de noticias")
        sources_query = "SELECT id, name, base_url, language, country FROM news_sources"
        sources = await db_manager.execute_sql(sources_query)
        print(f"✅ {len(sources)} fuentes encontradas:")
        for source in sources:
            print(f"   - {source['name']} ({source['language']}, {source['country']})")

        # Test 4: Probar inserción de un artículo de prueba
        print("\n📊 Test 4: Insertar artículo de prueba")
        from datetime import datetime

        # Insertar artículo de prueba
        insert_query = """
        INSERT INTO articles (source_id, title, url, content, published_at, language, country)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, title
        """

        article_data = (
            1,  # source_id (primer source)
            "Test Article: Avances en detección temprana",
            "https://test.com/test-article-123",
            "Este es un artículo de prueba sobre avances en la detección temprana del cáncer de seno...",
            datetime.now(),
            "es",
            "Colombia",
        )

        result = await db_manager.execute_sql_one(insert_query, *article_data)
        print(f"✅ Artículo insertado: ID {result['id']}, Título: '{result['title']}'")

        # Test 5: Consultar artículos
        print("\n📊 Test 5: Consultar artículos")
        articles_query = """
        SELECT a.id, a.title, a.language, a.country, ns.name as source_name
        FROM articles a
        JOIN news_sources ns ON a.source_id = ns.id
        ORDER BY a.created_at DESC
        LIMIT 5
        """
        articles = await db_manager.execute_sql(articles_query)
        print(f"✅ {len(articles)} artículos encontrados:")
        for article in articles:
            print(
                f"   - [{article['id']}] {article['title'][:50]}... ({article['source_name']})"
            )

        # Test 6: Test de ORM con SQLAlchemy
        print("\n📊 Test 6: Test de SQLAlchemy ORM")
        from sqlalchemy import select

        from services.data.database.models import NewsSource

        async with db_manager.get_session() as session:
            # Consultar fuentes usando ORM
            stmt = select(NewsSource).where(NewsSource.is_active == True)
            result = await session.execute(stmt)
            active_sources = result.scalars().all()

            print(f"✅ {len(active_sources)} fuentes activas (via ORM):")
            for source in active_sources:
                print(f"   - {source.name} ({source.validation_status})")

        print("\n🎉 Todos los tests pasaron exitosamente!")

    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback

        traceback.print_exc()

    finally:
        await close_database()
        print("\n📝 Conexiones cerradas")


if __name__ == "__main__":
    asyncio.run(test_database())
