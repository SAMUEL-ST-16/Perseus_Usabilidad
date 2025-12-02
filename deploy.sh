#!/bin/bash
#
# Script de Despliegue Automatizado - Perseus
# Para Ubuntu 22.04 LTS en DigitalOcean Droplet
#
# Uso:
#   1. Crea un droplet en DigitalOcean (Ubuntu 22.04)
#   2. Copia este script al servidor
#   3. Ejecuta: chmod +x deploy.sh && sudo ./deploy.sh
#
# El script instalará y configurará automáticamente:
#   - Python 3.11 + Backend FastAPI
#   - Node.js + Frontend Angular (compilado)
#   - Nginx como reverse proxy
#   - Servicios systemd para auto-inicio
#   - Firewall (ufw)
#   - SSL con Let's Encrypt (opcional)
#

set -e  # Detener si hay errores

echo "=================================================="
echo "  🚀 Perseus - Despliegue Automatizado"
echo "=================================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables de configuración
PROJECT_NAME="perseus"
PROJECT_DIR="/opt/$PROJECT_NAME"
BACKEND_DIR="$PROJECT_DIR/Backend"
FRONTEND_DIR="$PROJECT_DIR/Frontend"
REPO_URL=""  # Se pedirá al usuario

# Usuario del sistema (no root)
APP_USER="perseus"

# ==================================================
# PASO 1: Actualizar sistema
# ==================================================
echo -e "${GREEN}[1/10] Actualizando sistema...${NC}"
apt-get update -y
apt-get upgrade -y

# ==================================================
# PASO 2: Instalar dependencias del sistema
# ==================================================
echo -e "${GREEN}[2/10] Instalando dependencias del sistema...${NC}"
apt-get install -y \
    software-properties-common \
    build-essential \
    curl \
    wget \
    git \
    nginx \
    ufw \
    certbot \
    python3-certbot-nginx \
    supervisor

# ==================================================
# PASO 3: Instalar Python 3.11
# ==================================================
echo -e "${GREEN}[3/10] Instalando Python 3.11...${NC}"
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update -y
apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip

# Hacer Python 3.11 el predeterminado
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
update-alternatives --set python3 /usr/bin/python3.11

# ==================================================
# PASO 4: Instalar Node.js 18.x
# ==================================================
echo -e "${GREEN}[4/10] Instalando Node.js 18...${NC}"
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Instalar Angular CLI globalmente
npm install -g @angular/cli@21

# ==================================================
# PASO 5: Crear usuario del sistema
# ==================================================
echo -e "${GREEN}[5/10] Creando usuario del sistema...${NC}"
if ! id "$APP_USER" &>/dev/null; then
    useradd -m -s /bin/bash $APP_USER
    echo "Usuario $APP_USER creado"
else
    echo "Usuario $APP_USER ya existe"
fi

# ==================================================
# PASO 6: Clonar repositorio
# ==================================================
echo -e "${GREEN}[6/10] Clonando repositorio...${NC}"

# Pedir URL del repositorio si no está configurada
if [ -z "$REPO_URL" ]; then
    echo -e "${YELLOW}Ingresa la URL de tu repositorio de GitHub:${NC}"
    read -p "URL del repo: " REPO_URL
fi

# Eliminar directorio si existe
if [ -d "$PROJECT_DIR" ]; then
    echo "Eliminando instalación anterior..."
    rm -rf $PROJECT_DIR
fi

# Clonar repo
mkdir -p $PROJECT_DIR
cd /tmp
git clone $REPO_URL perseus-temp

# Copiar Backend y Frontend
cp -r perseus-temp/Backend $PROJECT_DIR/
cp -r perseus-temp/Frontend $PROJECT_DIR/

# Limpiar
rm -rf perseus-temp

# ==================================================
# PASO 7: Configurar Backend
# ==================================================
echo -e "${GREEN}[7/10] Configurando Backend...${NC}"

cd $BACKEND_DIR

# Crear .env interactivo
echo -e "${YELLOW}Configurando variables de entorno del Backend...${NC}"
echo ""

# Verificar si existe .env.example
if [ ! -f ".env.example" ]; then
    echo -e "${RED}ERROR: .env.example no encontrado en Backend/${NC}"
    exit 1
fi

# Pedir credenciales al usuario
echo "Necesito algunas credenciales. Presiona Enter para usar valores por defecto."
echo ""

read -p "HuggingFace Token (obligatorio): " HF_TOKEN
read -p "Groq API Key (recomendado, presiona Enter para omitir): " GROQ_KEY
read -p "OpenAI API Key (opcional, presiona Enter para omitir): " OPENAI_KEY
read -p "Nombre modelo binario [SamuelSoto7/PerseusV8_Binario]: " BINARY_MODEL
read -p "Nombre modelo multiclase [SamuelSoto7/PerseusV2_Multiclass]: " MULTICLASS_MODEL
read -p "Tu dominio (ej: perseus.com, presiona Enter para usar IP): " DOMAIN

# Valores por defecto
BINARY_MODEL=${BINARY_MODEL:-SamuelSoto7/PerseusV8_Binario}
MULTICLASS_MODEL=${MULTICLASS_MODEL:-SamuelSoto7/PerseusV2_Multiclass}

# Detectar IP pública del droplet
PUBLIC_IP=$(curl -s ifconfig.me)

# Configurar CORS según dominio o IP
if [ -z "$DOMAIN" ]; then
    CORS_ORIGINS="[\"http://$PUBLIC_IP\",\"http://www.$PUBLIC_IP\"]"
    SERVER_NAME=$PUBLIC_IP
else
    CORS_ORIGINS="[\"http://$DOMAIN\",\"http://www.$DOMAIN\",\"https://$DOMAIN\",\"https://www.$DOMAIN\"]"
    SERVER_NAME=$DOMAIN
fi

# Crear archivo .env
cat > .env <<EOF
# ========== HuggingFace Configuration ==========
HUGGINGFACE_API_TOKEN=$HF_TOKEN

# ========== Model Configuration ==========
BINARY_MODEL_NAME=$BINARY_MODEL
MULTICLASS_MODEL_NAME=$MULTICLASS_MODEL
MODEL_DEVICE=-1

# ========== API Configuration ==========
API_TITLE=Perseus API
API_DESCRIPTION=API for extracting and classifying requirements using BERT models
API_VERSION=1.0.0
API_HOST=0.0.0.0
API_PORT=8000

# ========== CORS Configuration ==========
CORS_ORIGINS=$CORS_ORIGINS

# ========== Logging Configuration ==========
LOG_LEVEL=INFO

# ========== Validation Limits ==========
MAX_TEXT_LENGTH=10000
MIN_TEXT_LENGTH=1

# ========== Model Loading ==========
LAZY_MODEL_LOADING=true

# ========== LLM Provider Configuration ==========
EOF

# Agregar configuración de LLM según lo que el usuario ingresó
if [ ! -z "$GROQ_KEY" ]; then
    echo "LLM_PROVIDER=groq" >> .env
    echo "GROQ_API_KEY=$GROQ_KEY" >> .env
    echo "GROQ_MODEL=llama-3.1-70b-versatile" >> .env
elif [ ! -z "$OPENAI_KEY" ]; then
    echo "LLM_PROVIDER=openai" >> .env
    echo "OPENAI_API_KEY=$OPENAI_KEY" >> .env
    echo "OPENAI_MODEL=gpt-4o-mini" >> .env
else
    echo "LLM_PROVIDER=none" >> .env
fi

# Agregar configuración de Google Play
cat >> .env <<EOF

# ========== Google Play Scraper Configuration ==========
PLAYSTORE_MIN_WORDS=15
PLAYSTORE_MIN_RATING=2
PLAYSTORE_MAX_RATING=3
PLAYSTORE_LANG=es
PLAYSTORE_COUNTRY=pe
PLAYSTORE_TARGET_REQUIREMENTS=30
PLAYSTORE_BATCH_SIZE=50
PLAYSTORE_MAX_TOTAL_COMMENTS=500
EOF

echo -e "${GREEN}✓ Archivo .env creado${NC}"

# Crear entorno virtual e instalar dependencias
echo "Instalando dependencias de Python..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

echo -e "${GREEN}✓ Backend configurado${NC}"

# ==================================================
# PASO 8: Compilar Frontend
# ==================================================
echo -e "${GREEN}[8/10] Compilando Frontend...${NC}"

cd $FRONTEND_DIR

# Actualizar environment.prod.ts con la URL correcta
if [ ! -z "$DOMAIN" ]; then
    API_URL="https://$DOMAIN/api/requirements"
else
    API_URL="http://$PUBLIC_IP/api/requirements"
fi

cat > src/environments/environment.prod.ts <<EOF
// Ambiente de producción
export const environment = {
  production: true,
  apiUrl: '$API_URL'
};
EOF

echo -e "${GREEN}✓ Environment configurado con API: $API_URL${NC}"

# Instalar dependencias y compilar
echo "Instalando dependencias de Node.js..."
npm install

echo "Compilando aplicación Angular..."
npm run build

echo -e "${GREEN}✓ Frontend compilado${NC}"

# ==================================================
# PASO 9: Configurar servicios systemd
# ==================================================
echo -e "${GREEN}[9/10] Configurando servicios systemd...${NC}"

# Servicio para Backend
cat > /etc/systemd/system/perseus-backend.service <<EOF
[Unit]
Description=Perseus FastAPI Backend
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Cambiar permisos del proyecto
chown -R $APP_USER:$APP_USER $PROJECT_DIR

# Habilitar e iniciar servicio de backend
systemctl daemon-reload
systemctl enable perseus-backend
systemctl start perseus-backend

echo -e "${GREEN}✓ Servicio de backend iniciado${NC}"

# Configurar Nginx
cat > /etc/nginx/sites-available/perseus <<EOF
server {
    listen 80;
    server_name $SERVER_NAME;

    # Frontend - Archivos estáticos de Angular
    root $FRONTEND_DIR/dist/Perseus/browser;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;

    # Frontend routes - Angular routing
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API - Proxy reverso a FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # Timeouts para modelos ML (pueden tardar)
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host \$host;
    }

    # Cache para assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

# Habilitar sitio
ln -sf /etc/nginx/sites-available/perseus /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Probar configuración de Nginx
nginx -t

# Reiniciar Nginx
systemctl restart nginx
systemctl enable nginx

echo -e "${GREEN}✓ Nginx configurado${NC}"

# ==================================================
# PASO 10: Configurar Firewall
# ==================================================
echo -e "${GREEN}[10/10] Configurando firewall...${NC}"

ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'

echo -e "${GREEN}✓ Firewall configurado${NC}"

# ==================================================
# RESUMEN FINAL
# ==================================================
echo ""
echo "=================================================="
echo -e "${GREEN}  ✅ DESPLIEGUE COMPLETADO EXITOSAMENTE${NC}"
echo "=================================================="
echo ""
echo "📋 INFORMACIÓN DEL SERVIDOR:"
echo "  - IP Pública: $PUBLIC_IP"
if [ ! -z "$DOMAIN" ]; then
    echo "  - Dominio: $DOMAIN"
fi
echo ""
echo "🌐 URLS DE ACCESO:"
if [ ! -z "$DOMAIN" ]; then
    echo "  - Frontend: http://$DOMAIN"
    echo "  - Backend API Docs: http://$DOMAIN/api/requirements/docs"
    echo "  - Health Check: http://$DOMAIN/health"
else
    echo "  - Frontend: http://$PUBLIC_IP"
    echo "  - Backend API Docs: http://$PUBLIC_IP/api/requirements/docs"
    echo "  - Health Check: http://$PUBLIC_IP/health"
fi
echo ""
echo "🔧 COMANDOS ÚTILES:"
echo "  - Ver logs del backend: sudo journalctl -u perseus-backend -f"
echo "  - Reiniciar backend: sudo systemctl restart perseus-backend"
echo "  - Ver status: sudo systemctl status perseus-backend"
echo "  - Reiniciar Nginx: sudo systemctl restart nginx"
echo ""
echo "🔒 CONFIGURAR SSL (OPCIONAL):"
if [ ! -z "$DOMAIN" ]; then
    echo "  Ejecuta: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
else
    echo "  1. Configura un dominio apuntando a $PUBLIC_IP"
    echo "  2. Ejecuta: sudo certbot --nginx -d tu-dominio.com"
fi
echo ""
echo "📝 ARCHIVOS IMPORTANTES:"
echo "  - Backend .env: $BACKEND_DIR/.env"
echo "  - Nginx config: /etc/nginx/sites-available/perseus"
echo "  - Systemd service: /etc/systemd/system/perseus-backend.service"
echo ""
echo "=================================================="
echo -e "${YELLOW}  Prueba tu aplicación abriendo la URL en tu navegador${NC}"
echo "=================================================="
echo ""
