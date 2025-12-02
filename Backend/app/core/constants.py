"""
Constants for the Perseus API
Centralizes all constant values used throughout the application
"""

# ========== Model Labels ==========
# Etiquetas del modelo binario
# IMPORTANTE: El modelo binario puede retornar etiquetas con nombres personalizados
# o etiquetas genéricas (LABEL_0, LABEL_1). Asegúrate de configurar correctamente
# cuál etiqueta indica "ES UN REQUISITO VÁLIDO".
LABEL_VALID_REQUIREMENT = "requisito_valido"
LABEL_NOT_REQUIREMENT = "no_requisito"

# Variantes de etiquetas del modelo binario
# ⚠️ CONFIGURACIÓN TEMPORAL INVERTIDA PARA TESTING ⚠️
# El modelo está retornando LABEL_0 para todo, así que temporalmente
# se invirtió para probar que el código funciona correctamente.
# Revertir cuando el modelo binario esté re-entrenado correctamente
BINARY_VALID_LABELS = [
    "aplica",            # Etiqueta personalizada
    "LABEL_1",           # ⚠️ INVERTIDO TEMPORALMENTE para testing
    "1"                  # Variante numérica
]

# Etiquetas que indican NO es un requisito
BINARY_INVALID_LABELS = [
    "no-aplica",         # Etiqueta personalizada
    "LABEL_0",           # ⚠️ INVERTIDO TEMPORALMENTE para testing
    "0"                  # Variante numérica
]

# Etiquetas del modelo multiclase (subcaracterísticas de usabilidad ISO 25010:2023)
# El modelo multiclase predice cuál subcaracterística de usabilidad es
USABILITY_SUBCHARACTERISTICS = [
    "Operabilidad",
    "Aprendizabilidad",
    "Involucración del usuario",
    "Reconocibilidad de adecuación",
    "Protección frente a errores de usuario",
    "Inclusividad",
    "Auto descriptividad",
    "Asistencia al usuario"
]

# ========== HTTP Status Codes ==========
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_TOO_MANY_REQUESTS = 429
HTTP_INTERNAL_ERROR = 500
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_GATEWAY_TIMEOUT = 504

# ========== Error Codes ==========
ERROR_VALIDATION = "validation_error"
ERROR_RATE_LIMIT = "rate_limit"
ERROR_MODEL_LOADING = "model_loading"
ERROR_TIMEOUT = "timeout"
ERROR_INTERNAL = "internal_error"
ERROR_PREDICTION = "prediction_error"

# ========== Model Configuration ==========
# Pipeline task type
PIPELINE_TASK = "text-classification"

# Threshold para considerar una predicción como válida
CONFIDENCE_THRESHOLD = 0.5

# ========== Timeouts ==========
# Timeout para carga de modelos (segundos)
MODEL_LOAD_TIMEOUT = 300  # 5 minutos

# Timeout para predicciones (segundos)
PREDICTION_TIMEOUT = 30

# ========== API Documentation ==========
API_TAGS_METADATA = [
    {
        "name": "Requirements Extraction",
        "description": "Endpoints para extracción y clasificación de requisitos de usabilidad según ISO 25010:2023"
    },
    {
        "name": "Health",
        "description": "Endpoints para verificar el estado de la API y modelos"
    }
]
