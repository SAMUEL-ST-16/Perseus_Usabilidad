# Perseus Backend

Backend API para la extracción automática de requisitos de usabilidad desde comentarios de usuarios, basado en el estándar ISO 25010:2023.

## 🚀 Características

- **Clasificación Binaria**: Detecta si un comentario es un requisito de usabilidad válido
- **Clasificación Multiclase**: Clasifica requisitos en 8 subcaracterísticas de usabilidad ISO 25010:2023:
  - Operabilidad
  - Aprendizabilidad
  - Involucración del usuario
  - Reconocibilidad de adecuación
  - Protección frente a errores de usuario
  - Inclusividad
  - Auto descriptividad
  - Asistencia al usuario
- **Generación de PDF**: Crea informes profesionales con los requisitos extraídos
- **Múltiples fuentes**: Procesa comentarios individuales, archivos CSV y URLs de Google Play Store
- **API REST**: FastAPI con documentación interactiva

## 📋 Requisitos

- Python 3.11+
- Docker & Docker Compose (opcional)
- 4GB+ RAM (para modelos de ML)

## 🛠️ Instalación

### Opción 1: Con Docker (Recomendado)

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### Opción 2: Sin Docker

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

# Ejecutar aplicación
uvicorn app.main:app --reload
```

## 📚 Uso de la API

### Documentación Interactiva

Una vez ejecutado, visita:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### 1. Verificar estado
```bash
GET /health
```

#### 2. Procesar comentario único (retorna PDF)
```bash
POST /process/single
Content-Type: application/json

{
  "comment": "La aplicación debería ser más fácil de usar y tener tutoriales interactivos"
}
```

#### 3. Procesar archivo CSV (retorna PDF)
```bash
POST /process/csv
Content-Type: multipart/form-data

file: comentarios.csv
```

#### 4. Procesar URL de Play Store (retorna PDF)
```bash
POST /process/playstore
Content-Type: application/json

{
  "url": "https://play.google.com/store/apps/details?id=com.example.app"
}
```

#### 5. Analizar y obtener JSON (sin PDF)
```bash
POST /analyze/single
POST /analyze/csv
POST /analyze/playstore
```

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# API Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true
WORKERS=1
LOG_LEVEL=INFO

# Model Configuration
BINARY_MODEL_NAME=samuel-moya/requirements-binary-classification
MULTICLASS_MODEL_NAME=samuel-moya/requirements-multiclass-classification

# HuggingFace Token (opcional)
HUGGINGFACE_TOKEN=your_token_here

# Cache Configuration
ENABLE_CACHE=true
CACHE_TTL=3600
```

## 📁 Estructura del Proyecto

```
Backend/
├── app/
│   ├── core/               # Configuración y utilidades
│   │   ├── config.py       # Configuración de la aplicación
│   │   ├── constants.py    # Constantes
│   │   ├── exceptions.py   # Excepciones personalizadas
│   │   └── logger.py       # Configuración de logging
│   ├── routers/            # Endpoints de la API
│   │   └── requirements.py # Rutas de requisitos
│   ├── schemas/            # Modelos Pydantic
│   │   ├── models.py       # Modelos de request/response
│   │   └── requirements.py # Modelos adicionales
│   ├── services/           # Lógica de negocio
│   │   ├── huggingface_service.py    # Servicio de modelos ML
│   │   ├── processing_service.py     # Procesamiento de comentarios
│   │   ├── description_service.py    # Generación de descripciones
│   │   ├── scraper_service.py        # Scraping de Play Store
│   │   ├── pdf_service.py            # Generación de PDFs
│   │   └── orchestrator.py           # Orquestación de servicios
│   └── main.py             # Aplicación FastAPI principal
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con cobertura
pytest --cov=app tests/
```

## 🐛 Troubleshooting

### Los modelos no cargan
- Verifica tu conexión a internet
- Aumenta el timeout en `constants.py`
- Si usas modelos privados, configura `HUGGINGFACE_TOKEN`

### Error de memoria
- Reduce el número de workers
- Aumenta la RAM disponible
- Procesa menos comentarios simultáneamente

### CORS errors
- Verifica `CORS_ORIGINS` en `config.py`
- Agrega el origen del frontend

## 📝 Licencia

MIT License - ver archivo LICENSE

## 👥 Autor

Samuel Soto - Desarrollo de Tesis
[SamuelSoto7](https://huggingface.co/SamuelSoto7)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request
