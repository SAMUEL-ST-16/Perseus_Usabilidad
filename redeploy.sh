#!/bin/bash
#
# 🔄 Script de Re-Despliegue Rápido - Perseus
# Destruye el servidor actual y lo vuelve a crear con la configuración actualizada
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
║   🔄 Perseus - Re-Despliegue Rápido          ║
║                                                  ║
╚══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}Este script va a:${NC}"
echo "  1. Destruir el servidor actual"
echo "  2. Limpiar caché de Terraform"
echo "  3. Re-desplegar con la configuración actualizada"
echo ""
echo -e "${RED}ADVERTENCIA: Esto eliminará el servidor actual${NC}"
echo ""
read -p "¿Continuar? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${RED}Re-despliegue cancelado.${NC}"
    exit 0
fi

cd terraform

# Paso 1: Destruir servidor actual
echo ""
echo -e "${YELLOW}[1/4] Destruyendo servidor actual...${NC}"
terraform destroy -auto-approve || echo "No hay infraestructura para destruir"
echo -e "${GREEN}✓ Servidor destruido${NC}"

# Paso 2: Limpiar caché
echo ""
echo -e "${YELLOW}[2/4] Limpiando caché de Terraform...${NC}"
rm -rf .terraform/
rm -f .terraform.lock.hcl
echo -e "${GREEN}✓ Caché limpiado${NC}"

# Paso 3: Inicializar Terraform
echo ""
echo -e "${YELLOW}[3/4] Inicializando Terraform...${NC}"
terraform init
echo -e "${GREEN}✓ Terraform inicializado${NC}"

# Paso 4: Desplegar
echo ""
echo -e "${YELLOW}[4/4] Desplegando servidor con configuración actualizada...${NC}"
echo ""
echo "Esto tomará 2-3 minutos para crear el servidor..."
echo ""
terraform apply -auto-approve

echo ""
echo -e "${GREEN}✓ Servidor creado${NC}"
echo ""

# Obtener información
DROPLET_IP=$(terraform output -raw droplet_ip 2>/dev/null || echo "")

echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════╗
║                                                  ║
║       ✅ SERVIDOR CREADO EXITOSAMENTE           ║
║                                                  ║
╚══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${GREEN}📋 PRÓXIMOS PASOS:${NC}"
echo ""
echo "1. Espera 5-7 minutos para que cloud-init complete la instalación"
echo ""
echo "2. Monitorea el progreso (espera 2 minutos antes de conectarte):"
echo -e "   ${CYAN}ssh -i ~/.ssh/perseus_terraform root@$DROPLET_IP${NC}"
echo ""
echo "3. Ver logs de cloud-init:"
echo -e "   ${CYAN}tail -f /var/log/cloud-init-output.log${NC}"
echo ""
echo "   Deberías ver:"
echo "   - Instalación de Python 3.11"
echo "   - Instalación de Node.js"
echo "   - Clonación del repositorio"
echo "   - 'Reiniciando servidor para completar la instalación...'"
echo "   - [Se cortará la conexión - ESTO ES NORMAL]"
echo ""
echo "4. Espera 1 minuto y reconéctate:"
echo -e "   ${CYAN}ssh -i ~/.ssh/perseus_terraform root@$DROPLET_IP${NC}"
echo ""
echo "5. Verifica que el post-boot se ejecutó:"
echo -e "   ${CYAN}cat /var/log/perseus-post-boot.log${NC}"
echo ""
echo "   Debes ver:"
echo "   ✓ Backend service está habilitado"
echo "   ✓ Nginx service está habilitado"
echo "   ✓ Backend está ACTIVO"
echo "   ✓ Nginx está ACTIVO"
echo ""
echo "6. Accede a la aplicación:"
echo -e "   ${CYAN}http://$DROPLET_IP${NC}"
echo ""
echo -e "${YELLOW}⏱️  TIEMPO TOTAL ESTIMADO: 5-7 minutos${NC}"
echo ""
