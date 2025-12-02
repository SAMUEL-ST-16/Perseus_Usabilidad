# Perseus - Sistema de Extracción de Requisitos de Usabilidad

Sistema automatizado para la extracción y clasificación de requisitos de usabilidad basados en **ISO 25010:2023** a partir de comentarios de usuarios de aplicaciones móviles, utilizando modelos **BERT** y **LLMs**.

## 🎯 Descripción del Proyecto

Perseus es una aplicación web completa que permite analizar comentarios de usuarios de Google Play Store y extraer requisitos de usabilidad clasificados según las 8 subcaracterísticas de usabilidad de la norma ISO 25010:2023:

1. **Operabilidad** - Grado en que el producto tiene atributos que facilitan su operación y control
2. **Aprendizabilidad** - Grado en que el producto permite al usuario aprender su uso
3. **Involucración del usuario** - Grado en que el usuario está satisfecho y motivado con el uso del producto
4. **Reconocibilidad de adecuación** - Grado en que los usuarios pueden reconocer si el producto es apropiado para sus necesidades
5. **Protección frente a errores de usuario** - Grado en que el sistema protege a los usuarios contra cometer errores
6. **Inclusividad** - Grado en que el producto puede ser usado por personas con diversas características y capacidades
7. **Auto descriptividad** - Grado en que la interfaz de usuario es auto-explicativa
8. **Asistencia al usuario** - Grado en que el producto proporciona ayuda y soporte al usuario

## 🏗️ Arquitectura del Sistema

```
Perseus/
├── Backend/                    # API FastAPI con modelos BERT
│   ├── app/
│   │   ├── core/              # Configuración y utilidades
│   │   ├── routers/           # Endpoints de la API
│   │   ├── services/          # Lógica de negocio (ML, scraping, PDF)
│   │   └── schemas/           # Modelos Pydantic
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env.example
│
├── Frontend/                   # Aplicación Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # Componentes de UI
│   │   │   ├── services/      # Servicios HTTP
│   │   │   ├── models/        # Interfaces TypeScript
│   │   │   └── data/          # Datos de referencia
│   │   └── environments/      # Configuración de ambientes
│   ├── Dockerfile.prod
│   ├── nginx.conf
│   └── package.json
│
├── deploy.sh                   # 🚀 Script de despliegue automatizado
├── DIGITALOCEAN_DEPLOY.md     # 📖 Guía de despliegue en DigitalOcean
├── DEPLOYMENT_GUIDE.md        # 📖 Guía completa de despliegue
└── README.md                   # Este archivo
```

## 🚀 Opciones de Despliegue

### 🏆 Opción 1: Terraform - Infrastructure as Code (MÁS PROFESIONAL)

**LA MEJOR OPCIÓN PARA TESIS** - Automatización completa con un solo comando

**Ventajas:**
- ✅ **100% AUTOMATIZADO**: Un solo comando hace TODO
- ✅ **Infrastructure as Code (IaC)**: Infraestructura versionada en Git
- ✅ **MUY PROFESIONAL**: Tecnología usada en empresas reales
- ✅ **REPRODUCIBLE**: Crear/destruir infraestructura fácilmente
- ✅ **CERO CLICS**: No necesitas acceder a DigitalOcean manualmente
- ✅ **GRATIS con GitHub Student Pack**: $200 de crédito

**Guía:** Ver [`TERRAFORM_DEPLOY.md`](TERRAFORM_DEPLOY.md)

**Resumen rápido:**
```bash
# 1. Instalar Terraform
# https://www.terraform.io/downloads

# 2. Ejecutar UN SOLO comando
chmod +x auto-deploy.sh
./auto-deploy.sh

# 3. Esperar 5-10 minutos
# 4. Acceder a http://TU_IP_PUBLICA
```

**Qué hace automáticamente:**
- Crea droplet en DigitalOcean ($6/mes)
- Configura firewall y SSH
- Clona tu repositorio de GitHub
- Instala Python, Node.js, Nginx
- Configura Backend + Frontend
- Despliega aplicación completa

**Costo:** $0 con GitHub Student Pack, o $6/mes

---

### ⭐ Opción 2: DigitalOcean con Script Manual (ALTERNATIVA)

Si prefieres crear el droplet manualmente y luego automatizar la configuración.

**Ventajas:**
- ✅ **Control manual** del droplet
- ✅ **Script automatiza** la configuración
- ✅ **Barato** ($6/mes)

**Guía:** Ver [`DIGITALOCEAN_DEPLOY.md`](DIGITALOCEAN_DEPLOY.md)

**Resumen rápido:**
```bash
# 1. Crear droplet en DigitalOcean (Ubuntu 22.04)
# 2. Conectarse por SSH
ssh root@TU_IP_PUBLICA

# 3. Ejecutar script
chmod +x deploy.sh
sudo ./deploy.sh

# 4. Acceder a http://TU_IP_PUBLICA
```

### Opción 3: Docker (Local o Servidor)

**Ventajas:**
- Fácil de replicar
- Portable entre diferentes sistemas
- Aislamiento de dependencias

**Instrucciones:**
```bash
cd Backend
docker-compose up -d
```

Acceso:
- Frontend: http://localhost
- Backend: http://localhost:8000

**Guía completa:** Ver [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - Sección "Despliegue con Docker"

### Opción 4: Cloud Platforms (Gratis)

**Backend:**
- Railway: https://railway.app (gratis hasta 500 horas/mes)
- Render: https://render.com (plan gratuito)

**Frontend:**
- Vercel: https://vercel.com (gratis para proyectos personales)
- Netlify: https://netlify.com (gratis)

**Guía completa:** Ver [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - Sección "Despliegue en Cloud"

### Opción 5: VPS Tradicional

Para cualquier VPS (AWS EC2, Linode, Vultr, etc.)

**Guía completa:** Ver [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - Sección "Despliegue en VPS"

## 💻 Desarrollo Local

### Requisitos Previos

**Backend:**
- Python 3.11+
- pip

**Frontend:**
- Node.js 18+
- npm 11+
- Angular CLI 21

### Instalación y Ejecución

#### Backend

```bash
cd Backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

Backend disponible en: http://localhost:8000

#### Frontend

```bash
cd Frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
ng serve

# O abrir navegador automáticamente
ng serve --open
```

Frontend disponible en: http://localhost:4200

## 📋 Variables de Entorno Requeridas

### Backend (.env)

```env
# HuggingFace (OBLIGATORIO)
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxx

# Modelos BERT
BINARY_MODEL_NAME=SamuelSoto7/Perseus_binario
MULTICLASS_MODEL_NAME=SamuelSoto7/Perseus_Multiclase

# LLM Provider (elige uno)
LLM_PROVIDER=groq  # o "openai" o "none"

# Groq API (GRATIS - RECOMENDADO)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
GROQ_MODEL=llama-3.1-70b-versatile

# O usar OpenAI (DE PAGO)
# OPENAI_API_KEY=sk_xxxxxxxxxxxxx
# OPENAI_MODEL=gpt-4o-mini

# CORS
CORS_ORIGINS=["http://localhost:4200"]  # En desarrollo
# CORS_ORIGINS=["https://tu-dominio.com"]  # En producción
```

**Obtener tokens:**
- HuggingFace: https://huggingface.co/settings/tokens
- Groq (gratis): https://console.groq.com/keys
- OpenAI (pago): https://platform.openai.com/api-keys

### Frontend (environments)

**Desarrollo:** `src/environments/environment.ts`
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/requirements'
};
```

**Producción:** `src/environments/environment.prod.ts`
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://tu-dominio.com/api/requirements'
};
```

## 🎨 Funcionalidades

### 1. Procesamiento de Comentario Individual
Ingresa un comentario manualmente y obtén un PDF con los requisitos de seguridad extraídos.

### 2. Procesamiento de Archivo CSV
Carga un CSV con múltiples comentarios y obtén un PDF con todos los requisitos analizados.

**Formato CSV:**
```csv
content,score
"El sistema debería tener autenticación de dos factores",4.5
"La app se cierra sola",2.0
```

### 3. Procesamiento desde Google Play Store
Ingresa la URL de una app y automáticamente extrae comentarios y genera requisitos.

**Formato URL:**
```
https://play.google.com/store/apps/details?id=com.ejemplo.app
```

### 4. Página Informativa ISO 25010
Información detallada sobre la norma ISO/IEC 25010 y las subcaracterísticas de seguridad.

## 🔗 APIs y Endpoints

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Health check detallado |
| POST | `/api/requirements/process/single` | Procesar comentario individual |
| POST | `/api/requirements/process/csv` | Procesar archivo CSV |
| POST | `/api/requirements/process/playstore` | Procesar desde Play Store |
| GET | `/api/requirements/docs` | Documentación Swagger |

**Documentación completa:** http://localhost:8000/docs (una vez iniciado el backend)

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Transformers** - Modelos BERT de HuggingFace
- **LangChain** - Orquestación de LLMs
- **BeautifulSoup4** - Web scraping
- **ReportLab** - Generación de PDFs
- **Pydantic** - Validación de datos

### Frontend
- **Angular 21** - Framework frontend
- **TypeScript 5.7** - Lenguaje tipado
- **RxJS** - Programación reactiva
- **CSS3** - Estilos modernos

### Infraestructura
- **Docker** - Contenedorización
- **Nginx** - Reverse proxy y servidor web
- **Systemd** - Gestión de servicios

## 📊 Modelos de Machine Learning

### Modelo Binario
- **Nombre:** `SamuelSoto7/Perseus_binario`
- **Función:** Detecta si un texto es un requisito de usabilidad válido
- **Arquitectura:** BERT fine-tuned

### Modelo Multiclase
- **Nombre:** `SamuelSoto7/Perseus_Multiclase`
- **Función:** Clasifica la subcaracterística de usabilidad según ISO 25010:2023
- **Clases (8):** Operabilidad, Aprendizabilidad, Involucración del usuario, Reconocibilidad de adecuación, Protección frente a errores de usuario, Inclusividad, Auto descriptividad, Asistencia al usuario

### LLM para Descripciones
- **Groq (Gratis):** llama-3.1-70b-versatile
- **OpenAI (Pago):** gpt-4o-mini
- **Función:** Genera descripciones detalladas de requisitos

## 📖 Documentación Completa

### Guías de Despliegue

- **[TERRAFORM_DEPLOY.md](TERRAFORM_DEPLOY.md)** - 🏆 Despliegue con Terraform (MÁS PROFESIONAL - RECOMENDADO)
- **[DIGITALOCEAN_DEPLOY.md](DIGITALOCEAN_DEPLOY.md)** - ⭐ Despliegue automatizado en DigitalOcean
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - 📖 Guía completa de todas las opciones de despliegue

### Documentación de Componentes

- **[Backend/README.md](Backend/README.md)** - Documentación del backend
- **[Frontend/README.md](Frontend/README.md)** - Documentación del frontend

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
cd Backend
pip install -r requirements.txt
```

### Error: CORS policy blocked
Verifica `CORS_ORIGINS` en `.env` del backend.

### Frontend no carga después de build
Verifica la configuración de `environment.prod.ts` con la URL correcta del backend.

### Modelos tardan mucho en cargar
Es normal la primera vez. Los modelos se descargan de HuggingFace y se cachean localmente.

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Angular Documentation](https://angular.dev/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [ISO/IEC 25010:2023](https://iso25000.com/index.php/normas-iso-25000/iso-25010)
- [Groq API Documentation](https://console.groq.com/docs)

## 🎓 Para Tesis

Este proyecto está diseñado para ser presentado como tesis. Incluye:

- ✅ Script de despliegue automatizado profesional
- ✅ Documentación completa y detallada
- ✅ Arquitectura limpia y escalable
- ✅ Despliegue en producción real
- ✅ Uso de tecnologías modernas (BERT, LLMs, FastAPI, Angular)
- ✅ Implementación de estándar internacional (ISO 25010:2023)

### Evidencias para Incluir en Tesis

1. **Capturas de pantalla:**
   - Aplicación funcionando en producción
   - Dashboard de DigitalOcean
   - API Docs (Swagger)
   - Resultados de análisis

2. **Diagramas:**
   - Arquitectura del sistema
   - Flujo de datos
   - Diagrama de despliegue

3. **Código:**
   - Script de despliegue automatizado
   - Ejemplos de endpoints
   - Configuración de Docker

4. **Métricas:**
   - Tiempo de procesamiento
   - Precisión de modelos
   - Logs del sistema

## 📄 Licencia

Proyecto académico - Todos los derechos reservados

## 👨‍💻 Autor

Samuel Soto - [SamuelSoto7](https://huggingface.co/SamuelSoto7)

---

## 🚀 Inicio Rápido

**Para despliegue PROFESIONAL con un solo comando:**
```bash
./auto-deploy.sh
```
Ver guía completa: [`TERRAFORM_DEPLOY.md`](TERRAFORM_DEPLOY.md)

**Para otras opciones de despliegue:** Ver [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)
