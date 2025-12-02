#!/bin/bash
#
# Script de Arreglo Rápido del Backend - Perseus
# Corrige el archivo .env y reinicia el servicio
#

set -e

echo "=========================================="
echo "  Perseus - Arreglo Rápido Backend"
echo "=========================================="
echo ""

echo "==> 1. Verificando archivo .env actual:"
cat /opt/perseus/Backend/.env
echo ""

echo "==> 2. Creando backup del .env actual:"
cp /opt/perseus/Backend/.env /opt/perseus/Backend/.env.backup
echo "Backup guardado en: /opt/perseus/Backend/.env.backup"
echo ""

echo "==> 3. Leyendo valores actuales:"
HF_TOKEN=$(grep HUGGINGFACE /opt/perseus/Backend/.env | cut -d'=' -f2 || echo "")
BINARY_MODEL=$(grep BINARY_MODEL_NAME /opt/perseus/Backend/.env | cut -d'=' -f2 || echo "SamuelSoto7/PerseusV8_Binario")
MULTICLASS_MODEL=$(grep MULTICLASS_MODEL_NAME /opt/perseus/Backend/.env | cut -d'=' -f2 || echo "SamuelSoto7/PerseusV2_Multiclass")
GROQ_KEY=$(grep GROQ_API_KEY /opt/perseus/Backend/.env | cut -d'=' -f2 || echo "")
OPENAI_KEY=$(grep OPENAI_API_KEY /opt/perseus/Backend/.env | cut -d'=' -f2 || echo "")

echo "HuggingFace Token: ${HF_TOKEN:0:20}..."
echo "Binary Model: $BINARY_MODEL"
echo "Multiclass Model: $MULTICLASS_MODEL"
echo ""

echo "==> 4. Creando nuevo archivo .env corregido:"
cat > /opt/perseus/Backend/.env << EOF
HUGGINGFACE_TOKEN=$HF_TOKEN
BINARY_MODEL_NAME=$BINARY_MODEL
MULTICLASS_MODEL_NAME=$MULTICLASS_MODEL
PROVIDER=groq
GROQ_API_KEY=$GROQ_KEY
GROQ_MODEL_NAME=llama-3.1-8b-instant
OPENAI_API_KEY=$OPENAI_KEY
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
RELOAD=False
WORKERS=1
EOF

echo "✓ Nuevo .env creado"
echo ""

echo "==> 5. Verificando nuevo .env:"
cat /opt/perseus/Backend/.env
echo ""

echo "==> 6. Ajustando permisos:"
chown perseus:perseus /opt/perseus/Backend/.env
chmod 600 /opt/perseus/Backend/.env
echo "✓ Permisos ajustados"
echo ""

echo "==> 7. Reiniciando servicio backend:"
systemctl restart perseus-backend
echo "✓ Servicio reiniciado"
echo ""

echo "==> 8. Esperando 5 segundos para que el servicio inicie..."
sleep 5
echo ""

echo "==> 9. Verificando estado del servicio:"
systemctl status perseus-backend --no-pager -l
echo ""

echo "==> 10. Verificando puerto 8000:"
netstat -tlnp | grep 8000 || echo "⚠️  Puerto 8000 NO está escuchando aún"
echo ""

echo "==> 11. Últimas líneas del log:"
journalctl -u perseus-backend -n 20 --no-pager
echo ""

echo "=========================================="
echo "  Arreglo Completado"
echo "=========================================="
echo ""
echo "Si el puerto 8000 NO está escuchando, ejecuta:"
echo "  journalctl -u perseus-backend -n 100 --no-pager"
echo ""
echo "Para verificar errores en el log."
echo ""
