# Guía de Despliegue - Perseus

Esta guía completa te ayudará a desplegar tu aplicación **Perseus** en producción.

## 📋 Índice

1. [Prerequisitos](#prerequisitos)
2. [Configuración del Backend](#configuración-del-backend)
3. [Configuración del Frontend](#configuración-del-frontend)
4. [Opciones de Despliegue](#opciones-de-despliegue)
5. [Despliegue con Docker](#despliegue-con-docker)
6. [Despliegue en Cloud](#despliegue-en-cloud)
7. [Configuración de Dominio y SSL](#configuración-de-dominio-y-ssl)
8. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)

---

## 🔧 Prerequisitos

### Software Necesario

- **Python 3.11+** (para backend)
- **Node.js 18+** y **npm 11+** (para frontend)
- **Git** (para control de versiones)
- **Docker y Docker Compose** (opcional, recomendado)

### Cuentas y APIs Requeridas

✅ **API de Modelos LLM** (elige una):
- **Groq API** (RECOMENDADO - GRATUITO): https://console.groq.com/
- **OpenAI API** (de pago): https://platform.openai.com/

✅ **HuggingFace** (para modelos BERT):
- Token de acceso: https://huggingface.co/settings/tokens
- Tus modelos deben estar publicados o accesibles

✅ **Servidor/Hosting** (elige uno):
- VPS (DigitalOcean, Linode, AWS EC2, etc.)
- Plataforma serverless (Railway, Render, Fly.io)
- Servidor propio

---

## 🔙 Configuración del Backend

### 1. Clonar y configurar

```bash
cd Backend
```

### 2. Crear y configurar archivo .env

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales reales:

```env
# ========== Configuración de Modelos HuggingFace ==========
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
BINARY_MODEL_NAME=tu-usuario/modelo-binario-bert
MULTICLASS_MODEL_NAME=tu-usuario/modelo-multiclase-bert

# ========== Configuración de LLM Provider ==========
# Opciones: "groq" (gratuito) o "openai" (de pago)
LLM_PROVIDER=groq

# Si usas Groq (recomendado - gratuito)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.1-70b-versatile

# Si usas OpenAI (de pago)
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
# OPENAI_MODEL=gpt-4o-mini

# ========== Configuración de API ==========
API_TITLE=Perseus API
API_VERSION=1.0.0
ENVIRONMENT=production
DEBUG=False

# ========== CORS (dominios permitidos) ==========
# En desarrollo: http://localhost:4200
# En producción: https://tu-dominio.com
ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# ========== Configuración de Logging ==========
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 3. Instalar dependencias

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Verificar instalación

```bash
python -m app.main
# Debería iniciar en http://localhost:8000
```

Prueba en tu navegador:
- API Docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/requirements/health

---

## 🎨 Configuración del Frontend

### 1. Instalar dependencias

```bash
cd Frontend
npm install
```

### 2. Configurar ambiente de producción

Edita `src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.tu-dominio.com/api/requirements'
  // Cambiar por la URL real de tu backend en producción
};
```

### 3. Compilar para producción

```bash
npm run build
```

Esto generará los archivos estáticos en la carpeta `dist/Perseus/browser/`.

### 4. Probar build localmente (opcional)

```bash
# Instalar servidor estático
npm install -g serve

# Servir archivos de producción
serve -s dist/Perseus/browser -l 4200
```

---

## 🚀 Opciones de Despliegue

### Opción 1: Docker (Recomendado)

**Ventajas:**
- Fácil de configurar
- Portátil entre diferentes servidores
- Aislamiento de dependencias

**Ver sección:** [Despliegue con Docker](#despliegue-con-docker)

### Opción 2: Servidor VPS tradicional

**Ventajas:**
- Control total del servidor
- Más barato a largo plazo
- Ideal para proyectos grandes

**Servicios recomendados:**
- DigitalOcean (desde $6/mes)
- Linode (desde $5/mes)
- AWS EC2 (desde $3.50/mes)
- Vultr (desde $5/mes)

**Ver sección:** [Despliegue en VPS](#despliegue-en-vps)

### Opción 3: Plataformas Cloud Modernas

**Ventajas:**
- Configuración rápida
- Auto-escalado
- CI/CD integrado

**Backend:**
- Railway (https://railway.app) - Gratis hasta 500 horas/mes
- Render (https://render.com) - Plan gratuito disponible
- Fly.io (https://fly.io) - Gratis hasta cierto límite

**Frontend:**
- Vercel (https://vercel.com) - Gratis para proyectos personales
- Netlify (https://netlify.com) - Gratis para proyectos personales
- Cloudflare Pages - Gratis

**Ver sección:** [Despliegue en Cloud](#despliegue-en-cloud)

---

## 🐳 Despliegue con Docker

### Paso 1: Configurar Docker en tu servidor

```bash
# Instalar Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

### Paso 2: Preparar el proyecto

```bash
# En tu servidor, clona el proyecto
git clone <tu-repositorio>
cd Perseus
```

### Paso 3: Configurar variables de entorno

```bash
cd Backend
cp .env.example .env
nano .env  # Edita con tus credenciales reales
```

### Paso 4: Construir frontend para producción

```bash
cd ../Frontend
npm install
npm run build
```

### Paso 5: Configurar Nginx para servir frontend

Crea `Frontend/Dockerfile.prod`:

```dockerfile
FROM nginx:alpine

# Copiar archivos compilados
COPY dist/Perseus/browser /usr/share/nginx/html

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Crea `Frontend/nginx.conf`:

```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Paso 6: Actualizar docker-compose.yml

Edita `Backend/docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: perseus-backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./app:/app/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/requirements/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    build:
      context: ../Frontend
      dockerfile: Dockerfile.prod
    container_name: perseus-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

### Paso 7: Iniciar servicios

```bash
cd Backend
docker-compose up -d
```

### Paso 8: Verificar

```bash
# Ver logs
docker-compose logs -f

# Ver estado
docker-compose ps

# Acceder a:
# Frontend: http://tu-servidor-ip
# Backend: http://tu-servidor-ip:8000/docs
```

---

## ☁️ Despliegue en Cloud

### Opción A: Railway (Backend)

1. **Crear cuenta en Railway**: https://railway.app
2. **Nuevo proyecto > Deploy from GitHub**
3. **Configurar variables de entorno**:
   - Ir a Variables
   - Agregar todas las variables de tu `.env`
4. **Railway detectará automáticamente el Dockerfile**
5. **Obtén la URL del backend**: https://perseus-backend.railway.app

### Opción B: Vercel (Frontend)

1. **Crear cuenta en Vercel**: https://vercel.com
2. **Nuevo proyecto > Import Git Repository**
3. **Configurar:**
   - Framework Preset: Angular
   - Root Directory: `Frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist/Perseus/browser`
4. **Variables de entorno**:
   - `API_URL`: URL de tu backend en Railway
5. **Deploy**

Vercel te dará una URL: https://perseus.vercel.app

### Opción C: Render (Backend + Frontend)

**Backend:**
1. Nuevo Web Service > Connect GitHub
2. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.11
3. Agregar variables de entorno
4. Deploy

**Frontend:**
1. Nuevo Static Site > Connect GitHub
2. Configurar:
   - Build Command: `cd Frontend && npm install && npm run build`
   - Publish Directory: `Frontend/dist/Perseus/browser`
3. Deploy

---

## 🌐 Despliegue en VPS

### Paso 1: Configurar servidor

```bash
# Actualizar sistema (Ubuntu/Debian)
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3.11 python3-pip nodejs npm nginx certbot python3-certbot-nginx git
```

### Paso 2: Configurar Backend

```bash
# Clonar proyecto
git clone <tu-repositorio>
cd Perseus/Backend

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Editar con credenciales reales
```

### Paso 3: Crear servicio systemd para backend

```bash
sudo nano /etc/systemd/system/perseus-backend.service
```

Contenido:

```ini
[Unit]
Description=Perseus FastAPI Backend
After=network.target

[Service]
Type=simple
User=tu-usuario
WorkingDirectory=/ruta/a/Perseus/Backend
Environment="PATH=/ruta/a/Perseus/Backend/venv/bin"
ExecStart=/ruta/a/Perseus/Backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Habilitar e iniciar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable perseus-backend
sudo systemctl start perseus-backend
sudo systemctl status perseus-backend
```

### Paso 4: Compilar Frontend

```bash
cd ../Frontend
npm install
npm run build
```

### Paso 5: Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/perseus
```

Contenido:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Frontend
    root /ruta/a/Perseus/Frontend/dist/Perseus/browser;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API proxy
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
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Habilitar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/perseus /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Paso 6: Configurar SSL con Let's Encrypt

```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Sigue las instrucciones. Certbot configurará automáticamente SSL y redirecciones HTTPS.

### Paso 7: Configurar firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 🔒 Configuración de Dominio y SSL

### 1. Comprar dominio

Servicios recomendados:
- Namecheap (https://namecheap.com)
- Google Domains (https://domains.google)
- Cloudflare Registrar (https://cloudflare.com)

### 2. Configurar DNS

En tu proveedor de DNS, crea registros:

```
Tipo    Nombre    Valor
A       @         IP_DE_TU_SERVIDOR
A       www       IP_DE_TU_SERVIDOR
```

### 3. Configurar SSL

**Opción 1: Let's Encrypt (Gratis)**
- Ya cubierto en [Paso 6 de VPS](#paso-6-configurar-ssl-con-lets-encrypt)

**Opción 2: Cloudflare (Gratis + CDN)**
1. Agregar sitio a Cloudflare
2. Cambiar nameservers de tu dominio
3. Activar SSL/TLS en Cloudflare
4. Configurar reglas de página (opcional)

---

## 📊 Monitoreo y Mantenimiento

### Logs

**Backend (systemd):**
```bash
sudo journalctl -u perseus-backend -f
```

**Backend (Docker):**
```bash
docker-compose logs -f backend
```

**Nginx:**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Monitoreo

**Uptime monitoring (gratis):**
- UptimeRobot (https://uptimerobot.com)
- Pingdom (https://pingdom.com)

**Application monitoring:**
- Sentry (https://sentry.io) - Para errores
- LogRocket (https://logrocket.com) - Para sesiones de usuario

### Actualizaciones

**Backend:**
```bash
cd Backend
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart perseus-backend
```

**Frontend:**
```bash
cd Frontend
git pull
npm install
npm run build
# Los archivos se actualizan automáticamente en dist/
```

### Backups

**Base de datos (si aplica):**
```bash
# Configurar cron job para backups diarios
0 2 * * * /ruta/a/script-backup.sh
```

**Variables de entorno:**
```bash
# Guardar .env en lugar seguro (fuera de git)
cp .env .env.backup.$(date +%Y%m%d)
```

---

## 🎯 Checklist Final de Despliegue

Antes de ir a producción, verifica:

- [ ] Backend `.env` configurado con credenciales reales
- [ ] Frontend `environment.prod.ts` apunta a URL correcta
- [ ] CORS configurado con dominios de producción
- [ ] SSL/HTTPS habilitado
- [ ] Firewall configurado
- [ ] Logs funcionando correctamente
- [ ] Health checks respondiendo
- [ ] Backups automatizados
- [ ] Monitoreo configurado
- [ ] Documentación API actualizada (`/docs`)
- [ ] Pruebas en producción realizadas
- [ ] Plan de rollback preparado

---

## 🆘 Solución de Problemas

### Error: "CORS policy blocked"

Verifica `ALLOWED_ORIGINS` en `.env` del backend:
```env
ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### Error: "Model loading timeout"

Aumenta `MODEL_LOAD_TIMEOUT` en `.env`:
```env
MODEL_LOAD_TIMEOUT=600  # 10 minutos
```

### Error: "API rate limit exceeded"

Si usas Groq/OpenAI, verifica tu cuota de API.

### Frontend no carga después de build

Verifica `<base href="/">` en `index.html` y configuración de rutas en Nginx.

---

## 📚 Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación Angular](https://angular.dev/)
- [HuggingFace Models](https://huggingface.co/models)
- [Groq API Docs](https://console.groq.com/docs)
- [Docker Docs](https://docs.docker.com/)

---

## 🎉 ¡Listo!

Tu aplicación **Perseus** está ahora desplegada en producción.

**URLs importantes:**
- Frontend: https://tu-dominio.com
- Backend API: https://tu-dominio.com/api/requirements/docs
- Health Check: https://tu-dominio.com/api/requirements/health

---

**Desarrollado con ❤️ para análisis de requisitos de usabilidad con IA**
