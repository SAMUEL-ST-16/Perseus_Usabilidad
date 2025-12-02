# Outputs de Terraform - Información después del despliegue

output "droplet_ip" {
  description = "IP pública del droplet"
  value       = digitalocean_droplet.perseus.ipv4_address
}

output "droplet_id" {
  description = "ID del droplet"
  value       = digitalocean_droplet.perseus.id
}

output "droplet_name" {
  description = "Nombre del droplet"
  value       = digitalocean_droplet.perseus.name
}

output "frontend_url" {
  description = "URL del frontend"
  value       = "http://${digitalocean_droplet.perseus.ipv4_address}"
}

output "backend_docs_url" {
  description = "URL de la documentación del backend (Swagger)"
  value       = "http://${digitalocean_droplet.perseus.ipv4_address}/api/requirements/docs"
}

output "health_check_url" {
  description = "URL del health check"
  value       = "http://${digitalocean_droplet.perseus.ipv4_address}/health"
}

output "ssh_command" {
  description = "Comando para conectarse por SSH"
  value       = "ssh root@${digitalocean_droplet.perseus.ipv4_address}"
}

output "deployment_status" {
  description = "Estado del despliegue"
  value = <<-EOT

  ================================================
    ✅ DROPLET CREADO EXITOSAMENTE
  ================================================

  📋 INFORMACIÓN:
    - IP Pública: ${digitalocean_droplet.perseus.ipv4_address}
    - Nombre: ${digitalocean_droplet.perseus.name}
    - Región: ${var.droplet_region}
    - Tamaño: ${var.droplet_size}

  🌐 URLS DE ACCESO:
    - Frontend: http://${digitalocean_droplet.perseus.ipv4_address}
    - Backend Docs: http://${digitalocean_droplet.perseus.ipv4_address}/api/requirements/docs
    - Health Check: http://${digitalocean_droplet.perseus.ipv4_address}/health

  🔧 CONECTARSE POR SSH:
    ssh root@${digitalocean_droplet.perseus.ipv4_address}

  ⏱️  IMPORTANTE:
    El droplet está siendo configurado automáticamente.
    Espera 5-10 minutos para que cloud-init termine.

    Para ver el progreso:
    ssh root@${digitalocean_droplet.perseus.ipv4_address} "tail -f /var/log/cloud-init-output.log"

  ================================================
  EOT
}
