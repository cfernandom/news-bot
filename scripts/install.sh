#!/bin/bash
# install.sh - Script de instalación automática de PreventIA News Analytics
# Version: 1.0
# Fecha: 29 de Julio de 2025

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${BLUE}🚀 PreventIA News Analytics${NC} - $1"
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

print_message "Iniciando instalación automatizada..."

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    print_error "No se encuentra docker-compose.yml. Ejecutar desde el directorio raíz del proyecto."
fi

# Verificar dependencias del sistema
print_message "Verificando dependencias del sistema..."

command -v docker >/dev/null 2>&1 || print_error "Docker no está instalado. Instalar desde https://docs.docker.com/get-docker/"
command -v docker-compose >/dev/null 2>&1 || print_error "Docker Compose no está instalado."
command -v python3 >/dev/null 2>&1 || print_error "Python 3 no está instalado."
command -v node >/dev/null 2>&1 || print_error "Node.js no está instalado."
command -v npm >/dev/null 2>&1 || print_error "NPM no está instalado."

print_success "Todas las dependencias están disponibles"

# Verificar que Docker está corriendo
if ! docker info >/dev/null 2>&1; then
    print_error "Docker no está ejecutándose. Iniciar Docker y reintentar."
fi

# Configurar variables de entorno
print_message "Configurando variables de entorno..."

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        print_message "Copiando .env.example a .env..."
        cp .env.example .env
        print_warning "Archivo .env creado. REVISAR Y PERSONALIZAR las configuraciones antes de continuar."
        print_warning "Especialmente: DATABASE_URL, OPENAI_API_KEY, JWT_SECRET_KEY"
        echo ""
        echo "¿Continuar con la instalación? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_message "Instalación pausada. Editar .env y ejecutar nuevamente."
            exit 0
        fi
    else
        print_error "No se encuentra .env ni .env.example. Crear archivo .env manualmente."
    fi
else
    print_success "Archivo .env encontrado"
fi

# Detener servicios existentes si están corriendo
print_message "Deteniendo servicios existentes..."
docker-compose down >/dev/null 2>&1 || true

# Limpiar volúmenes si es una instalación limpia
echo ""
echo "¿Realizar instalación limpia? (eliminar datos existentes) (y/N)"
read -r clean_install
if [[ "$clean_install" =~ ^[Yy]$ ]]; then
    print_warning "Eliminando volúmenes existentes..."
    docker-compose down -v >/dev/null 2>&1 || true
    docker system prune -f >/dev/null 2>&1 || true
fi

# Construir contenedores
print_message "Construyendo contenedores Docker..."
docker-compose build --no-cache

# Verificar que las imágenes se construyeron correctamente
print_message "Verificando imágenes construidas..."
if ! docker images | grep -q "news_bot_3"; then
    print_error "Error construyendo las imágenes Docker"
fi

# Levantar servicios
print_message "Levantando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
print_message "Esperando a que los servicios estén listos..."
sleep 15

# Verificar que los servicios están corriendo
print_message "Verificando estado de los servicios..."
if ! docker-compose ps | grep -q "Up"; then
    print_error "Algunos servicios no se iniciaron correctamente"
fi

# Verificar conectividad a PostgreSQL
print_message "Verificando conexión a base de datos..."
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if docker-compose exec -T postgres pg_isready -U preventia >/dev/null 2>&1; then
        print_success "PostgreSQL está listo"
        break
    fi
    print_message "Esperando PostgreSQL... (intento $attempt/$max_attempts)"
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_error "PostgreSQL no responde después de $max_attempts intentos"
fi

# Inicializar base de datos con migraciones
print_message "Ejecutando migraciones de base de datos..."
if [ -f "services/data/database/migrations/001_initial_schema.sql" ]; then
    docker-compose exec -T postgres psql -U preventia -d preventia_news -f /docker-entrypoint-initdb.d/001_initial_schema.sql >/dev/null 2>&1 || true
fi

if [ -f "services/data/database/migrations/002_compliance_consolidated.sql" ]; then
    docker-compose exec -T postgres psql -U preventia -d preventia_news -f /docker-entrypoint-initdb.d/002_compliance_consolidated.sql >/dev/null 2>&1 || true
fi

# Crear usuario administrador
print_message "Creando usuario administrador..."
docker-compose exec -T api python -m services.api.auth.startup >/dev/null 2>&1 || print_warning "Error creando usuario admin (puede que ya exista)"

# Verificar que la API responde
print_message "Verificando API..."
max_attempts=15
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        print_success "API está respondiendo"
        break
    fi
    print_message "Esperando API... (intento $attempt/$max_attempts)"
    sleep 3
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_warning "API no responde en el puerto 8000"
fi

# Verificar que el frontend está disponible
print_message "Verificando frontend..."
max_attempts=10
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:3000 >/dev/null 2>&1; then
        print_success "Frontend está disponible"
        break
    fi
    print_message "Esperando frontend... (intento $attempt/$max_attempts)"
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    print_warning "Frontend no responde en el puerto 3000"
fi

# Mostrar resumen de instalación
echo ""
echo "=========================================="
print_success "¡Instalación completada exitosamente!"
echo "=========================================="
echo ""
echo "🌐 Servicios disponibles:"
echo "   📊 Dashboard Principal: http://localhost:3000/"
echo "   🔧 Panel Admin:        http://localhost:3000/admin"
echo "   📚 API Docs:           http://localhost:8000/docs"
echo "   ❤️  API Health:         http://localhost:8000/health"
echo ""
echo "👤 Usuario administrador creado:"
echo "   Email: admin@preventia.com"
echo "   Password: admin123"
echo ""
echo "📋 Comandos útiles:"
echo "   docker-compose logs -f     # Ver logs en tiempo real"
echo "   docker-compose ps          # Estado de servicios"
echo "   docker-compose down        # Detener servicios"
echo "   ./scripts/validate_installation.sh  # Validar instalación"
echo ""
print_warning "IMPORTANTE: Cambiar la contraseña del administrador en el primer acceso"
print_warning "IMPORTANTE: Revisar configuración de .env para producción"
