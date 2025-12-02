# Despliegue Completamente Automatizado con Terraform

Esta es la **opción MÁS PROFESIONAL** para desplegar Perseus. Con **UN SOLO COMANDO** creas toda la infraestructura en DigitalOcean y despliegas la aplicación automáticamente.

## ¿Por Qué Terraform?

✅ **100% AUTOMATIZADO**: Un solo comando hace TODO
✅ **Infrastructure as Code (IaC)**: Código que define infraestructura
✅ **MUY PROFESIONAL**: Impresiona en tesis y entrevistas
✅ **REPRODUCIBLE**: Puedes crear/destruir la infraestructura fácilmente
✅ **NO MANUAL**: Cero clics en DigitalOcean

## Arquitectura del Despliegue

```
Tu Computadora
    │
    │  (1) Ejecuta auto-deploy.sh
    │
    ▼
Terraform
    │
    │  (2) Crea droplet en DigitalOcean
    │
    ▼
DigitalOcean Droplet
    │
    │  (3) Cloud-init instala y configura TODO
    │
    ▼
Aplicación Desplegada
  - Backend: FastAPI
  - Frontend: Angular
  - Nginx: Reverse Proxy
  - Systemd: Auto-inicio
```

## Requisitos Previos

### 1. Terraform Instalado

**Verificar si está instalado:**
```bash
terraform version
```

**Si NO está instalado:**

#### macOS (con Homebrew):
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

#### Linux (Ubuntu/Debian):
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

#### Windows (con Chocolatey):
```bash
choco install terraform
```

**O descarga desde:** https://www.terraform.io/downloads

### 2. Cuenta en DigitalOcean

- Crea una cuenta en https://www.digitalocean.com/
- **IMPORTANTE**: Con GitHub Student Pack obtienes **$200 GRATIS** por 60 días
  - Ve a https://education.github.com/pack
  - Activa el beneficio de DigitalOcean

### 3. API Token de DigitalOcean

1. Inicia sesión en DigitalOcean
2. Ve a **API** → https://cloud.digitalocean.com/account/api/tokens
3. Click en **"Generate New Token"**
4. Nombre: `Perseus`
5. Permisos: **Read & Write** (ambos marcados)
6. Click en **"Generate Token"**
7. **IMPORTANTE**: Copia el token inmediatamente (solo se muestra una vez)

### 4. Credenciales de APIs

Necesitarás:
- **HuggingFace Token**: https://huggingface.co/settings/tokens
- **Groq API Key** (GRATIS): https://console.groq.com/keys
- O **OpenAI API Key** (PAGO): https://platform.openai.com/api-keys

### 5. Proyecto en GitHub

Tu proyecto debe estar en GitHub para que el droplet pueda clonarlo.

```bash
# Si aún no lo has subido:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/Perseus.git
git push -u origin main
```

## Despliegue - UN SOLO COMANDO

### Opción A: Script Automatizado (RECOMENDADO)

Este script te guía paso a paso pidiendo las credenciales:

```bash
# Dar permisos de ejecución
chmod +x auto-deploy.sh

# Ejecutar
./auto-deploy.sh
```

El script te pedirá:
1. DigitalOcean Token
2. URL del repositorio de GitHub
3. HuggingFace Token
4. Groq API Key (o OpenAI)
5. Región del droplet (ej: nyc1)
6. Tamaño del droplet (ej: s-1vcpu-1gb)
7. Nombres de los modelos

**Tiempo total: 2-3 minutos para crear infraestructura + 5-10 minutos para configuración automática**

### Opción B: Manual (Para Usuarios Avanzados)

```bash
cd terraform

# 1. Copiar archivo de ejemplo
cp terraform.tfvars.example terraform.tfvars

# 2. Editar con tus credenciales
nano terraform.tfvars

# 3. Generar SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/perseus_terraform -N ""

# 4. Inicializar Terraform
terraform init

# 5. Ver plan de despliegue
terraform plan

# 6. Aplicar (crear infraestructura)
terraform apply
```

## ¿Qué Hace Terraform Automáticamente?

### 1. Crea Infraestructura
- **Droplet** (servidor virtual) en DigitalOcean
- **SSH Key** para acceso seguro
- **Firewall** con reglas de seguridad
- **Opcional**: Registro de dominio DNS

### 2. Cloud-Init Configura el Servidor
Cuando el droplet se crea, **cloud-init** ejecuta automáticamente:

1. ✅ Actualiza el sistema
2. ✅ Instala Python 3.11
3. ✅ Instala Node.js 18
4. ✅ Clona tu repositorio de GitHub
5. ✅ Configura el Backend (.env con tus credenciales)
6. ✅ Instala dependencias de Python
7. ✅ Compila el Frontend Angular
8. ✅ Configura Nginx como reverse proxy
9. ✅ Crea servicio systemd para auto-inicio
10. ✅ Configura firewall (ufw)

**TODO ESTO SIN INTERVENCIÓN MANUAL**

## Verificar el Despliegue

### 1. Ver Outputs de Terraform

Después de que `terraform apply` termine, verás:

```
Outputs:

droplet_ip = "167.172.123.45"
frontend_url = "http://167.172.123.45"
backend_docs_url = "http://167.172.123.45/api/requirements/docs"
ssh_command = "ssh root@167.172.123.45"
```

### 2. Monitorear Configuración Automática

Cloud-init tarda 5-10 minutos en configurar todo. Para ver el progreso:

```bash
# Conectarse al servidor
ssh root@TU_IP_PUBLICA

# Ver logs de cloud-init en tiempo real
tail -f /var/log/cloud-init-output.log

# O ver información del despliegue
cat /root/deployment-info.txt
```

### 3. Acceder a la Aplicación

Una vez que cloud-init termine:

- **Frontend**: http://TU_IP_PUBLICA
- **Backend Docs**: http://TU_IP_PUBLICA/api/requirements/docs
- **Health Check**: http://TU_IP_PUBLICA/health

## Estructura de Archivos de Terraform

```
terraform/
├── main.tf                    # Configuración principal de infraestructura
├── variables.tf               # Definición de variables
├── outputs.tf                 # Valores de salida después del despliegue
├── cloud-init.yaml            # Script de configuración automática del droplet
├── terraform.tfvars.example   # Ejemplo de archivo de variables
├── terraform.tfvars           # TUS credenciales (git-ignored)
└── .gitignore                 # Archivos a no subir a Git
```

## Archivos Creados Automáticamente

Durante el despliegue, Terraform crea:

```
.terraform/                    # Plugins de Terraform (git-ignored)
.terraform.lock.hcl           # Lock file de dependencias
terraform.tfstate             # Estado actual de la infraestructura (git-ignored)
terraform.tfstate.backup      # Backup del estado (git-ignored)
```

**IMPORTANTE**: Estos archivos están en `.gitignore` y NO deben subirse a Git porque contienen información sensible.

## Comandos Útiles

### Ver Estado de la Infraestructura

```bash
cd terraform
terraform show
```

### Ver Outputs

```bash
terraform output
terraform output droplet_ip
```

### Actualizar la Aplicación

Si haces cambios en tu código y quieres actualizar:

```bash
# Conectarse al servidor
ssh root@TU_IP_PUBLICA

# Actualizar Backend
cd /opt/perseus/Backend
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart perseus-backend

# Actualizar Frontend
cd /opt/perseus/Frontend
git pull origin main
npm install
npm run build
sudo systemctl restart nginx
```

### Destruir Infraestructura (Después de la Presentación)

```bash
cd terraform
terraform destroy
```

Esto eliminará TODOS los recursos en DigitalOcean y dejará de cobrar.

**⚠️ ADVERTENCIA**: Esto es irreversible. Asegúrate de tener backup de todo antes.

## Costos

### Droplet
- **s-1vcpu-1gb**: $6/mes (~$0.009/hora)
- **s-1vcpu-2gb**: $12/mes (~$0.018/hora)
- **s-2vcpu-2gb**: $18/mes (~$0.027/hora)

### Créditos Gratis
Si usas GitHub Student Pack: **$200 GRATIS** por 60 días

### Cálculo para Tesis
Si lo usas 1 mes para presentar: **$6 total**
Con créditos de estudiante: **$0**

## Solución de Problemas

### Error: "Terraform not found"

Instala Terraform siguiendo las instrucciones en [Requisitos Previos](#requisitos-previos)

### Error: "Invalid API token"

Verifica que tu token de DigitalOcean:
- Sea válido y no haya expirado
- Tenga permisos de **Read & Write**
- Esté correctamente copiado (sin espacios)

### Error: "Unable to create droplet"

Posibles causas:
- **Límite de cuenta**: Cuentas nuevas tienen límite de 1-2 droplets
- **Sin saldo**: Verifica que tengas crédito o método de pago válido
- **Región no disponible**: Cambia `droplet_region` a otra región

### Cloud-init no termina

Si después de 15 minutos sigue configurando:

```bash
# Conectarse al servidor
ssh root@TU_IP_PUBLICA

# Ver errores en cloud-init
cat /var/log/cloud-init.log | grep -i error

# Ver estado del servicio del backend
sudo systemctl status perseus-backend

# Ver logs del backend
sudo journalctl -u perseus-backend -n 50
```

### Frontend no carga

```bash
# Verificar que Nginx esté corriendo
sudo systemctl status nginx

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Backend no responde

```bash
# Verificar servicio
sudo systemctl status perseus-backend

# Ver logs
sudo journalctl -u perseus-backend -f

# Reiniciar servicio
sudo systemctl restart perseus-backend
```

## Configurar SSL/HTTPS (Opcional)

Si tienes un dominio:

### 1. Configurar DNS

En tu proveedor de dominio:

```
Tipo    Nombre    Valor
A       @         TU_IP_PUBLICA
A       www       TU_IP_PUBLICA
```

### 2. Actualizar terraform.tfvars

Descomentar y configurar:
```hcl
domain_name = "tu-dominio.com"
```

### 3. Aplicar cambios

```bash
terraform apply
```

### 4. Instalar certificado SSL

```bash
# Conectarse al servidor
ssh root@TU_IP_PUBLICA

# Instalar certificado Let's Encrypt
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

## Para tu Tesis

### Ventajas de Usar Terraform

1. **Infrastructure as Code (IaC)**
   - Tu infraestructura está versionada en Git
   - Es reproducible y documentada
   - Muestra conocimientos avanzados de DevOps

2. **Automatización Completa**
   - Cero intervención manual
   - Reduce errores humanos
   - Proceso repetible

3. **Muy Profesional**
   - Tecnología usada en empresas reales
   - Demuestra habilidades avanzadas
   - Impresiona en presentaciones

### Documentación para Incluir

1. **Capturas de Pantalla:**
   - Output de `terraform apply`
   - Dashboard de DigitalOcean mostrando el droplet
   - Aplicación funcionando

2. **Diagramas:**
   - Flujo de Terraform → DigitalOcean → Cloud-init
   - Arquitectura de la infraestructura

3. **Código:**
   - Archivos de Terraform (`main.tf`, `variables.tf`)
   - Script `cloud-init.yaml`
   - Script `auto-deploy.sh`

4. **En tu Presentación:**
   > "Implementé Infrastructure as Code usando Terraform para automatizar completamente el despliegue en DigitalOcean. Con un solo comando se crea toda la infraestructura, se configura el servidor y se despliega la aplicación sin intervención manual."

## Mejores Prácticas

### 1. No Subir Credenciales a Git

El archivo `.gitignore` ya está configurado para excluir:
- `terraform.tfvars` (contiene tus credenciales)
- `terraform.tfstate` (contiene IPs y configuración)
- `.terraform/` (archivos internos)

### 2. Usar Variables de Entorno (Alternativa)

En lugar de `terraform.tfvars`, puedes usar variables de entorno:

```bash
export TF_VAR_do_token="tu_token_aqui"
export TF_VAR_huggingface_token="tu_token_aqui"
export TF_VAR_groq_api_key="tu_key_aqui"

terraform apply
```

### 3. State Remoto (Avanzado)

Para proyectos reales, guarda el state en la nube:

```hcl
terraform {
  backend "s3" {
    # Configuración de S3 o Terraform Cloud
  }
}
```

## Recursos Adicionales

- [Documentación de Terraform](https://www.terraform.io/docs)
- [Provider de DigitalOcean](https://registry.terraform.io/providers/digitalocean/digitalocean/latest/docs)
- [Cloud-init Documentation](https://cloudinit.readthedocs.io/)
- [DigitalOcean Tutorials](https://docs.digitalocean.com/)

## Checklist de Despliegue

- [ ] Terraform instalado
- [ ] Cuenta en DigitalOcean creada
- [ ] API Token de DigitalOcean obtenido
- [ ] Proyecto subido a GitHub
- [ ] Credenciales de HuggingFace, Groq/OpenAI listas
- [ ] Ejecutar `./auto-deploy.sh`
- [ ] Esperar 5-10 minutos para cloud-init
- [ ] Verificar aplicación en http://TU_IP
- [ ] Tomar capturas para la tesis

---

**¡Con esto tienes el despliegue MÁS PROFESIONAL posible para tu tesis!**

Si tienes problemas, revisa la sección de [Solución de Problemas](#solución-de-problemas) o los logs en el servidor.
