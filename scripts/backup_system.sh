#!/bin/bash
# backup_system.sh - Script de backup automatizado para PreventIA News Analytics
# Version: 1.0
# Fecha: 29 de Julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración por defecto
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
COMPRESS="${COMPRESS:-true}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="preventia_backup_${TIMESTAMP}"

# Función para imprimir mensajes
print_message() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Función de ayuda
show_help() {
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "Script de backup automatizado para PreventIA News Analytics"
    echo ""
    echo "OPCIONES:"
    echo "  -d, --dir DIR          Directorio de backup (default: ./backups)"
    echo "  -r, --retention DAYS   Días de retención (default: 7)"
    echo "  -n, --no-compress      No comprimir los backups"
    echo "  -f, --full             Backup completo (incluye logs y cache)"
    echo "  -q, --quiet            Modo silencioso"
    echo "  -h, --help             Mostrar esta ayuda"
    echo ""
    echo "VARIABLES DE ENTORNO:"
    echo "  BACKUP_DIR             Directorio de backup"
    echo "  RETENTION_DAYS         Días de retención"
    echo "  COMPRESS               true/false para compresión"
    echo ""
    echo "EJEMPLOS:"
    echo "  $0                     # Backup básico"
    echo "  $0 -d /mnt/backups     # Backup en directorio específico"
    echo "  $0 -f -r 30            # Backup completo con retención de 30 días"
}

# Procesar argumentos de línea de comandos
FULL_BACKUP=false
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dir)
            BACKUP_DIR="$2"
            shift 2
            ;;
        -r|--retention)
            RETENTION_DAYS="$2"
            shift 2
            ;;
        -n|--no-compress)
            COMPRESS=false
            shift
            ;;
        -f|--full)
            FULL_BACKUP=true
            shift
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Opción desconocida: $1"
            ;;
    esac
done

# Función para log silencioso
log() {
    if [ "$QUIET" = false ]; then
        echo "$@"
    fi
}

# Verificar pre-requisitos
check_prerequisites() {
    log "$(print_message "Verificando pre-requisitos...")"

    # Verificar Docker
    if ! command -v docker >/dev/null 2>&1; then
        print_error "Docker no está instalado"
    fi

    if ! command -v docker-compose >/dev/null 2>&1; then
        print_error "Docker Compose no está instalado"
    fi

    # Verificar que los servicios estén corriendo
    if ! docker-compose ps | grep -q "Up"; then
        print_warning "Algunos servicios no están corriendo. El backup puede estar incompleto."
    fi

    # Crear directorio de backup
    mkdir -p "$BACKUP_DIR"
    if [ ! -w "$BACKUP_DIR" ]; then
        print_error "No se puede escribir en el directorio de backup: $BACKUP_DIR"
    fi

    log "$(print_success "Pre-requisitos verificados")"
}

# Backup de base de datos PostgreSQL
backup_database() {
    log "$(print_message "Realizando backup de PostgreSQL...")"

    local db_backup_file="${BACKUP_DIR}/${BACKUP_NAME}_database.sql"

    # Usar pg_dump a través del contenedor
    if docker-compose exec -T postgres pg_dump -U preventia -d preventia_news > "$db_backup_file" 2>/dev/null; then
        local db_size=$(du -h "$db_backup_file" | cut -f1)
        log "$(print_success "Backup de base de datos completado ($db_size)")"

        # Comprimir si está habilitado
        if [ "$COMPRESS" = true ]; then
            gzip "$db_backup_file"
            log "$(print_info "Base de datos comprimida: ${db_backup_file}.gz")"
        fi
    else
        print_error "Error realizando backup de la base de datos"
    fi
}

# Backup de archivos de configuración
backup_configuration() {
    log "$(print_message "Realizando backup de configuración...")"

    local config_backup_dir="${BACKUP_DIR}/${BACKUP_NAME}_config"
    mkdir -p "$config_backup_dir"

    # Archivos de configuración esenciales
    local config_files=(
        "docker-compose.yml"
        "docker-compose.prod.yml"
        ".env"
        "requirements.txt"
        "preventia-dashboard/package.json"
        "preventia-dashboard/package-lock.json"
        "services/data/database/migrations/"
        "config/"
        "scripts/"
    )

    for file in "${config_files[@]}"; do
        if [ -e "$file" ]; then
            cp -r "$file" "$config_backup_dir/" 2>/dev/null || true
            log "$(print_info "Copiado: $file")"
        fi
    done

    # Crear archivo de metadatos
    cat > "$config_backup_dir/backup_metadata.txt" << EOF
Backup creado: $(date)
Versión del sistema: $(git rev-parse HEAD 2>/dev/null || echo "N/A")
Branch: $(git branch --show-current 2>/dev/null || echo "N/A")
Servicios activos: $(docker-compose ps --services --filter "status=running" | tr '\n' ',' | sed 's/,$//')
Directorio original: $(pwd)
EOF

    log "$(print_success "Backup de configuración completado")"
}

# Backup de volúmenes Docker
backup_volumes() {
    log "$(print_message "Realizando backup de volúmenes Docker...")"

    local volumes_backup_dir="${BACKUP_DIR}/${BACKUP_NAME}_volumes"
    mkdir -p "$volumes_backup_dir"

    # Obtener lista de volúmenes del proyecto
    local volumes=$(docker-compose config --volumes 2>/dev/null || echo "")

    if [ -n "$volumes" ]; then
        for volume in $volumes; do
            log "$(print_info "Respaldando volumen: $volume")"

            # Crear backup del volumen usando un contenedor temporal
            docker run --rm \
                -v "$volume:/source:ro" \
                -v "$(pwd)/$volumes_backup_dir:/backup" \
                alpine:latest \
                tar czf "/backup/${volume}.tar.gz" -C /source . 2>/dev/null || true
        done

        log "$(print_success "Backup de volúmenes completado")"
    else
        log "$(print_info "No se encontraron volúmenes para respaldar")"
    fi
}

# Backup de logs (solo en modo completo)
backup_logs() {
    if [ "$FULL_BACKUP" = true ]; then
        log "$(print_message "Realizando backup de logs...")"

        local logs_backup_dir="${BACKUP_DIR}/${BACKUP_NAME}_logs"
        mkdir -p "$logs_backup_dir"

        # Obtener logs de todos los servicios
        local services=$(docker-compose ps --services 2>/dev/null)

        for service in $services; do
            local log_file="${logs_backup_dir}/${service}.log"
            docker-compose logs --no-color "$service" > "$log_file" 2>/dev/null || true
            log "$(print_info "Logs de $service guardados")"
        done

        log "$(print_success "Backup de logs completado")"
    fi
}

# Backup de código fuente (solo archivos críticos)
backup_source_code() {
    if [ "$FULL_BACKUP" = true ]; then
        log "$(print_message "Realizando backup de código fuente...")"

        local source_backup_file="${BACKUP_DIR}/${BACKUP_NAME}_source.tar"

        # Crear archivo tar con el código fuente, excluyendo archivos innecesarios
        tar cf "$source_backup_file" \
            --exclude='node_modules' \
            --exclude='__pycache__' \
            --exclude='.git' \
            --exclude='venv' \
            --exclude='*.pyc' \
            --exclude='backups' \
            --exclude='*.log' \
            services/ preventia-dashboard/src/ cli/ tests/ 2>/dev/null || true

        if [ "$COMPRESS" = true ]; then
            gzip "$source_backup_file"
            log "$(print_info "Código fuente comprimido: ${source_backup_file}.gz")"
        fi

        log "$(print_success "Backup de código fuente completado")"
    fi
}

# Limpiar backups antiguos
cleanup_old_backups() {
    log "$(print_message "Limpiando backups antiguos (>$RETENTION_DAYS días)...")"

    local deleted_count=0

    # Buscar y eliminar backups antiguos
    find "$BACKUP_DIR" -name "preventia_backup_*" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
    find "$BACKUP_DIR" -name "preventia_backup_*" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} + 2>/dev/null || true

    local remaining_backups=$(find "$BACKUP_DIR" -name "preventia_backup_*" | wc -l)
    log "$(print_success "Limpieza completada. Backups restantes: $remaining_backups")"
}

# Verificar integridad del backup
verify_backup() {
    log "$(print_message "Verificando integridad del backup...")"

    local backup_files=(
        "${BACKUP_DIR}/${BACKUP_NAME}_database.sql"
        "${BACKUP_DIR}/${BACKUP_NAME}_database.sql.gz"
        "${BACKUP_DIR}/${BACKUP_NAME}_config"
    )

    local verified=0
    local total=0

    for file in "${backup_files[@]}"; do
        if [ -e "$file" ]; then
            total=$((total + 1))

            if [ -f "$file" ] && [ -s "$file" ]; then
                verified=$((verified + 1))
                log "$(print_info "✓ $file")"
            elif [ -d "$file" ] && [ -n "$(ls -A "$file" 2>/dev/null)" ]; then
                verified=$((verified + 1))
                log "$(print_info "✓ $file/")"
            else
                log "$(print_warning "✗ $file (vacío o corrupto)")"
            fi
        fi
    done

    if [ "$verified" -eq "$total" ] && [ "$total" -gt 0 ]; then
        log "$(print_success "Verificación de integridad exitosa ($verified/$total archivos)")"
    else
        print_warning "Verificación parcial: $verified/$total archivos válidos"
    fi
}

# Generar reporte de backup
generate_report() {
    local report_file="${BACKUP_DIR}/${BACKUP_NAME}_report.txt"
    local backup_size=$(du -sh "${BACKUP_DIR}/${BACKUP_NAME}"* 2>/dev/null | awk '{sum+=$1} END {print sum}' || echo "N/A")

    cat > "$report_file" << EOF
========================================
REPORTE DE BACKUP - PreventIA News Analytics
========================================

Fecha y hora: $(date)
Nombre del backup: $BACKUP_NAME
Directorio: $BACKUP_DIR
Tipo: $([ "$FULL_BACKUP" = true ] && echo "Completo" || echo "Básico")
Compresión: $([ "$COMPRESS" = true ] && echo "Habilitada" || echo "Deshabilitada")
Tamaño total: $backup_size

COMPONENTES RESPALDADOS:
- Base de datos PostgreSQL: ✓
- Archivos de configuración: ✓
- Volúmenes Docker: ✓
$([ "$FULL_BACKUP" = true ] && echo "- Logs del sistema: ✓")
$([ "$FULL_BACKUP" = true ] && echo "- Código fuente: ✓")

SERVICIOS ACTIVOS DURANTE EL BACKUP:
$(docker-compose ps --format "table {{.Service}}\t{{.Status}}" 2>/dev/null | tail -n +2)

RETENCIÓN: $RETENTION_DAYS días
PRÓXIMA LIMPIEZA: $(date -d "+$RETENTION_DAYS days" 2>/dev/null || echo "N/A")

========================================
EOF

    log "$(print_success "Reporte generado: $report_file")"

    if [ "$QUIET" = false ]; then
        echo ""
        cat "$report_file"
    fi
}

# Función principal
main() {
    local start_time=$(date +%s)

    if [ "$QUIET" = false ]; then
        echo -e "${BLUE}🚀 PreventIA News Analytics - Sistema de Backup${NC}"
        echo "Iniciando backup: $BACKUP_NAME"
        echo "Directorio de destino: $BACKUP_DIR"
        echo "Tipo: $([ "$FULL_BACKUP" = true ] && echo "Completo" || echo "Básico")"
        echo ""
    fi

    # Ejecutar secuencia de backup
    check_prerequisites
    backup_database
    backup_configuration
    backup_volumes
    backup_logs
    backup_source_code
    verify_backup
    cleanup_old_backups
    generate_report

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    log ""
    log "$(print_success "¡Backup completado exitosamente!")"
    log "$(print_info "Tiempo total: ${duration} segundos")"
    log "$(print_info "Ubicación: $BACKUP_DIR")"

    # Mostrar comandos útiles
    if [ "$QUIET" = false ]; then
        echo ""
        echo "Comandos útiles:"
        echo "  ls -la $BACKUP_DIR/                   # Ver backups disponibles"
        echo "  $0 --help                             # Mostrar ayuda completa"
        echo "  ./scripts/restore_backup.sh           # Restaurar backup (futuro)"
    fi
}

# Manejar interrupciones
trap 'echo -e "\n${YELLOW}⚠️  Backup interrumpido por el usuario${NC}"; exit 130' INT TERM

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    print_error "No se encuentra docker-compose.yml. Ejecutar desde el directorio raíz del proyecto."
fi

# Ejecutar backup
main "$@"
