#!/bin/bash
#
# 🚀 Perseus - Despliegue Completamente Automatizado con Terraform
#
# Este script automatiza TODO el proceso de despliegue:
#   1. Valida que terraform esté instalado
#   2. Pide credenciales de forma interactiva
#   3. Genera SSH key si no existe
#   4. Crea archivo terraform.tfvars automáticamente
#   5. Ejecuta terraform para crear droplet
#   6. Cloud-init configura el servidor automáticamente
#   7. La app queda desplegada sin intervención manual
#
# Uso:
#   chmod +x auto-deploy.sh
#   ./auto-deploy.sh
#

set -e  # Detener si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🚀 Perseus - Despliegue Automatizado con Terraform  ║
║                                                          ║
║   Infrastructure as Code (IaC) para DigitalOcean        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ==================================================
# PASO 1: Validar Terraform instalado
# ==================================================
echo -e "${YELLOW}[1/8] Validando instalación de Terraform...${NC}"

if ! command -v terraform &> /dev/null; then
    echo -e "${RED}ERROR: Terraform no está instalado.${NC}"
    echo ""
    echo "Instala Terraform desde: https://www.terraform.io/downloads"
    echo ""
    echo "Instrucciones rápidas:"
    echo ""
    echo "  macOS (con Homebrew):"
    echo "    brew tap hashicorp/tap"
    echo "    brew install hashicorp/tap/terraform"
    echo ""
    echo "  Linux (Ubuntu/Debian):"
    echo "    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg"
    echo "    echo \"deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com \$(lsb_release -cs) main\" | sudo tee /etc/apt/sources.list.d/hashicorp.list"
    echo "    sudo apt update && sudo apt install terraform"
    echo ""
    echo "  Windows (con Chocolatey):"
    echo "    choco install terraform"
    echo ""
    exit 1
fi

TERRAFORM_VERSION=$(terraform version | head -n 1)
echo -e "${GREEN}✓ Terraform instalado: $TERRAFORM_VERSION${NC}"
echo ""

# ==================================================
# PASO 2: Generar SSH Key si no existe
# ==================================================
echo -e "${YELLOW}[2/8] Verificando SSH key...${NC}"

SSH_KEY_PATH="$HOME/.ssh/perseus_terraform"

if [ ! -f "$SSH_KEY_PATH" ]; then
    echo "No se encontró clave SSH. Generando una nueva..."
    ssh-keygen -t rsa -b 4096 -f "$SSH_KEY_PATH" -N "" -C "perseus-terraform"
    echo -e "${GREEN}✓ SSH key generada en: $SSH_KEY_PATH${NC}"
else
    echo -e "${GREEN}✓ SSH key encontrada: $SSH_KEY_PATH${NC}"
fi

SSH_PUBLIC_KEY=$(cat "$SSH_KEY_PATH.pub")
echo ""

# ==================================================
# PASO 3: Recopilar credenciales
# ==================================================
echo -e "${YELLOW}[3/8] Recopilando credenciales...${NC}"
echo ""
echo -e "${CYAN}Necesito algunas credenciales para continuar.${NC}"
echo -e "${CYAN}Presiona Enter para usar valores por defecto donde aplique.${NC}"
echo ""

# DigitalOcean Token
echo -e "${BLUE}──────────────────────────────────────${NC}"
echo -e "${GREEN}1. DigitalOcean API Token${NC}"
echo "   Obtén uno en: https://cloud.digitalocean.com/account/api/tokens"
echo "   Click en 'Generate New Token' → Nombre: 'Perseus' → Read & Write"
echo ""
read -p "DigitalOcean Token: " DO_TOKEN

# GitHub Repo
echo ""
echo -e "${BLUE}──────────────────────────────────────${NC}"
echo -e "${GREEN}2. Repositorio de GitHub${NC}"
echo "   Debe ser la URL completa de tu repositorio"
echo "   Ejemplo: https://github.com/tu-usuario/Perseus.git"
echo ""
read -p "URL del repositorio: " GITHUB_REPO

# HuggingFace Token
echo ""
echo -e "${BLUE}──────────────────────────────────────${NC}"
echo -e "${GREEN}3. HuggingFace Token (OBLIGATORIO)${NC}"
echo "   Obtén uno en: https://huggingface.co/settings/tokens"
echo ""
read -p "HuggingFace Token: " HF_TOKEN

# Groq API Key
echo ""
echo -e "${BLUE}──────────────────────────────────────${NC}"
echo -e "${GREEN}4. Groq API Key (GRATIS - RECOMENDADO)${NC}"
echo "   Obtén uno gratis en: https://console.groq.com/keys"
echo "   Presiona Enter para omitir"
echo ""
read -p "Groq API Key: " GROQ_KEY

# OpenAI API Key
if [ -z "$GROQ_KEY" ]; then
    echo ""
    echo -e "${BLUE}──────────────────────────────────────${NC}"
    echo -e "${GREEN}5. OpenAI API Key (OPCIONAL - DE PAGO)${NC}"
    echo "   Solo si prefieres usar OpenAI en lugar de Groq"
    echo "   Presiona Enter para omitir"
    echo ""
    read -p "OpenAI API Key: " OPENAI_KEY
else
    OPENAI_KEY=""
fi

# Configuración del droplet
echo ""
echo -e "${BLUE}──────────────────────────────────────${NC}"
echo -e "${GREEN}6. Configuración del Droplet${NC}"
echo ""

# Región
echo "Región del droplet (más cercana es más rápido):"
echo "  nyc1 = New York"
echo "  sfo3 = San Francisco"
echo "  lon1 = London"
echo "  fra1 = Frankfurt"
echo "  sgp1 = Singapore"
read -p "Región [nyc1]: " DROPLET_REGION
DROPLET_REGION=${DROPLET_REGION:-nyc1}

# Tamaño
echo ""
echo "Tamaño del droplet:"
echo "  s-1vcpu-1gb = \$6/mes (1GB RAM)"
echo "  s-1vcpu-2gb = \$12/mes (2GB RAM - recomendado)"
echo "  s-2vcpu-2gb = \$18/mes (más potencia)"
read -p "Tamaño [s-1vcpu-2gb]: " DROPLET_SIZE
DROPLET_SIZE=${DROPLET_SIZE:-s-1vcpu-2gb}

# Modelos
echo ""
echo -e "${BLUE}──────────────────────────────────────${NC}"
echo -e "${GREEN}7. Modelos de HuggingFace${NC}"
echo ""
read -p "Modelo binario [SamuelSoto7/PerseusV8_Binario]: " BINARY_MODEL
BINARY_MODEL=${BINARY_MODEL:-SamuelSoto7/PerseusV8_Binario}

read -p "Modelo multiclase [SamuelSoto7/PerseusV2_Multiclass]: " MULTICLASS_MODEL
MULTICLASS_MODEL=${MULTICLASS_MODEL:-SamuelSoto7/PerseusV2_Multiclass}

# Determinar LLM provider
if [ ! -z "$GROQ_KEY" ]; then
    LLM_PROVIDER="groq"
elif [ ! -z "$OPENAI_KEY" ]; then
    LLM_PROVIDER="openai"
else
    LLM_PROVIDER="none"
fi

echo ""
echo -e "${GREEN}✓ Credenciales recopiladas${NC}"
echo ""

# ==================================================
# PASO 4: Crear archivo terraform.tfvars
# ==================================================
echo -e "${YELLOW}[4/8] Generando archivo terraform.tfvars...${NC}"

cd terraform

cat > terraform.tfvars <<EOF
# Archivo generado automáticamente por auto-deploy.sh
# Fecha: $(date)

# DigitalOcean Configuration
do_token       = "$DO_TOKEN"
ssh_public_key = "$SSH_PUBLIC_KEY"
droplet_region = "$DROPLET_REGION"
droplet_size   = "$DROPLET_SIZE"

# GitHub Repository
github_repo = "$GITHUB_REPO"

# HuggingFace Configuration
huggingface_token     = "$HF_TOKEN"
binary_model_name     = "$BINARY_MODEL"
multiclass_model_name = "$MULTICLASS_MODEL"

# LLM Provider Configuration
llm_provider   = "$LLM_PROVIDER"
groq_api_key   = "$GROQ_KEY"
openai_api_key = "$OPENAI_KEY"
EOF

echo -e "${GREEN}✓ terraform.tfvars creado${NC}"
echo ""

# ==================================================
# PASO 5: Terraform Init
# ==================================================
echo -e "${YELLOW}[5/8] Inicializando Terraform...${NC}"
terraform init

echo -e "${GREEN}✓ Terraform inicializado${NC}"
echo ""

# ==================================================
# PASO 6: Terraform Plan
# ==================================================
echo -e "${YELLOW}[6/8] Generando plan de despliegue...${NC}"
echo ""
terraform plan

echo ""
echo -e "${GREEN}✓ Plan generado${NC}"
echo ""

# ==================================================
# PASO 7: Confirmar despliegue
# ==================================================
echo -e "${BLUE}══════════════════════════════════════${NC}"
echo -e "${YELLOW}¿Deseas continuar con el despliegue?${NC}"
echo ""
echo "Esto va a:"
echo "  - Crear un droplet en DigitalOcean ($DROPLET_SIZE en $DROPLET_REGION)"
echo "  - Configurar firewall"
echo "  - Instalar y desplegar la aplicación automáticamente"
echo ""
echo "Costo estimado: ~\$6/mes (puedes destruirlo después)"
echo ""
read -p "Continuar? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${RED}Despliegue cancelado.${NC}"
    exit 0
fi

# ==================================================
# PASO 8: Terraform Apply
# ==================================================
echo ""
echo -e "${YELLOW}[7/8] Creando infraestructura en DigitalOcean...${NC}"
echo ""
echo "Esto tomará 2-3 minutos..."
echo ""

terraform apply -auto-approve

echo ""
echo -e "${GREEN}✓ Infraestructura creada${NC}"
echo ""

# ==================================================
# PASO 9: Mostrar información final
# ==================================================
echo -e "${YELLOW}[8/8] Obteniendo información del despliegue...${NC}"
echo ""

# Guardar outputs
DROPLET_IP=$(terraform output -raw droplet_ip)
FRONTEND_URL=$(terraform output -raw frontend_url)
BACKEND_URL=$(terraform output -raw backend_docs_url)
SSH_COMMAND=$(terraform output -raw ssh_command)

echo ""
terraform output deployment_status
echo ""

# ==================================================
# RESUMEN FINAL
# ==================================================
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║            ✅ DESPLIEGUE COMPLETADO EXITOSAMENTE         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${GREEN}📋 INFORMACIÓN IMPORTANTE:${NC}"
echo ""
echo "1. El droplet está siendo configurado automáticamente"
echo "   Esto toma aproximadamente 5-10 minutos"
echo ""
echo "2. Para ver el progreso en tiempo real:"
echo -e "   ${CYAN}$SSH_COMMAND \"tail -f /var/log/cloud-init-output.log\"${NC}"
echo ""
echo "3. Una vez que cloud-init termine, accede a:"
echo -e "   ${CYAN}$FRONTEND_URL${NC}"
echo ""
echo "4. Guarda la clave SSH para acceder al servidor:"
echo -e "   ${CYAN}$SSH_KEY_PATH${NC}"
echo ""
echo -e "${GREEN}📝 COMANDOS ÚTILES:${NC}"
echo ""
echo "  Conectarse al servidor:"
echo -e "    ${CYAN}$SSH_COMMAND${NC}"
echo ""
echo "  Ver logs del backend:"
echo -e "    ${CYAN}$SSH_COMMAND \"sudo journalctl -u perseus-backend -f\"${NC}"
echo ""
echo "  Destruir infraestructura (después de la presentación):"
echo -e "    ${CYAN}cd terraform && terraform destroy${NC}"
echo ""
echo -e "${YELLOW}⏱️  ESPERA 5-10 MINUTOS para que la configuración termine${NC}"
echo ""
echo -e "${GREEN}¡Listo! Tu aplicación estará disponible pronto en $FRONTEND_URL${NC}"
echo ""
