# 🚀 Perseus - Inicio Rápido

## Opción 1: Terraform (🏆 MÁS PROFESIONAL - RECOMENDADO)

**Un solo comando despliega TODO automáticamente**

### Prerequisitos

1. **Instalar Terraform**: https://www.terraform.io/downloads
2. **Cuenta DigitalOcean**: https://www.digitalocean.com/
3. **GitHub Student Pack** (opcional): $200 gratis → https://education.github.com/pack

### Credenciales Necesarias

Consigue estas API keys antes de empezar:

| Servicio | Link | Costo | Obligatorio |
|----------|------|-------|-------------|
| DigitalOcean Token | https://cloud.digitalocean.com/account/api/tokens | $6/mes* | ✅ Sí |
| HuggingFace Token | https://huggingface.co/settings/tokens | Gratis | ✅ Sí |
| Groq API Key | https://console.groq.com/keys | Gratis | ⭐ Recomendado |
| OpenAI API Key | https://platform.openai.com/api-keys | De pago | ❌ Opcional |

*\*Con GitHub Student Pack: GRATIS ($200 de crédito)*

### Despliegue en 3 Pasos

```bash
# 1. Clonar o asegurarte que tu proyecto esté en GitHub
git push origin main

# 2. Ejecutar script de despliegue
chmod +x auto-deploy.sh
./auto-deploy.sh

# 3. Ingresar credenciales cuando te las pida
# El script hará TODO automáticamente
```

**Tiempo total:** 2-3 minutos (Terraform) + 5-10 minutos (configuración automática)

**Resultado:**
- Droplet creado en DigitalOcean
- Backend + Frontend desplegados
- App funcionando en: `http://TU_IP_PUBLICA`

### Qué Hace el Script Automáticamente

✅ Crea servidor (droplet) en DigitalOcean
✅ Configura firewall y seguridad
✅ Instala Python 3.11 y Node.js 18
✅ Clona tu repositorio de GitHub
✅ Configura variables de entorno
✅ Instala todas las dependencias
✅ Compila Frontend
✅ Configura Nginx
✅ Inicia servicios automáticamente

**CERO INTERVENCIÓN MANUAL**

---

## Opción 2: Docker Local (Para Desarrollo/Pruebas)

**Si solo quieres probar localmente**

### Prerequisitos

- Docker instalado: https://www.docker.com/get-started
- Las mismas API keys de arriba

### Despliegue

```bash
# 1. Configurar variables de entorno
cd Backend
cp .env.example .env
nano .env  # Edita con tus credenciales

# 2. Iniciar con Docker Compose
docker-compose up -d
```

**Resultado:**
- Frontend: http://localhost
- Backend: http://localhost:8000

---

## Después del Despliegue

### Verificar que Funciona

1. **Frontend**: Abre `http://TU_IP_PUBLICA` en tu navegador
2. **Backend Docs**: `http://TU_IP_PUBLICA/api/requirements/docs`
3. **Health Check**: `http://TU_IP_PUBLICA/health`

### Conectarse al Servidor (Solo Terraform)

```bash
# SSH key está en ~/.ssh/perseus_terraform
ssh -i ~/.ssh/perseus_terraform root@TU_IP_PUBLICA
```

### Ver Logs

```bash
# Backend
ssh root@TU_IP "sudo journalctl -u perseus-backend -f"

# Nginx
ssh root@TU_IP "sudo tail -f /var/log/nginx/error.log"

# Cloud-init (configuración inicial)
ssh root@TU_IP "tail -f /var/log/cloud-init-output.log"
```

### Destruir Infraestructura (Después de la Presentación)

```bash
cd terraform
terraform destroy
```

Esto elimina TODO y deja de cobrar.

---

## Estructura de Archivos del Proyecto

```
Perseus/
├── auto-deploy.sh              🚀 Script maestro (ejecuta esto)
├── TERRAFORM_DEPLOY.md         📖 Guía completa de Terraform
├── QUICKSTART.md               ⚡ Esta guía
│
├── terraform/                  🏗️ Infraestructura como código
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── cloud-init.yaml
│   └── terraform.tfvars.example
│
├── Backend/                    🔙 API FastAPI
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
└── Frontend/                   🎨 App Angular
    ├── src/
    ├── package.json
    └── Dockerfile.prod
```

---

## Troubleshooting Rápido

### "Terraform not found"
```bash
# Instalar Terraform
# macOS:
brew install terraform

# Linux:
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

### "Error creating droplet"
- Verifica que tu token de DigitalOcean tenga permisos Read & Write
- Verifica que tengas crédito o método de pago
- Prueba cambiar la región en terraform.tfvars

### "Frontend no carga"
Espera 5-10 minutos. Cloud-init está configurando el servidor.

Para ver progreso:
```bash
ssh root@TU_IP "tail -f /var/log/cloud-init-output.log"
```

---

## Para tu Tesis

### Capturas de Pantalla Recomendadas

1. Output de `terraform apply` mostrando recursos creados
2. Dashboard de DigitalOcean con el droplet
3. Frontend funcionando en el navegador
4. Backend Swagger docs (`/api/requirements/docs`)
5. Ejemplo de análisis de requisitos (PDF generado)

### Frase para tu Presentación

> "Implementé Infrastructure as Code usando Terraform para automatizar completamente el despliegue en DigitalOcean. Con un solo comando se crea toda la infraestructura, se configura el servidor y se despliega la aplicación sin intervención manual, demostrando prácticas modernas de DevOps."

---

## Links Útiles

📖 **Documentación Completa:**
- [TERRAFORM_DEPLOY.md](TERRAFORM_DEPLOY.md) - Guía detallada de Terraform
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Todas las opciones de despliegue
- [Backend/README.md](Backend/README.md) - Documentación del backend
- [Frontend/README.md](Frontend/README.md) - Documentación del frontend

🔗 **Servicios Externos:**
- DigitalOcean: https://www.digitalocean.com/
- Terraform: https://www.terraform.io/
- HuggingFace: https://huggingface.co/
- Groq: https://console.groq.com/

📚 **Recursos:**
- ISO 25010:2023: https://iso25000.com/index.php/normas-iso-25000/iso-25010
- FastAPI: https://fastapi.tiangolo.com/
- Angular: https://angular.dev/

---

## Checklist Final

Antes de presentar tu tesis:

- [ ] Proyecto funciona localmente
- [ ] Código subido a GitHub
- [ ] Terraform instalado
- [ ] Credenciales de APIs listas
- [ ] Ejecutado `./auto-deploy.sh`
- [ ] Aplicación funcionando en IP pública
- [ ] Capturas de pantalla tomadas
- [ ] URLs documentadas en la tesis

---

**¿Listo? ¡Ejecuta `./auto-deploy.sh` y en 10 minutos tendrás tu app desplegada!** 🚀
