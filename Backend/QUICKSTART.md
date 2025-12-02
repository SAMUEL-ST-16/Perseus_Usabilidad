# Perseus Backend - Guía Rápida

Guía de inicio rápido para poner en marcha el backend en menos de 5 minutos.

## 🚀 Inicio Rápido con Docker

### 1. Prerrequisitos
- Docker y Docker Compose instalados
- 4GB+ RAM disponible

### 2. Clonar y ejecutar
```bash
# Navegar al directorio del backend
cd Backend

# Ejecutar con Docker Compose
docker-compose up --build
```

### 3. Verificar funcionamiento
```bash
# Abrir en el navegador
http://localhost:8000/docs

# O verificar con curl
curl http://localhost:8000/health
```

¡Listo! La API está corriendo en `http://localhost:8000`

---

## 💻 Inicio Rápido sin Docker

### 1. Prerrequisitos
- Python 3.11+
- pip

### 2. Configurar entorno
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
# Desde el directorio Backend/
uvicorn app.main:app --reload
```

### 4. Verificar
```bash
# Abrir en el navegador
http://localhost:8000/docs
```

---

## 🧪 Probar la API

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: Procesar un comentario
```bash
curl -X POST "http://localhost:8000/analyze/single" \
  -H "Content-Type: application/json" \
  -d '{"comment": "La aplicación debe cifrar las contraseñas del usuario"}'
```

### Test 3: Descargar PDF
```bash
curl -X POST "http://localhost:8000/process/single" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Necesito autenticación de dos factores"}' \
  --output requisito.pdf
```

---

## 📊 Ejemplo de CSV

Crea un archivo `comentarios.csv`:

```csv
comment
La app debe cifrar mis datos personales
Quiero autenticación de dos factores
Debería verificar mi identidad con huella digital
Necesito que guarde mi historial de compras
La app debe ser resistente a ataques
```

Luego prueba:

```bash
curl -X POST "http://localhost:8000/process/csv" \
  -F "file=@comentarios.csv" \
  --output requisitos.pdf
```

---

## 🌐 Ejemplo de Play Store

```bash
curl -X POST "http://localhost:8000/analyze/playstore" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://play.google.com/store/apps/details?id=com.whatsapp"}' \
  | jq .
```

---

## 🛑 Detener el servicio

### Con Docker
```bash
# Detener
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Sin Docker
```bash
# Ctrl+C en la terminal donde corre uvicorn
```

---

## 📚 Próximos pasos

1. Lee el [README.md](README.md) completo
2. Explora la documentación interactiva en `/docs`
3. Personaliza la configuración en `.env`
4. Integra con el frontend

---

## ❓ Problemas comunes

**Error: Port 8000 already in use**
```bash
# Cambiar puerto en docker-compose.yml o .env
PORT=8001
```

**Error: Models not loading**
```bash
# Verificar conexión a internet
# Aumentar memoria disponible
# Revisar logs: docker-compose logs -f
```

**Error: CORS**
```bash
# Agregar origen del frontend en app/core/config.py
CORS_ORIGINS = ["http://localhost:4200"]
```

---

## 🆘 Ayuda

- **Documentación API**: http://localhost:8000/docs
- **Logs**: `docker-compose logs -f backend`
- **Issues**: Reporta problemas en el repositorio
