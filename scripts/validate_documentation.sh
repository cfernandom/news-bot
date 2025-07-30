#!/bin/bash
# validate_documentation.sh - Script de validación continua de documentación
# Version: 1.0
# Fecha: 29 de Julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
DOCS_DIR="manual"
SCRIPTS_DIR="scripts"
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0
VALIDATION_LOG="/tmp/docs_validation.log"

# Función para imprimir mensajes
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

print_check() {
    echo -n "  📋 Verificando $1... "
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

# Función de ayuda
show_help() {
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "Script de validación continua de documentación para PreventIA"
    echo ""
    echo "OPCIONES:"
    echo "  -q, --quiet           Modo silencioso"
    echo "  -f, --fix             Intentar corregir errores automáticamente"
    echo "  -d, --docs-dir DIR    Directorio de documentación (default: manual)"
    echo "  -o, --output FILE     Archivo de salida del reporte"
    echo "  -h, --help            Mostrar esta ayuda"
    echo ""
    echo "EJEMPLOS:"
    echo "  $0                    # Validación básica"
    echo "  $0 -f                 # Validación con corrección automática"
    echo "  $0 -q -o report.txt   # Modo silencioso con reporte"
}

# Procesar argumentos
QUIET=false
FIX_ERRORS=false
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quiet)
            QUIET=true
            shift
            ;;
        -f|--fix)
            FIX_ERRORS=true
            shift
            ;;
        -d|--docs-dir)
            DOCS_DIR="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Opción desconocida: $1"
            exit 1
            ;;
    esac
done

# Log function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$VALIDATION_LOG"
    if [ "$QUIET" = false ]; then
        echo "$1"
    fi
}

# Verificar estructura de documentación
check_documentation_structure() {
    print_header "ESTRUCTURA DE DOCUMENTACIÓN"

    # Archivos requeridos
    local required_files=(
        "README.md"
        "01_DescripcionSistema.md"
        "02_DisenoTecnico.md"
        "03_InstalacionConfiguracion.md"
        "04_Despliegue.md"
        "05_ResolucionProblemas.md"
    )

    for file in "${required_files[@]}"; do
        print_check "archivo $file existe"
        if [ -f "$DOCS_DIR/$file" ]; then
            print_pass

            # Verificar que no esté vacío
            if [ ! -s "$DOCS_DIR/$file" ]; then
                print_warning "Archivo $file está vacío"
            fi
        else
            print_fail "Archivo requerido $file no encontrado"
        fi
    done

    # Verificar directorios opcionales
    print_check "directorio de assets"
    if [ -d "$DOCS_DIR/assets" ]; then
        print_pass
        local assets_count=$(find "$DOCS_DIR/assets" -type f | wc -l)
        print_info "$assets_count archivos en assets/"
    else
        print_warning "Directorio assets/ no encontrado"
    fi
}

# Verificar enlaces internos
check_internal_links() {
    print_header "ENLACES INTERNOS"

    local broken_links=0

    for doc_file in "$DOCS_DIR"/*.md; do
        if [ -f "$doc_file" ]; then
            local filename=$(basename "$doc_file")
            print_check "enlaces en $filename"

            # Buscar enlaces markdown [texto](archivo)
            local internal_links=$(grep -o '\[.*\](.*\.md)' "$doc_file" 2>/dev/null || true)

            if [ -n "$internal_links" ]; then
                local links_count=0
                local broken_count=0

                while IFS= read -r link; do
                    if [ -n "$link" ]; then
                        links_count=$((links_count + 1))
                        local target_file=$(echo "$link" | sed 's/.*(\(.*\))/\1/')

                        if [ ! -f "$DOCS_DIR/$target_file" ]; then
                            broken_count=$((broken_count + 1))
                            log_message "Enlace roto en $filename: $target_file"
                        fi
                    fi
                done <<< "$internal_links"

                if [ "$broken_count" -eq 0 ]; then
                    print_pass
                    print_info "$links_count enlaces verificados"
                else
                    print_fail "$broken_count enlaces rotos de $links_count"
                    broken_links=$((broken_links + broken_count))
                fi
            else
                print_pass
                print_info "Sin enlaces internos"
            fi
        fi
    done

    if [ "$broken_links" -gt 0 ] && [ "$FIX_ERRORS" = true ]; then
        print_info "Modo de corrección no implementado para enlaces rotos"
    fi
}

# Verificar comandos documentados
check_documented_commands() {
    print_header "COMANDOS DOCUMENTADOS"

    local total_commands=0
    local working_commands=0

    for doc_file in "$DOCS_DIR"/*.md; do
        if [ -f "$doc_file" ]; then
            local filename=$(basename "$doc_file")
            print_check "comandos en $filename"

            # Extraer bloques de código bash
            local bash_commands=$(awk '/```bash/,/```/ {if (!/```/) print}' "$doc_file" 2>/dev/null || true)

            if [ -n "$bash_commands" ]; then
                local commands_in_file=0
                local working_in_file=0

                # Contar líneas que parecen comandos (empiezan con $ o son comandos conocidos)
                while IFS= read -r line; do
                    if [[ "$line" =~ ^[[:space:]]*\$[[:space:]]+ ]] || \
                       [[ "$line" =~ ^[[:space:]]*(docker|python|npm|curl|git)[[:space:]] ]]; then
                        commands_in_file=$((commands_in_file + 1))

                        # Extraer el comando sin el prompt $
                        local clean_command=$(echo "$line" | sed 's/^[[:space:]]*\$[[:space:]]*//' | sed 's/^[[:space:]]*//')

                        # Verificar algunos comandos básicos
                        if [[ "$clean_command" =~ ^(docker --version|python --version|node --version) ]]; then
                            if command -v $(echo "$clean_command" | cut -d' ' -f1) >/dev/null 2>&1; then
                                working_in_file=$((working_in_file + 1))
                            fi
                        else
                            # Para otros comandos, solo verificar que el comando base existe
                            local base_cmd=$(echo "$clean_command" | cut -d' ' -f1)
                            if command -v "$base_cmd" >/dev/null 2>&1 || [ -f "$base_cmd" ] || [[ "$base_cmd" =~ ^\./ ]]; then
                                working_in_file=$((working_in_file + 1))
                            fi
                        fi
                    fi
                done <<< "$bash_commands"

                total_commands=$((total_commands + commands_in_file))
                working_commands=$((working_commands + working_in_file))

                if [ "$commands_in_file" -gt 0 ]; then
                    if [ "$working_in_file" -eq "$commands_in_file" ]; then
                        print_pass
                    else
                        print_warning "$working_in_file/$commands_in_file comandos verificados"
                    fi
                    print_info "$commands_in_file comandos encontrados"
                else
                    print_pass
                    print_info "Sin comandos bash"
                fi
            else
                print_pass
                print_info "Sin bloques bash"
            fi
        fi
    done

    log_message "Total comandos verificados: $working_commands/$total_commands"
}

# Verificar scripts mencionados en documentación
check_referenced_scripts() {
    print_header "SCRIPTS REFERENCIADOS"

    local missing_scripts=0

    for doc_file in "$DOCS_DIR"/*.md; do
        if [ -f "$doc_file" ]; then
            local filename=$(basename "$doc_file")
            print_check "scripts en $filename"

            # Buscar referencias a archivos .sh y .py en scripts/
            local script_refs=$(grep -o 'scripts/[a-zA-Z0-9_.-]*\.\(sh\|py\)' "$doc_file" 2>/dev/null || true)

            if [ -n "$script_refs" ]; then
                local refs_count=0
                local missing_count=0

                while IFS= read -r script_ref; do
                    if [ -n "$script_ref" ]; then
                        refs_count=$((refs_count + 1))

                        if [ ! -f "$script_ref" ]; then
                            missing_count=$((missing_count + 1))
                            log_message "Script faltante referenciado en $filename: $script_ref"
                        fi
                    fi
                done <<< "$script_refs"

                missing_scripts=$((missing_scripts + missing_count))

                if [ "$missing_count" -eq 0 ]; then
                    print_pass
                    print_info "$refs_count scripts verificados"
                else
                    print_fail "$missing_count scripts faltantes de $refs_count"
                fi
            else
                print_pass
                print_info "Sin referencias a scripts"
            fi
        fi
    done
}

# Verificar consistencia de versiones
check_version_consistency() {
    print_header "CONSISTENCIA DE VERSIONES"

    # Verificar versiones mencionadas en documentación vs archivos reales
    print_check "versiones de Python"
    local doc_python_version=$(grep -r "python.*version\|Python.*[0-9]\+\.[0-9]\+" "$DOCS_DIR/" | head -1 | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1)
    local actual_python_version=$(python3 --version 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" || echo "N/A")

    if [ "$doc_python_version" = "$actual_python_version" ] || [ -z "$doc_python_version" ]; then
        print_pass
        print_info "Documentado: $doc_python_version, Actual: $actual_python_version"
    else
        print_warning "Versión documentada ($doc_python_version) ≠ actual ($actual_python_version)"
    fi

    print_check "versiones de Node.js"
    local doc_node_version=$(grep -r "node.*version\|Node.*[0-9]\+\.[0-9]\+" "$DOCS_DIR/" | head -1 | grep -o "v\?[0-9]\+\.[0-9]\+\.[0-9]\+" | head -1)
    local actual_node_version=$(node --version 2>/dev/null | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" || echo "N/A")

    if [ "$doc_node_version" = "$actual_node_version" ] || [ -z "$doc_node_version" ]; then
        print_pass
        print_info "Documentado: $doc_node_version, Actual: $actual_node_version"
    else
        print_warning "Versión documentada ($doc_node_version) ≠ actual ($actual_node_version)"
    fi

    # Verificar package.json vs documentación
    print_check "dependencias de frontend"
    if [ -f "preventia-dashboard/package.json" ]; then
        local package_deps=$(jq -r '.dependencies | keys[]' preventia-dashboard/package.json 2>/dev/null | wc -l || echo "0")
        print_pass
        print_info "$package_deps dependencias en package.json"
    else
        print_fail "package.json no encontrado"
    fi
}

# Verificar ejemplos de código
check_code_examples() {
    print_header "EJEMPLOS DE CÓDIGO"

    for doc_file in "$DOCS_DIR"/*.md; do
        if [ -f "$doc_file" ]; then
            local filename=$(basename "$doc_file")
            print_check "sintaxis en $filename"

            # Contar bloques de código
            local code_blocks=$(grep -c '```' "$doc_file" 2>/dev/null || echo "0")
            local code_blocks_pairs=$((code_blocks / 2))

            # Verificar que los bloques estén balanceados
            if [ $((code_blocks % 2)) -eq 0 ]; then
                print_pass
                print_info "$code_blocks_pairs bloques de código"
            else
                print_fail "Bloques de código desbalanceados"
            fi

            # Verificar sintaxis básica de algunos lenguajes
            local syntax_errors=0

            # Extraer y verificar bloques JSON
            if grep -q '```json' "$doc_file"; then
                local json_blocks=$(awk '/```json/,/```/ {if (!/```/) print}' "$doc_file")
                if [ -n "$json_blocks" ]; then
                    if ! echo "$json_blocks" | jq . >/dev/null 2>&1; then
                        syntax_errors=$((syntax_errors + 1))
                        log_message "Error de sintaxis JSON en $filename"
                    fi
                fi
            fi

            if [ "$syntax_errors" -gt 0 ]; then
                print_warning "$syntax_errors errores de sintaxis encontrados"
            fi
        fi
    done
}

# Verificar actualización de documentación
check_documentation_freshness() {
    print_header "ACTUALIZACIÓN DE DOCUMENTACIÓN"

    local old_files=0
    local days_threshold=30

    for doc_file in "$DOCS_DIR"/*.md; do
        if [ -f "$doc_file" ]; then
            local filename=$(basename "$doc_file")
            print_check "actualización de $filename"

            local file_age_days=$(( ($(date +%s) - $(stat -c %Y "$doc_file")) / 86400 ))

            if [ "$file_age_days" -lt "$days_threshold" ]; then
                print_pass
                print_info "Actualizado hace $file_age_days días"
            else
                print_warning "No actualizado en $file_age_days días"
                old_files=$((old_files + 1))
            fi
        fi
    done

    if [ "$old_files" -gt 0 ]; then
        log_message "$old_files archivos no actualizados en >$days_threshold días"
    fi
}

# Generar reporte de validación
generate_report() {
    local report_content=""

    report_content+="========================================\n"
    report_content+="REPORTE DE VALIDACIÓN DE DOCUMENTACIÓN\n"
    report_content+="========================================\n\n"
    report_content+="Fecha: $(date)\n"
    report_content+="Directorio: $DOCS_DIR\n\n"
    report_content+="RESUMEN:\n"
    report_content+="- Total verificaciones: $TOTAL_CHECKS\n"
    report_content+="- Pasaron: $PASSED_CHECKS\n"
    report_content+="- Advertencias: $WARNING_CHECKS\n"
    report_content+="- Fallaron: $FAILED_CHECKS\n\n"

    local success_rate=0
    if [ "$TOTAL_CHECKS" -gt 0 ]; then
        success_rate=$(( (PASSED_CHECKS * 100) / TOTAL_CHECKS ))
    fi
    report_content+="Tasa de éxito: ${success_rate}%\n\n"

    if [ -f "$VALIDATION_LOG" ]; then
        report_content+="DETALLES DE PROBLEMAS:\n"
        report_content+="$(cat "$VALIDATION_LOG")\n"
    fi

    report_content+="========================================\n"

    if [ -n "$OUTPUT_FILE" ]; then
        echo -e "$report_content" > "$OUTPUT_FILE"
        log_message "Reporte guardado en: $OUTPUT_FILE"
    fi

    if [ "$QUIET" = false ]; then
        echo ""
        echo "=========================================="
        echo -e "${BLUE}📋 REPORTE DE VALIDACIÓN${NC}"
        echo "=========================================="
        echo ""
        echo -e "Total verificaciones: $TOTAL_CHECKS"
        echo -e "${GREEN}✅ Pasaron: $PASSED_CHECKS${NC}"
        echo -e "${YELLOW}⚠️  Advertencias: $WARNING_CHECKS${NC}"
        echo -e "${RED}❌ Fallaron: $FAILED_CHECKS${NC}"
        echo ""
        echo -e "Tasa de éxito: ${success_rate}%"
        echo ""

        if [ "$FAILED_CHECKS" -eq 0 ] && [ "$WARNING_CHECKS" -lt 3 ]; then
            echo -e "${GREEN}🎉 ¡DOCUMENTACIÓN EN BUEN ESTADO!${NC}"
        elif [ "$FAILED_CHECKS" -lt 3 ]; then
            echo -e "${YELLOW}⚠️  DOCUMENTACIÓN NECESITA ATENCIÓN${NC}"
        else
            echo -e "${RED}❌ DOCUMENTACIÓN REQUIERE CORRECCIONES${NC}"
        fi
    fi
}

# Función principal
main() {
    if [ "$QUIET" = false ]; then
        echo -e "${BLUE}🚀 PreventIA News Analytics - Validación de Documentación${NC}"
        echo "Fecha: $(date)"
        echo "Directorio: $DOCS_DIR"
        echo ""
    fi

    # Limpiar log anterior
    > "$VALIDATION_LOG"

    # Verificar que el directorio de documentación existe
    if [ ! -d "$DOCS_DIR" ]; then
        print_fail "Directorio de documentación no encontrado: $DOCS_DIR"
        exit 1
    fi

    # Ejecutar todas las verificaciones
    check_documentation_structure
    check_internal_links
    check_documented_commands
    check_referenced_scripts
    check_version_consistency
    check_code_examples
    check_documentation_freshness

    # Generar reporte
    generate_report

    # Determinar código de salida
    if [ "$FAILED_CHECKS" -eq 0 ] && [ "$WARNING_CHECKS" -lt 5 ]; then
        exit 0
    elif [ "$FAILED_CHECKS" -lt 3 ]; then
        exit 1
    else
        exit 2
    fi
}

# Verificar dependencias
if ! command -v jq >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  'jq' no está instalado. Algunas verificaciones serán omitidas.${NC}"
fi

# Ejecutar validación
main "$@"
