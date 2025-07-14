#!/bin/bash
# init_fresh_database.sh
# Script para inicializar una base de datos completamente nueva sin errores
# Debe ejecutarse después de docker-compose up para asegurar que todo esté correcto

set -e

echo "🔄 Iniciando configuración de base de datos fresca..."

# Verificar que los servicios estén ejecutándose
echo "📊 Verificando servicios Docker..."
if ! docker-compose ps | grep -q "healthy"; then
    echo "❌ Los servicios no están saludables. Ejecuta: docker-compose up -d"
    exit 1
fi

# Esperar a que PostgreSQL esté completamente listo
echo "⏳ Esperando PostgreSQL..."
sleep 5

# Verificar conectividad con PostgreSQL
echo "🔌 Verificando conexión a PostgreSQL..."
if ! docker-compose exec postgres pg_isready -U preventia -d preventia_news; then
    echo "❌ PostgreSQL no está listo"
    exit 1
fi

# Verificar que las migraciones se hayan ejecutado correctamente
echo "📋 Verificando migraciones..."
TABLES=$(docker-compose exec postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('news_sources', 'articles', 'compliance_audit_log', 'users', 'user_roles');")
if [ $(echo $TABLES | xargs) -lt 5 ]; then
    echo "❌ Faltan tablas en la base de datos. Aplicando migraciones..."
    docker-compose exec postgres psql -U preventia -d preventia_news -f /docker-entrypoint-initdb.d/002_source_administration.sql
fi

# Verificar que la columna 'status' exista en compliance_audit_log
echo "🔍 Verificando columna 'status' en compliance_audit_log..."
STATUS_COLUMN=$(docker-compose exec postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'compliance_audit_log' AND column_name = 'status';")
if [ $(echo $STATUS_COLUMN | xargs) -eq 0 ]; then
    echo "⚠️ Agregando columna 'status' faltante..."
    docker-compose exec postgres psql -U preventia -d preventia_news -c "ALTER TABLE compliance_audit_log ADD COLUMN status VARCHAR(50) DEFAULT 'pending';"
fi

# Verificar que las columnas de compliance estén presentes
echo "📊 Verificando columnas de compliance..."
COMPLIANCE_COLUMNS=$(docker-compose exec postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'compliance_audit_log' AND column_name IN ('compliance_score_before', 'compliance_score_after', 'risk_level', 'violations_count');")
if [ $(echo $COMPLIANCE_COLUMNS | xargs) -lt 4 ]; then
    echo "⚠️ Agregando columnas de compliance faltantes..."
    docker-compose exec postgres psql -U preventia -d preventia_news -c "
        ALTER TABLE compliance_audit_log 
        ADD COLUMN IF NOT EXISTS compliance_score_before NUMERIC(3,2),
        ADD COLUMN IF NOT EXISTS compliance_score_after NUMERIC(3,2),
        ADD COLUMN IF NOT EXISTS risk_level VARCHAR(20),
        ADD COLUMN IF NOT EXISTS violations_count INTEGER DEFAULT 0;
    "
fi

# Reiniciar API para limpiar sesiones con errores
echo "🔄 Reiniciando API para limpiar sesiones..."
docker-compose restart api

# Esperar a que la API esté lista
echo "⏳ Esperando API..."
sleep 10

# Verificar que la API esté respondiendo
echo "🔌 Verificando API..."
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$API_RESPONSE" != "200" ]; then
    echo "❌ API no está respondiendo correctamente (HTTP $API_RESPONSE)"
    exit 1
fi

# Verificar que el frontend esté accesible
echo "🌐 Verificando frontend..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$FRONTEND_RESPONSE" != "200" ]; then
    echo "❌ Frontend no está accesible (HTTP $FRONTEND_RESPONSE)"
    exit 1
fi

# Verificar que no haya fuentes duplicadas (limpiar si las hay)
echo "🧹 Verificando fuentes duplicadas..."
SOURCE_COUNT=$(docker-compose exec postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM news_sources;")
if [ $(echo $SOURCE_COUNT | xargs) -gt 0 ]; then
    echo "⚠️ Encontradas $SOURCE_COUNT fuentes. Para prueba fresca, eliminar todas..."
    read -p "¿Eliminar todas las fuentes existentes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose exec postgres psql -U preventia -d preventia_news -c "
            DELETE FROM articles; 
            DELETE FROM compliance_audit_log; 
            DELETE FROM news_sources;
        "
        echo "✅ Base de datos limpia"
    fi
fi

# Verificar conteo final
FINAL_SOURCES=$(docker-compose exec postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM news_sources;")
FINAL_ARTICLES=$(docker-compose exec postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM articles;")

echo ""
echo "🎯 INICIALIZACIÓN COMPLETA"
echo "📊 Estado de la base de datos:"
echo "   - Fuentes: $(echo $FINAL_SOURCES | xargs)"
echo "   - Artículos: $(echo $FINAL_ARTICLES | xargs)"
echo "🌐 Interfaces disponibles:"
echo "   - Admin Panel: http://localhost:3000/admin"
echo "   - Dashboard: http://localhost:3000/"
echo "   - API Health: http://localhost:8000/health"
echo ""
echo "✅ Sistema listo para uso en producción"
echo "📋 Siguiente paso: Usar admin panel para crear fuentes con información de compliance"