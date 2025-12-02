# 🚨 Solución Rápida - Servidor Desplegado con Versión Antigua

## 📊 Diagnóstico del Problema

El servidor que desplegaste **usó la versión ANTERIOR** de `cloud-init.yaml` (antes de implementar la estrategia de reinicio en 2 fases).

**Evidencia:**
- ❌ No existe `/var/log/perseus-post-boot.log`
- ❌ No hay entradas en journalctl para los servicios
- ❌ El servidor no se reinició automáticamente
- ✅ Cloud-init terminó en ~97 segundos (muy rápido, no instaló nada)

**Causa:** El servidor se creó ANTES de que subieras los cambios a GitHub, o Terraform usó una versión cacheada del `cloud-init.yaml`.

---

## 🔧 Solución 1: Re-desplegar desde Cero (RECOMENDADO)

### Paso 1: Destruir el servidor actual

```bash
cd "c:\Users\SAMUEL\Documents\XII CICLO\Desarrollo de Tesis Final\Perseus\terraform"
terraform destroy -auto-approve
```

### Paso 2: Verificar que los cambios están en cloud-init.yaml

```bash
# Buscar la sección write_files (debe existir)
grep -n "write_files:" cloud-init.yaml

# Buscar el comando reboot (debe existir al final)
grep -n "reboot" cloud-init.yaml
```

**Deberías ver:**
- Línea ~16: `write_files:`
- Línea ~250+: `- reboot`

### Paso 3: Limpiar caché de Terraform

```bash
rm -rf .terraform/
rm -f .terraform.lock.hcl
rm -f terraform.tfstate*
```

### Paso 4: Re-desplegar

```bash
# Opción A: Con auto-deploy.sh
cd ..
./auto-deploy.sh

# Opción B: Manual
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

### Paso 5: Monitorear el despliegue

```bash
# Esperar 2 minutos después de terraform apply, luego conectarse
ssh -i ~/.ssh/perseus_terraform root@<IP_DEL_SERVIDOR>

# Ver logs de cloud-init en tiempo real
tail -f /var/log/cloud-init-output.log

# Deberías ver:
# - Instalación de Python 3.11
# - Instalación de Node.js
# - Clonación del repositorio
# - Instalación de dependencias
# - "Reiniciando servidor para completar la instalación..."
# - Luego se cortará la conexión (reinicio)

# Esperar 1 minuto y reconectarse
ssh -i ~/.ssh/perseus_terraform root@<IP_DEL_SERVIDOR>

# Verificar que el post-boot se ejecutó
cat /var/log/perseus-post-boot.log
```

---

## 🔧 Solución 2: Arreglar el Servidor Actual (Temporal)

Si no quieres destruir el servidor, puedes iniciar los servicios manualmente:

### Conectarse al servidor

```bash
ssh -i ~/.ssh/perseus_terraform root@<IP_DEL_SERVIDOR>
```

### Verificar qué se instaló

```bash
# Ver si la aplicación está instalada
ls -la /opt/perseus/

# Ver si el servicio existe
systemctl status perseus-backend.service
```

### Si la aplicación NO está instalada

El servidor está vacío. **DEBES usar Solución 1** (re-desplegar).

### Si la aplicación SÍ está instalada

Iniciar servicios manualmente:

```bash
# Iniciar backend
systemctl start perseus-backend.service

# Verificar estado
systemctl status perseus-backend.service
systemctl status nginx.service

# Ver logs si hay errores
journalctl -u perseus-backend.service -n 50
```

---

## ✅ Verificación Post-Despliegue

Después de re-desplegar, verifica:

### 1. Logs de post-boot existen

```bash
cat /var/log/perseus-post-boot.log
```

**Debe mostrar:**
```
=== Perseus Post-Boot Script ===
Fecha: Mon Dec 01 XX:XX:XX UTC 2025
✓ Backend service está habilitado
✓ Nginx service está habilitado
Iniciando backend...
✓ Backend está ACTIVO
✓ Nginx está ACTIVO
=== Post-Boot Completado ===
```

### 2. Script se auto-eliminó

```bash
ls -la /opt/perseus-post-boot.sh
# Debe decir: No such file or directory
```

### 3. Servicios están corriendo

```bash
systemctl status perseus-backend.service
systemctl status nginx.service
# Ambos deben decir: Active: active (running)
```

### 4. Aplicación responde

```bash
# Desde el servidor
curl http://localhost:80

# Desde tu navegador
http://<IP_DEL_SERVIDOR>
http://<IP_DEL_SERVIDOR>/api/requirements/docs
```

---

## 🎯 Recomendación Final

**USA SOLUCIÓN 1** (re-desplegar desde cero). Es más rápido y garantiza que todo funcione correctamente.

**Tiempo total:** ~7-8 minutos
- Destruir servidor: 1 min
- Terraform apply: 2 min
- Cloud-init + reinicio + post-boot: 5 min

---

## 📝 Checklist de Verificación

Antes de re-desplegar, confirma:

- [ ] El archivo `cloud-init.yaml` tiene la sección `write_files:` (línea ~16)
- [ ] El archivo `cloud-init.yaml` tiene el comando `- reboot` al final
- [ ] Los cambios están guardados y subidos a GitHub
- [ ] Has ejecutado `terraform destroy` para eliminar el servidor actual
- [ ] Has limpiado el caché de Terraform

Después de re-desplegar, confirma:

- [ ] El archivo `/var/log/perseus-post-boot.log` existe
- [ ] El script `/opt/perseus-post-boot.sh` NO existe (se auto-eliminó)
- [ ] El servicio `perseus-backend.service` está activo
- [ ] El servicio `nginx.service` está activo
- [ ] La aplicación responde en `http://<IP>/`
