#!/bin/bash
#
# Script de Diagnóstico del Backend - Perseus
#

echo "=========================================="
echo "  Perseus - Diagnóstico del Backend"
echo "=========================================="
echo ""

echo "==> 1. Estado del servicio backend:"
systemctl status perseus-backend --no-pager -l
echo ""

echo "==> 2. Logs del backend (últimas 100 líneas):"
journalctl -u perseus-backend -n 100 --no-pager
echo ""

echo "==> 3. Procesos de Python/Uvicorn:"
ps aux | grep -E 'python|uvicorn' | grep -v grep
echo ""

echo "==> 4. Puertos escuchando (8000):"
netstat -tlnp | grep 8000 || echo "Puerto 8000 NO está escuchando"
echo ""

echo "==> 5. Verificando instalación de dependencias:"
ls -la /opt/perseus/Backend/venv/
echo ""

echo "==> 6. Verificando archivo .env:"
ls -la /opt/perseus/Backend/.env
echo ""

echo "==> 7. Contenido de .env (sin secretos):"
cat /opt/perseus/Backend/.env | grep -v "API_KEY\|TOKEN" || echo "No se puede leer .env"
echo ""

echo "==> 8. Verificando permisos del directorio:"
ls -la /opt/perseus/Backend/ | head -20
echo ""

echo "==> 9. Verificando usuario del servicio:"
cat /etc/systemd/system/perseus-backend.service | grep User
echo ""

echo "==> 10. Probando uvicorn manualmente (como usuario perseus):"
su - perseus -c "cd /opt/perseus/Backend && source venv/bin/activate && python -c 'import sys; print(sys.version)' && pip list | grep -E 'fastapi|uvicorn|torch|transformers'"
echo ""

echo "=========================================="
echo "  Diagnóstico Completado"
echo "=========================================="
