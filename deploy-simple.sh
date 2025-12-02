#!/bin/bash
#
# 🚀 Script Simplificado de Despliegue - Perseus
# Este script usa las credenciales ya configuradas en terraform/terraform.tfvars
#

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════╗
║                                                  ║
║   🚀 Perseus - Despliegue Simplificado        ║
║                                                  ║
╚══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Validar Terraform
echo -e "${YELLOW}[1/5] Validando Terraform...${NC}"
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}ERROR: Terraform no está instalado.${NC}"
    echo "Instala desde: https://www.terraform.io/downloads"
    exit 1
fi
echo -e "${GREEN}✓ Terraform instalado${NC}"
echo ""

# Generar SSH Key si no existe
echo -e "${YELLOW}[2/5] Generando SSH key...${NC}"
SSH_KEY_PATH="$HOME/.ssh/perseus_terraform"

if [ ! -f "$SSH_KEY_PATH" ]; then
    echo "Generando nueva SSH key..."
    ssh-keygen -t rsa -b 4096 -f "$SSH_KEY_PATH" -N "" -C "perseus-terraform"
    echo -e "${GREEN}✓ SSH key generada${NC}"
else
    echo -e "${GREEN}✓ SSH key ya existe${NC}"
fi

SSH_PUBLIC_KEY=$(cat "$SSH_KEY_PATH.pub")
echo ""

# Solicitar URL del repositorio
echo -e "${YELLOW}[3/5] Configuración del repositorio...${NC}"
echo ""
read -p "Ingresa la URL de tu repositorio de GitHub: " GITHUB_REPO

# Actualizar terraform.tfvars con la SSH key y repo
cd terraform

# Crear copia de respaldo (compatible con Linux y macOS)
cp terraform.tfvars terraform.tfvars.bak

# Reemplazar placeholder de SSH key y GitHub repo
sed -i "s|ssh_public_key = \"PLACEHOLDER - Se reemplazará por auto-deploy.sh\"|ssh_public_key = \"$SSH_PUBLIC_KEY\"|" terraform.tfvars
sed -i "s|github_repo = \"https://github.com/TU_USUARIO/Perseus.git\"|github_repo = \"$GITHUB_REPO\"|" terraform.tfvars

# Eliminar copia de respaldo si todo salió bien
rm -f terraform.tfvars.bak

echo -e "${GREEN}✓ Configuración actualizada${NC}"
echo ""

# Terraform init
echo -e "${YELLOW}[4/5] Inicializando Terraform...${NC}"
terraform init
echo -e "${GREEN}✓ Terraform inicializado${NC}"
echo ""

# Terraform plan
echo -e "${YELLOW}Generando plan de despliegue...${NC}"
terraform plan
echo ""

# Confirmar
echo -e "${BLUE}══════════════════════════════════════${NC}"
echo -e "${YELLOW}¿Continuar con el despliegue?${NC}"
echo ""
echo "Esto creará:"
echo "  - Droplet en DigitalOcean (región: nyc1)"
echo "  - Firewall configurado"
echo "  - Aplicación desplegada automáticamente"
echo ""
echo "Costo estimado: ~\$6/mes"
echo ""
read -p "Continuar? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${RED}Despliegue cancelado.${NC}"
    exit 0
fi

# Terraform apply
echo ""
echo -e "${YELLOW}[5/5] Creando infraestructura...${NC}"
echo "Esto tomará 2-3 minutos..."
echo ""
terraform apply -auto-approve

echo ""
echo -e "${GREEN}✓ Infraestructura creada${NC}"
echo ""

# Mostrar información
DROPLET_IP=$(terraform output -raw droplet_ip)

echo ""
terraform output deployment_status
echo ""

echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════╗
║                                                  ║
║       ✅ DESPLIEGUE COMPLETADO EXITOSAMENTE      ║
║                                                  ║
╚══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${GREEN}📋 INFORMACIÓN IMPORTANTE:${NC}"
echo ""
echo "1. La aplicación está siendo configurada automáticamente"
echo "   (toma 5-10 minutos)"
echo ""
echo "2. Para ver el progreso:"
echo -e "   ${CYAN}ssh -i $SSH_KEY_PATH root@$DROPLET_IP \"tail -f /var/log/cloud-init-output.log\"${NC}"
echo ""
echo "3. Una vez listo, accede a:"
echo -e "   ${CYAN}http://$DROPLET_IP${NC}"
echo ""
echo "4. Backend Docs:"
echo -e "   ${CYAN}http://$DROPLET_IP/api/requirements/docs${NC}"
echo ""
echo -e "${YELLOW}⏱️  ESPERA 5-10 MINUTOS para que termine la configuración${NC}"
echo ""
