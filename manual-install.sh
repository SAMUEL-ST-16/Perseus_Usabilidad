#!/bin/bash
#
# Script de Instalación Manual - Perseus
# Ejecuta este script en el servidor si cloud-init falla
#

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}==> Instalando Python 3.11...${NC}"
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update -y
apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
update-alternatives --set python3 /usr/bin/python3.11

echo -e "${GREEN}==> Instalando Node.js 18...${NC}"
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs
hash -r
which npm || (echo -e "${RED}ERROR: npm not found${NC}" && exit 1)
/usr/bin/npm install -g @angular/cli@21

echo -e "${GREEN}==> Creando usuario perseus...${NC}"
useradd -m -s /bin/bash perseus || true

echo -e "${GREEN}==> Clonando repositorio desde GitHub...${NC}"
echo "Ingresa la URL de tu repositorio GitHub:"
read -p "URL: " GITHUB_REPO

mkdir -p /opt/perseus
cd /tmp
rm -rf perseus-temp
git clone "$GITHUB_REPO" perseus-temp
cp -r perseus-temp/Backend /opt/perseus/
cp -r perseus-temp/Frontend /opt/perseus/
rm -rf perseus-temp

echo -e "${GREEN}==> Configurando Backend...${NC}"
echo "Ingresa tu HuggingFace Token:"
read -p "Token: " HF_TOKEN

echo "Ingresa tu Groq API Key (o presiona Enter para omitir):"
read -p "Groq Key: " GROQ_KEY

if [ -z "$GROQ_KEY" ]; then
    LLM_PROVIDER="none"
else
    LLM_PROVIDER="groq"
fi

cat > /opt/perseus/Backend/.env << EOF
HUGGINGFACE_TOKEN=$HF_TOKEN
BINARY_MODEL_NAME=SamuelSoto7/PerseusV8_Binario
MULTICLASS_MODEL_NAME=SamuelSoto7/PerseusV2_Multiclass
PROVIDER=$LLM_PROVIDER
GROQ_API_KEY=$GROQ_KEY
GROQ_MODEL_NAME=llama-3.1-8b-instant
OPENAI_API_KEY=
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
RELOAD=False
WORKERS=1
EOF

echo -e "${GREEN}==> Instalando dependencias Python...${NC}"
cd /opt/perseus/Backend
python3.11 -m venv venv
/opt/perseus/Backend/venv/bin/pip install --upgrade pip
/opt/perseus/Backend/venv/bin/pip install -r requirements.txt

echo -e "${GREEN}==> Compilando Frontend...${NC}"
cd /opt/perseus/Frontend
PUBLIC_IP=$(curl -s ifconfig.me)

cat > /opt/perseus/Frontend/src/environments/environment.prod.ts << EOF
export const environment = {
  production: true,
  apiUrl: 'http://$PUBLIC_IP/api/requirements'
};
EOF

/usr/bin/npm install
/usr/bin/npm run build

echo -e "${GREEN}==> Configurando servicio systemd...${NC}"
cat > /etc/systemd/system/perseus-backend.service << 'EOF'
[Unit]
Description=Perseus FastAPI Backend
After=network.target

[Service]
Type=simple
User=perseus
WorkingDirectory=/opt/perseus/Backend
Environment="PATH=/opt/perseus/Backend/venv/bin"
ExecStart=/opt/perseus/Backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

chown -R perseus:perseus /opt/perseus
systemctl daemon-reload
systemctl enable perseus-backend

echo -e "${GREEN}==> Esperando estabilización (60 segundos)...${NC}"
sleep 60

echo -e "${GREEN}==> Iniciando servicio backend...${NC}"
systemctl start perseus-backend

echo -e "${GREEN}==> Configurando Nginx...${NC}"
cat > /etc/nginx/sites-available/perseus << 'EOF'
server {
    listen 80;
    server_name _;
    root /opt/perseus/Frontend/dist/Perseus/browser;
    index index.html;
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_vary on;
    location / {
        try_files $uri $uri/ /index.html;
    }
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host $host;
    }
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

ln -sf /etc/nginx/sites-available/perseus /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl enable nginx

echo -e "${GREEN}==> Configurando firewall...${NC}"
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ INSTALACIÓN COMPLETADA EXITOSAMENTE  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo "Accede a la aplicación en: http://$PUBLIC_IP"
echo "API Docs: http://$PUBLIC_IP/api/requirements/docs"
echo ""
echo "Verificar servicios:"
echo "  systemctl status perseus-backend"
echo "  systemctl status nginx"
echo ""
