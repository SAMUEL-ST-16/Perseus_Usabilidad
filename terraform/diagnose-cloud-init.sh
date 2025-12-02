#!/bin/bash
# Script para diagnosticar cloud-init en el servidor

echo "=== DIAGNÓSTICO COMPLETO DE CLOUD-INIT ==="
echo ""

echo "[1] Verificar si cloud-init se ejecutó completamente"
cloud-init status --long
echo ""

echo "[2] Ver qué módulos de cloud-init se ejecutaron"
ls -la /var/lib/cloud/instance/
echo ""

echo "[3] Ver user-data recibido por cloud-init"
echo "Primeras 100 líneas de user-data:"
head -n 100 /var/lib/cloud/instance/user-data.txt 2>&1 || echo "No se encontró user-data.txt"
echo ""

echo "[4] Ver si hay errores en cloud-init"
grep -i "error\|fail\|traceback" /var/log/cloud-init.log | head -n 20
echo ""

echo "[5] Ver cloud-init-output completo (últimas 100 líneas)"
tail -n 100 /var/log/cloud-init-output.log
echo ""

echo "[6] Verificar si write_files funcionó"
ls -la /opt/perseus-post-boot.sh 2>&1
ls -la /etc/systemd/system/perseus-post-boot.service 2>&1
echo ""

echo "[7] Verificar si runcmd se ejecutó"
grep -A 5 "Running.*runcmd" /var/log/cloud-init.log
echo ""

echo "[8] Ver contenido completo de cloud-init.log (últimas 200 líneas)"
tail -n 200 /var/log/cloud-init.log
echo ""

echo "=== FIN DEL DIAGNÓSTICO ==="
