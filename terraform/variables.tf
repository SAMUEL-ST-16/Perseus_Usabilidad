# Variables de Terraform para Perseus

# ========== DigitalOcean Configuration ==========

variable "do_token" {
  description = "DigitalOcean API Token"
  type        = string
  sensitive   = true
}

variable "ssh_public_key" {
  description = "SSH public key para acceder al droplet"
  type        = string
}

variable "droplet_region" {
  description = "Región del droplet (nyc1, sfo3, lon1, fra1, etc.)"
  type        = string
  default     = "nyc1"  # New York por defecto
}

variable "droplet_size" {
  description = "Tamaño del droplet"
  type        = string
  default     = "s-1vcpu-2gb"  # $12/mes - 2GB RAM

  # Otras opciones:
  # s-1vcpu-1gb = $6/mes (1GB RAM)
  # s-2vcpu-2gb = $18/mes (2 vCPUs, 2GB RAM)
}

# ========== GitHub Repository ==========

variable "github_repo" {
  description = "URL del repositorio de GitHub (https://github.com/usuario/repo.git)"
  type        = string
}

# ========== HuggingFace Configuration ==========

variable "huggingface_token" {
  description = "HuggingFace API Token"
  type        = string
  sensitive   = true
}

variable "binary_model_name" {
  description = "Nombre del modelo binario en HuggingFace"
  type        = string
  default     = "SamuelSoto7/PerseusV8_Binario"
}

variable "multiclass_model_name" {
  description = "Nombre del modelo multiclase en HuggingFace"
  type        = string
  default     = "SamuelSoto7/PerseusV2_Multiclass"
}

# ========== LLM Provider Configuration ==========

variable "llm_provider" {
  description = "Proveedor de LLM (groq, openai, none)"
  type        = string
  default     = "groq"

  validation {
    condition     = contains(["groq", "openai", "none"], var.llm_provider)
    error_message = "llm_provider debe ser: groq, openai, o none"
  }
}

variable "groq_api_key" {
  description = "Groq API Key (gratis)"
  type        = string
  default     = ""
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API Key (de pago)"
  type        = string
  default     = ""
  sensitive   = true
}

# ========== Optional Domain ==========

variable "domain_name" {
  description = "Nombre de dominio (opcional)"
  type        = string
  default     = ""
}
