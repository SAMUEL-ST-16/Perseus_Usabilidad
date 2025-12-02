terraform {
  required_version = ">= 1.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Provider de DigitalOcean
provider "digitalocean" {
  token = var.do_token
}

# SSH Key para acceder al droplet
resource "digitalocean_ssh_key" "default" {
  name       = "perseus-terraform-key"
  public_key = var.ssh_public_key
}

# Droplet (servidor) en DigitalOcean
resource "digitalocean_droplet" "perseus" {
  # Nombre del servidor
  name   = "perseus-server"

  # Región (puedes cambiar según tu ubicación)
  # nyc1 = New York, sfo3 = San Francisco, lon1 = London, fra1 = Frankfurt
  region = var.droplet_region

  # Tamaño del servidor
  # s-1vcpu-1gb = $6/mes (1GB RAM)
  # s-1vcpu-2gb = $12/mes (2GB RAM - recomendado)
  # s-2vcpu-2gb = $18/mes (2 vCPUs, 2GB RAM)
  size   = var.droplet_size

  # Imagen del sistema operativo
  image  = "ubuntu-22-04-x64"

  # SSH key para acceso
  ssh_keys = [digitalocean_ssh_key.default.id]

  # Script de inicialización (cloud-init)
  # Este script se ejecuta automáticamente cuando el droplet se crea
  user_data = templatefile("${path.module}/cloud-init.yaml", {
    github_repo         = var.github_repo
    hf_token           = var.huggingface_token
    groq_key           = var.groq_api_key
    openai_key         = var.openai_api_key
    binary_model       = var.binary_model_name
    multiclass_model   = var.multiclass_model_name
    llm_provider       = var.llm_provider
  })

  # Tags para organizar
  tags = ["perseus", "terraform", "production"]

  # Esperar a que cloud-init termine
  lifecycle {
    create_before_destroy = true
  }
}

# Firewall para seguridad
resource "digitalocean_firewall" "perseus" {
  name = "perseus-firewall"

  droplet_ids = [digitalocean_droplet.perseus.id]

  # Reglas de entrada (inbound)
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]  # SSH desde cualquier IP
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]  # HTTP
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]  # HTTPS
  }

  # Reglas de salida (outbound) - permitir todo
  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

# Registrar dominio opcional (si tienes uno)
# Descomenta si tienes un dominio registrado
# resource "digitalocean_domain" "perseus" {
#   name       = var.domain_name
#   ip_address = digitalocean_droplet.perseus.ipv4_address
# }
