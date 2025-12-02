# Despliegue en DigitalOcean - Guía Rápida

Esta guía te permite desplegar **Backend + Frontend** completo en un solo servidor DigitalOcean usando un script automatizado.

## ¿Por Qué Esta Opción?

✅ **TODO EN UN SOLO LUGAR**: Backend + Frontend en el mismo servidor
✅ **SCRIPT AUTOMATIZADO**: Instalación completamente automática
✅ **BAJO COSTO**: Desde $6/mes (puedes destruirlo después)
✅ **PROFESIONAL**: Perfecto para tesis
✅ **SÍ ES DESPLIEGUE EN PRODUCCIÓN**: Completamente válido

## Costo Estimado

| Plan | CPU | RAM | Almacenamiento | Costo/Mes |
|------|-----|-----|----------------|-----------|
| Basic | 1 vCPU | 1 GB | 25 GB SSD | $6 USD |
| Basic | 1 vCPU | 2 GB | 50 GB SSD | $12 USD |
| Basic | 2 vCPU | 2 GB | 60 GB SSD | $18 USD |

**Recomendación para tesis:** Plan de $6/mes es suficiente. Puedes destruir el droplet después de la presentación.

## Paso 1: Crear Cuenta en DigitalOcean

1. Ve a https://www.digitalocean.com/
2. Crea una cuenta (te dan $200 de crédito gratis por 60 días con GitHub Student Pack)
3. Verifica tu cuenta (necesitas tarjeta de crédito o PayPal)

### Obtener Crédito Gratis (Estudiantes)

Si tienes cuenta de estudiante en GitHub:
1. Ve a https://education.github.com/pack
2. Solicita el GitHub Student Developer Pack
3. Activa el beneficio de DigitalOcean ($200 gratis por 60 días)

## Paso 2: Crear un Droplet

1. **Inicia sesión** en DigitalOcean
2. Click en **"Create"** → **"Droplets"**
3. Configurar el droplet:

### Distribución
- Selecciona **Ubuntu 22.04 LTS**

### Plan
- Selecciona **Basic** ($6/mes es suficiente)
- CPU: Shared CPU
- Disco: Regular (SSD)

### Datacenter Region
- Elige la región más cercana (ej: New York, San Francisco)

### Authentication
- **Opción 1 (Recomendada):** SSH Key
  - Genera una clave SSH si no tienes una
  - Windows: `ssh-keygen -t rsa -b 4096`
  - Agrega la clave pública (.pub) a DigitalOcean

- **Opción 2 (Más Fácil):** Password
  - Crea una contraseña fuerte
  - La usarás para conectarte al servidor

### Hostname
- Pon un nombre descriptivo: `perseus-server`

4. Click en **"Create Droplet"**
5. Espera 1-2 minutos mientras se crea

## Paso 3: Conectarse al Droplet

Una vez creado, verás la **IP pública** del droplet (ej: `159.65.123.45`)

### Desde Windows (PowerShell o CMD)

```bash
ssh root@TU_IP_PUBLICA
# Ejemplo: ssh root@159.65.123.45
```

### Desde Linux/Mac

```bash
ssh root@TU_IP_PUBLICA
```

Si usaste password, ingresa la contraseña que configuraste.

## Paso 4: Subir el Script de Despliegue

Hay dos formas de hacerlo:

### Opción A: Clonar desde GitHub (RECOMENDADO)

Si ya subiste tu proyecto a GitHub:

```bash
# Dentro del droplet
cd /tmp
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
chmod +x deploy.sh
```

### Opción B: Copiar el script directamente

Desde tu computadora local:

```bash
# Copiar deploy.sh al servidor
scp deploy.sh root@TU_IP_PUBLICA:/tmp/deploy.sh
```

Luego en el servidor:

```bash
chmod +x /tmp/deploy.sh
```

## Paso 5: Ejecutar el Script de Despliegue

```bash
sudo /tmp/deploy.sh
```

El script te pedirá:

### Información Requerida:

1. **URL del repositorio Git**
   ```
   Ejemplo: https://github.com/tu-usuario/Perseus.git
   ```

2. **HuggingFace Token** (OBLIGATORIO)
   ```
   Obtén uno en: https://huggingface.co/settings/tokens
   ```

3. **Groq API Key** (RECOMENDADO - GRATIS)
   ```
   Obtén uno gratis en: https://console.groq.com/keys
   Presiona Enter para omitir
   ```

4. **OpenAI API Key** (OPCIONAL - DE PAGO)
   ```
   Solo si quieres usar OpenAI en lugar de Groq
   Presiona Enter para omitir
   ```

5. **Nombre del modelo binario**
   ```
   Por defecto: SamuelSoto7/Perseus_binario
   Presiona Enter para usar el valor por defecto
   ```

6. **Nombre del modelo multiclase**
   ```
   Por defecto: SamuelSoto7/Perseus_Multiclase
   Presiona Enter para usar el valor por defecto
   ```

7. **Dominio** (OPCIONAL)
   ```
   Si tienes un dominio (ej: perseus.com), ingrésalo
   Si no, presiona Enter y usará la IP pública
   ```

### ¿Qué hace el script?

El script automáticamente:
- ✅ Actualiza el sistema
- ✅ Instala Python 3.11
- ✅ Instala Node.js 18
- ✅ Clona tu repositorio
- ✅ Configura el Backend con .env
- ✅ Instala dependencias de Python
- ✅ Compila el Frontend Angular
- ✅ Configura Nginx como reverse proxy
- ✅ Crea servicio systemd para auto-inicio
- ✅ Configura firewall (UFW)
- ✅ Inicia todo automáticamente

**Tiempo estimado:** 5-10 minutos

## Paso 6: Verificar el Despliegue

Una vez que el script termine, verás un resumen con:

```
================================================
  ✅ DESPLIEGUE COMPLETADO EXITOSAMENTE
================================================

📋 INFORMACIÓN DEL SERVIDOR:
  - IP Pública: 159.65.123.45

🌐 URLS DE ACCESO:
  - Frontend: http://159.65.123.45
  - Backend API Docs: http://159.65.123.45/api/requirements/docs
  - Health Check: http://159.65.123.45/health
```

### Probar la Aplicación

1. Abre tu navegador
2. Ve a `http://TU_IP_PUBLICA`
3. Deberías ver el frontend de Perseus
4. Prueba las funcionalidades

### Verificar Backend

Ve a `http://TU_IP_PUBLICA/api/requirements/docs` para ver la documentación de la API.

## Paso 7: Configurar SSL (HTTPS) - OPCIONAL

Si tienes un dominio:

### 1. Configurar DNS

En tu proveedor de dominio (Namecheap, GoDaddy, etc.):

```
Tipo    Nombre    Valor
A       @         TU_IP_PUBLICA
A       www       TU_IP_PUBLICA
```

Espera 5-30 minutos para que el DNS se propague.

### 2. Instalar Certificado SSL

En el droplet:

```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Sigue las instrucciones de Certbot. Esto:
- Obtiene un certificado SSL gratis de Let's Encrypt
- Configura HTTPS automáticamente
- Redirige HTTP → HTTPS

Ahora tu app estará en `https://tu-dominio.com`

## Comandos Útiles

### Ver logs del backend
```bash
sudo journalctl -u perseus-backend -f
```

### Reiniciar backend
```bash
sudo systemctl restart perseus-backend
```

### Ver estado del backend
```bash
sudo systemctl status perseus-backend
```

### Reiniciar Nginx
```bash
sudo systemctl restart nginx
```

### Ver logs de Nginx
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Actualizar la aplicación
```bash
cd /opt/perseus/Backend
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart perseus-backend

cd /opt/perseus/Frontend
git pull origin main
npm install
npm run build
sudo systemctl restart nginx
```

## Solución de Problemas

### El frontend no carga

```bash
# Verificar que Nginx esté corriendo
sudo systemctl status nginx

# Verificar logs de Nginx
sudo tail -f /var/log/nginx/error.log

# Reiniciar Nginx
sudo systemctl restart nginx
```

### El backend no responde

```bash
# Verificar que el servicio esté corriendo
sudo systemctl status perseus-backend

# Ver logs del backend
sudo journalctl -u perseus-backend -f

# Reiniciar backend
sudo systemctl restart perseus-backend
```

### Error "Connection refused" al acceder a la API

```bash
# Verificar que el backend esté escuchando en el puerto 8000
sudo netstat -tlnp | grep 8000

# Si no aparece, revisar logs
sudo journalctl -u perseus-backend -n 50
```

### Error de CORS

Edita el archivo `.env` del backend:

```bash
sudo nano /opt/perseus/Backend/.env
```

Agrega tu dominio o IP a `CORS_ORIGINS`:
```env
CORS_ORIGINS=["http://tu-dominio.com","https://tu-dominio.com"]
```

Reinicia el backend:
```bash
sudo systemctl restart perseus-backend
```

## Costos y Destrucción del Droplet

### Ver Costos
En el dashboard de DigitalOcean puedes ver el uso actual y costos estimados.

### Destruir el Droplet (Después de la Presentación)

1. Ve al dashboard de DigitalOcean
2. Click en el droplet
3. Click en "Destroy"
4. Confirma

**IMPORTANTE:** Esto eliminará TODOS los datos del servidor. Asegúrate de tener backup de todo lo importante.

### Backup del Droplet (Antes de Destruir)

#### Opción 1: Snapshot (Imagen completa)
```bash
# Desde el dashboard de DigitalOcean
# Droplets → Tu droplet → Snapshots → Take Snapshot
```
Costo: ~$0.05/GB/mes

#### Opción 2: Backup manual de archivos
```bash
# Desde tu computadora local
scp -r root@TU_IP:/opt/perseus ./backup-perseus
```

## Para tu Tesis

### Documentación que Puedes Incluir

1. **Capturas de Pantalla:**
   - Dashboard de DigitalOcean con el droplet
   - Frontend funcionando en la IP pública
   - Backend API docs (`/api/requirements/docs`)
   - Logs del sistema mostrando el servicio corriendo

2. **Diagrama de Arquitectura:**
   ```
   Internet → Nginx (Puerto 80/443)
       ├── / → Frontend Angular (archivos estáticos)
       └── /api/ → Backend FastAPI (127.0.0.1:8000)
   ```

3. **Script de Despliegue:**
   Incluye el `deploy.sh` en los anexos de tu tesis

4. **Evidencia de Producción:**
   - URL pública funcionando
   - Logs del sistema
   - Métricas de uso

## Checklist de Despliegue

Antes de presentar tu tesis:

- [ ] Droplet creado en DigitalOcean
- [ ] Script de despliegue ejecutado exitosamente
- [ ] Frontend accesible desde IP pública
- [ ] Backend API docs funcionando
- [ ] Todas las funcionalidades probadas
- [ ] (Opcional) SSL configurado con dominio
- [ ] Capturas de pantalla tomadas
- [ ] URL documentada en la tesis

## Recursos Adicionales

- [Documentación DigitalOcean](https://docs.digitalocean.com/)
- [Tutorial SSH en DigitalOcean](https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/)
- [Let's Encrypt SSL](https://letsencrypt.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

**¿Necesitas ayuda?** Revisa los comandos de solución de problemas o consulta los logs del sistema.
