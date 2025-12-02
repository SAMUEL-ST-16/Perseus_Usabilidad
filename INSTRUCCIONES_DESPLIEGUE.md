# 🚀 Instrucciones de Despliegue - PASO A PASO

## ✅ Credenciales YA Configuradas

Ya configuré todos tus tokens en `terraform/terraform.tfvars`:
- ✅ DigitalOcean Token
- ✅ HuggingFace Token
- ✅ Groq API Key
- ✅ OpenAI API Key
- ✅ Modelos configurados

**Solo falta:**
1. Subir el proyecto a GitHub
2. Ejecutar el script de despliegue

---

## Paso 1: Crear Repositorio en GitHub

### Opción A: Un Solo Repositorio (RECOMENDADO)

1. Ve a https://github.com/new
2. Nombre del repo: `Perseus`
3. Descripción: `Sistema de Extracción de Requisitos de Usabilidad con IA`
4. Visibilidad: **Public** (para que el droplet pueda clonarlo)
5. **NO marques** "Add a README file"
6. Click en **"Create repository"**

### Opción B: Dos Repositorios Separados

Si prefieres tener Backend y Frontend separados:
1. Crea repo: `Perseus-Backend` (Public)
2. Crea repo: `Perseus-Frontend` (Public)

**IMPORTANTE:** Si eliges 2 repos, necesitarás modificar el cloud-init.

---

## Paso 2: Subir el Código a GitHub

### Si elegiste UN SOLO repositorio:

```bash
# Navega a la carpeta del proyecto
cd "C:\Users\SAMUEL\Documents\XII CICLO\Desarrollo de Tesis Final\Perseus"

# Inicializar git (si no está inicializado)
git init

# Agregar TODOS los archivos
git add .

# Crear commit inicial
git commit -m "Initial commit - Perseus with Terraform deployment"

# Agregar remote (REEMPLAZA TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/Perseus.git

# Renombrar rama a main
git branch -M main

# Push a GitHub
git push -u origin main
```

### Si elegiste DOS repositorios:

**Backend:**
```bash
cd "C:\Users\SAMUEL\Documents\XII CICLO\Desarrollo de Tesis Final\Perseus\Backend"
git init
git add .
git commit -m "Initial commit - Backend"
git remote add origin https://github.com/TU_USUARIO/Perseus-Backend.git
git branch -M main
git push -u origin main
```

**Frontend:**
```bash
cd "C:\Users\SAMUEL\Documents\XII CICLO\Desarrollo de Tesis Final\Perseus\Frontend"
git init
git add .
git commit -m "Initial commit - Frontend"
git remote add origin https://github.com/TU_USUARIO/Perseus-Frontend.git
git branch -M main
git push -u origin main
```

---

## Paso 3: Actualizar URL del Repositorio

Si creaste **UN SOLO repo**, edita `terraform/terraform.tfvars`:

```bash
# Abre el archivo
notepad terraform\terraform.tfvars

# Busca la línea:
github_repo = "https://github.com/TU_USUARIO/Perseus.git"

# Reemplaza TU_USUARIO con tu usuario real de GitHub
# Ejemplo:
github_repo = "https://github.com/SamuelSoto7/Perseus.git"

# Guarda el archivo
```

Si creaste **DOS repos**, necesitas modificar `terraform/cloud-init.yaml` (te puedo ayudar después).

---

## Paso 4: Instalar Terraform

### Windows (con Chocolatey)

```powershell
# Instalar Chocolatey si no lo tienes
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Terraform
choco install terraform
```

### Windows (Manual)

1. Descarga desde: https://www.terraform.io/downloads
2. Descomprime el archivo
3. Mueve `terraform.exe` a `C:\Windows\System32\`
4. Abre nueva terminal y verifica: `terraform version`

### Linux/Mac

```bash
# Linux
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# macOS
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

---

## Paso 5: Ejecutar el Despliegue

### Desde Windows (Git Bash o WSL)

```bash
# Navega a la carpeta del proyecto
cd "C:\Users\SAMUEL\Documents\XII CICLO\Desarrollo de Tesis Final\Perseus"

# Da permisos de ejecución al script
chmod +x deploy-simple.sh

# Ejecuta el script
./deploy-simple.sh
```

### Desde PowerShell (Alternativa)

Si no tienes Git Bash, ejecuta manualmente:

```powershell
# Navega a terraform
cd "C:\Users\SAMUEL\Documents\XII CICLO\Desarrollo de Tesis Final\Perseus\terraform"

# Inicializar Terraform
terraform init

# Ver plan
terraform plan

# Aplicar (crear infraestructura)
terraform apply
```

---

## Paso 6: Esperar y Verificar

### Durante el Despliegue

1. **Terraform** creará el droplet (2-3 minutos)
2. **Cloud-init** configurará todo automáticamente (5-10 minutos)

### Ver el Progreso

Una vez que Terraform termine, te dará la IP del droplet. Para ver el progreso:

```bash
# Reemplaza TU_IP con la IP que te dio Terraform
ssh root@TU_IP "tail -f /var/log/cloud-init-output.log"
```

### Verificar que Funcione

Después de 10 minutos, accede a:

- **Frontend**: http://TU_IP
- **Backend Docs**: http://TU_IP/api/requirements/docs
- **Health Check**: http://TU_IP/health

---

## 🎯 Resumen del Proceso

```
1. Crear repo en GitHub (5 min)
   ↓
2. Subir código (git push) (2 min)
   ↓
3. Actualizar terraform.tfvars con URL del repo (1 min)
   ↓
4. Instalar Terraform (5 min)
   ↓
5. Ejecutar deploy-simple.sh (2 min)
   ↓
6. Esperar configuración automática (10 min)
   ↓
7. ¡App funcionando! 🎉
```

**Total: ~25 minutos** (la mayoría es espera automática)

---

## ⚠️ Notas Importantes

### Seguridad

El archivo `terraform/terraform.tfvars` contiene tus credenciales REALES.
**YA está en .gitignore**, así que NO se subirá a GitHub.

Verifica que esté en .gitignore:
```bash
cat terraform/.gitignore | grep terraform.tfvars
```

Deberías ver:
```
terraform.tfvars
```

### Repositorio Privado vs Público

Si haces el repo PRIVADO, necesitas:
1. Crear un Personal Access Token en GitHub
2. Modificar cloud-init para usar: `https://TOKEN@github.com/usuario/repo.git`

**RECOMENDACIÓN:** Usa repo PÚBLICO para simplicidad.

### Destruir Infraestructura

Después de la presentación de tu tesis:

```bash
cd terraform
terraform destroy
```

Esto elimina TODO de DigitalOcean y deja de cobrar.

---

## 🆘 Si Algo Sale Mal

### Error: "Terraform not found"
Instala Terraform (Paso 4)

### Error: "Invalid credentials"
Verifica que los tokens en `terraform.tfvars` sean correctos

### Error: "Repository not found"
- Verifica que el repo sea PÚBLICO
- Verifica que la URL en terraform.tfvars sea correcta

### Cloud-init no termina
Espera 15 minutos. Si sigue sin funcionar:
```bash
ssh root@TU_IP
cat /var/log/cloud-init.log | grep -i error
```

---

## 📞 Contacto

Si tienes problemas, revisa:
1. `TERRAFORM_DEPLOY.md` - Guía completa
2. `QUICKSTART.md` - Resumen rápido
3. Logs del servidor: `ssh root@TU_IP`

---

**¡Todo está listo! Solo sigue los pasos y en 25 minutos tendrás tu app desplegada!** 🚀
