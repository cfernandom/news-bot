#!/bin/bash
# validate_installation.sh - Script de validación de instalación de PreventIA News Analytics
# Version: 1.0
# Fecha: 29 de Julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores para reporte final
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Función para imprimir mensajes
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_check() {
    echo -n "  Verificando $1... "
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
}

print_pass() {
    echo -e "${GREEN}✅ PASS${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
}

print_fail() {
    echo -e "${RED}❌ FAIL${NC}"
    if [ -n "$1" ]; then
        echo -e "     ${RED}$1${NC}"
    fi
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARNING${NC}"
    if [ -n "$1" ]; then
        echo -e "     ${YELLOW}$1${NC}"
    fi
    WARNING_CHECKS=$((WARNING_CHECKS + 1))
}

print_info() {
    echo -e "     ${BLUE}ℹ️  $1${NC}"
}

# Verificar dependencias del sistema
check_system_dependencies() {
    print_header "DEPENDENCIAS DEL SISTEMA"

    print_check "Docker instalado"
    if command -v docker >/dev/null 2>&1; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | sed 's/,//')
        print_pass
        print_info "Versión: $DOCKER_VERSION"
    else
        print_fail "Docker no está instalado"
    fi

    print_check "Docker Compose instalado"
    if command -v docker-compose >/dev/null 2>&1; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | sed 's/,//')
        print_pass
        print_info "Versión: $COMPOSE_VERSION"
    else
        print_fail "Docker Compose no está instalado"
    fi

    print_check "Docker daemon corriendo"
    if docker info >/dev/null 2>&1; then
        print_pass
    else
        print_fail "Docker daemon no está corriendo"
    fi

    print_check "Python 3 instalado"
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_pass
        print_info "Versión: $PYTHON_VERSION"
    else
        print_fail "Python 3 no está instalado"
    fi

    print_check "Node.js instalado"
    if command -v node >/dev/null 2>&1; then
        NODE_VERSION=$(node --version)
        print_pass
        print_info "Versión: $NODE_VERSION"
    else
        print_warning "Node.js no está instalado (requerido para desarrollo frontend)"
    fi

    print_check "curl instalado"
    if command -v curl >/dev/null 2>&1; then
        print_pass
    else
        print_fail "curl no está instalado (requerido para health checks)"
    fi
}

# Verificar archivos de configuración
check_configuration_files() {
    print_header "ARCHIVOS DE CONFIGURACIÓN"

    print_check "docker-compose.yml existe"
    if [ -f "docker-compose.yml" ]; then
        print_pass
    else
        print_fail "docker-compose.yml no encontrado"
    fi

    print_check "Archivo .env existe"
    if [ -f ".env" ]; then
        print_pass
    else
        print_warning ".env no encontrado (se puede usar .env.example)"
    fi

    print_check "requirements.txt existe"
    if [ -f "requirements.txt" ]; then
        print_pass
        DEPS_COUNT=$(wc -l < requirements.txt)
        print_info "$DEPS_COUNT dependencias listadas"
    else
        print_fail "requirements.txt no encontrado"
    fi

    print_check "package.json existe (frontend)"
    if [ -f "preventia-dashboard/package.json" ]; then
        print_pass
    else
        print_fail "preventia-dashboard/package.json no encontrado"
    fi

    print_check "Migraciones de BD existen"
    if [ -d "services/data/database/migrations" ] && [ -n "$(ls -A services/data/database/migrations 2>/dev/null)" ]; then
        MIGRATION_COUNT=$(ls -1 services/data/database/migrations/*.sql 2>/dev/null | wc -l)
        print_pass
        print_info "$MIGRATION_COUNT archivos de migración encontrados"
    else
        print_fail "Migraciones de base de datos no encontradas"
    fi
}

# Verificar servicios Docker
check_docker_services() {
    print_header "SERVICIOS DOCKER"

    print_check "Contenedores definidos en docker-compose"
    if docker-compose config >/dev/null 2>&1; then
        SERVICES_COUNT=$(docker-compose config --services | wc -l)
        print_pass
        print_info "$SERVICES_COUNT servicios definidos"
    else
        print_fail "Error en configuración de docker-compose"
        return
    fi

    print_check "Servicios corriendo"
    RUNNING_SERVICES=$(docker-compose ps --services --filter "status=running" 2>/dev/null | wc -l)
    TOTAL_SERVICES=$(docker-compose ps --services 2>/dev/null | wc -l)

    if [ "$RUNNING_SERVICES" -eq "$TOTAL_SERVICES" ] && [ "$TOTAL_SERVICES" -gt 0 ]; then
        print_pass
        print_info "$RUNNING_SERVICES/$TOTAL_SERVICES servicios corriendo"
    elif [ "$RUNNING_SERVICES" -gt 0 ]; then
        print_warning "Solo $RUNNING_SERVICES/$TOTAL_SERVICES servicios corriendo"
    else
        print_fail "Ningún servicio corriendo"
    fi

    # Verificar servicios individuales
    EXPECTED_SERVICES=("postgres" "api" "frontend" "redis")
    for service in "${EXPECTED_SERVICES[@]}"; do
        print_check "Servicio $service"
        if docker-compose ps "$service" 2>/dev/null | grep -q "Up"; then
            print_pass
        else
            print_fail "Servicio $service no está corriendo"
        fi
    done
}

# Verificar conectividad de red
check_network_connectivity() {
    print_header "CONECTIVIDAD DE RED"

    print_check "API responde (puerto 8000)"
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null | grep -q "200"; then
        print_pass
        RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8000/health 2>/dev/null)
        print_info "Tiempo de respuesta: ${RESPONSE_TIME}s"
    else
        print_fail "API no responde en http://localhost:8000/health"
    fi

    print_check "Frontend accesible (puerto 3000)"
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null | grep -q "200"; then
        print_pass
    else
        print_fail "Frontend no accesible en http://localhost:3000"
    fi

    print_check "PostgreSQL conectividad"
    if docker-compose exec -T postgres pg_isready -U preventia >/dev/null 2>&1; then
        print_pass
    else
        print_fail "PostgreSQL no responde"
    fi

    print_check "Redis conectividad"
    if docker-compose exec -T redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
        print_pass
    else
        print_warning "Redis no responde (opcional para desarrollo)"
    fi
}

# Verificar base de datos
check_database() {
    print_header "BASE DE DATOS"

    print_check "Base de datos 'preventia_news' existe"
    if docker-compose exec -T postgres psql -U preventia -d preventia_news -c "SELECT 1;" >/dev/null 2>&1; then
        print_pass
    else
        print_fail "Base de datos no accesible"
        return
    fi

    # Verificar tablas principales
    EXPECTED_TABLES=("news_sources" "articles" "sentiment_analysis" "topic_classification" "users")
    for table in "${EXPECTED_TABLES[@]}"; do
        print_check "Tabla '$table' existe"
        if docker-compose exec -T postgres psql -U preventia -d preventia_news -c "\\dt $table" 2>/dev/null | grep -q "$table"; then
            print_pass
            # Contar registros
            COUNT=$(docker-compose exec -T postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM $table;" 2>/dev/null | tr -d ' \n')
            print_info "$COUNT registros"
        else
            print_fail "Tabla '$table' no existe"
        fi
    done

    print_check "Usuario administrador existe"
    ADMIN_COUNT=$(docker-compose exec -T postgres psql -U preventia -d preventia_news -t -c "SELECT COUNT(*) FROM users WHERE email='admin@preventia.com';" 2>/dev/null | tr -d ' \n')
    if [ "$ADMIN_COUNT" -gt 0 ]; then
        print_pass
        print_info "Usuario admin@preventia.com encontrado"
    else
        print_warning "Usuario administrador no encontrado"
    fi
}

# Verificar endpoints de API
check_api_endpoints() {
    print_header "ENDPOINTS DE API"

    # Lista de endpoints críticos para verificar
    ENDPOINTS=(
        "GET|/health|API Health Check"
        "GET|/docs|API Documentation"
        "GET|/api/sources|News Sources"
        "GET|/api/articles|Articles"
        "GET|/api/analytics/summary|Analytics Summary"
    )

    for endpoint_info in "${ENDPOINTS[@]}"; do
        IFS='|' read -r method path description <<< "$endpoint_info"
        print_check "$description ($method $path)"

        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000$path" 2>/dev/null)

        if [[ "$HTTP_CODE" =~ ^(200|401)$ ]]; then
            print_pass
            if [ "$HTTP_CODE" = "401" ]; then
                print_info "Requiere autenticación (normal)"
            fi
        else
            print_fail "HTTP $HTTP_CODE"
        fi
    done
}

# Verificar logs por errores
check_logs() {
    print_header "ANÁLISIS DE LOGS"

    print_check "Logs de API sin errores críticos"
    ERROR_COUNT=$(docker-compose logs api 2>/dev/null | grep -i "error\|exception\|traceback" | wc -l)
    if [ "$ERROR_COUNT" -lt 5 ]; then
        print_pass
        print_info "$ERROR_COUNT errores encontrados en logs"
    else
        print_warning "$ERROR_COUNT errores encontrados en logs de API"
    fi

    print_check "Logs de PostgreSQL sin errores"
    PG_ERROR_COUNT=$(docker-compose logs postgres 2>/dev/null | grep -i "error\|fatal" | wc -l)
    if [ "$PG_ERROR_COUNT" -lt 3 ]; then
        print_pass
        print_info "$PG_ERROR_COUNT errores en logs de PostgreSQL"
    else
        print_warning "$PG_ERROR_COUNT errores en logs de PostgreSQL"
    fi
}

# Verificar rendimiento básico
check_performance() {
    print_header "RENDIMIENTO BÁSICO"

    print_check "Tiempo de respuesta API < 2s"
    RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:8000/health 2>/dev/null)
    if [ -n "$RESPONSE_TIME" ] && [ "$(echo "$RESPONSE_TIME < 2.0" | bc 2>/dev/null)" = "1" ]; then
        print_pass
        print_info "Tiempo: ${RESPONSE_TIME}s"
    else
        print_warning "Tiempo de respuesta: ${RESPONSE_TIME}s (lento)"
    fi

    print_check "Uso de memoria Docker"
    MEMORY_USAGE=$(docker stats --no-stream --format "table {{.MemUsage}}" 2>/dev/null | tail -n +2 | head -1)
    if [ -n "$MEMORY_USAGE" ]; then
        print_pass
        print_info "Uso de memoria: $MEMORY_USAGE"
    else
        print_warning "No se pudo obtener estadísticas de memoria"
    fi
}

# Generar reporte final
generate_report() {
    echo ""
    echo "=========================================="
    echo -e "${BLUE}🔍 REPORTE DE VALIDACIÓN${NC}"
    echo "=========================================="
    echo ""
    echo -e "Total de verificaciones: ${TOTAL_CHECKS}"
    echo -e "${GREEN}✅ Pasaron: ${PASSED_CHECKS}${NC}"
    echo -e "${YELLOW}⚠️  Advertencias: ${WARNING_CHECKS}${NC}"
    echo -e "${RED}❌ Fallaron: ${FAILED_CHECKS}${NC}"
    echo ""

    # Calcular porcentaje de éxito
    if [ "$TOTAL_CHECKS" -gt 0 ]; then
        SUCCESS_RATE=$(( (PASSED_CHECKS * 100) / TOTAL_CHECKS ))
        echo -e "Tasa de éxito: ${SUCCESS_RATE}%"
    fi

    echo ""

    if [ "$FAILED_CHECKS" -eq 0 ]; then
        echo -e "${GREEN}🎉 ¡INSTALACIÓN VÁLIDA!${NC}"
        echo "El sistema está funcionando correctamente."
        if [ "$WARNING_CHECKS" -gt 0 ]; then
            echo -e "${YELLOW}⚠️  Hay algunas advertencias que puedes revisar.${NC}"
        fi
        exit 0
    elif [ "$FAILED_CHECKS" -lt 5 ]; then
        echo -e "${YELLOW}⚠️  INSTALACIÓN PARCIAL${NC}"
        echo "El sistema funciona pero hay algunos problemas."
        echo "Revisar los errores anteriores."
        exit 1
    else
        echo -e "${RED}❌ INSTALACIÓN FALLIDA${NC}"
        echo "Hay problemas críticos que deben resolverse."
        echo "Revisar la documentación y logs para más detalles."
        exit 2
    fi
}

# Función principal
main() {
    echo -e "${BLUE}🚀 PreventIA News Analytics - Validación de Instalación${NC}"
    echo "Fecha: $(date)"
    echo "Directorio: $(pwd)"
    echo ""

    # Verificar que estamos en el directorio correcto
    if [ ! -f "docker-compose.yml" ]; then
        echo -e "${RED}❌ Error: No se encuentra docker-compose.yml${NC}"
        echo "Ejecutar desde el directorio raíz del proyecto."
        exit 1
    fi

    # Ejecutar todas las verificaciones
    check_system_dependencies
    check_configuration_files
    check_docker_services
    check_network_connectivity
    check_database
    check_api_endpoints
    check_logs
    check_performance

    # Generar reporte final
    generate_report
}

# Manejar interrupciones
trap 'echo -e "\n${YELLOW}⚠️  Validación interrumpida por el usuario${NC}"; exit 130' INT TERM

# Verificar si bc está disponible para cálculos (opcional)
if ! command -v bc >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  'bc' no está instalado. Algunos cálculos serán omitidos.${NC}"
fi

# Ejecutar validación
main "$@"
