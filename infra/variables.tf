variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "home-api"
}

variable "homeassistant_url" {
  description = "Home Assistant URL (e.g., https://your-instance.nabu.casa)"
  type        = string
}

variable "cpu" {
  description = "CPU units for App Runner (256, 512, 1024, 2048, 4096)"
  type        = string
  default     = "256"
}

variable "memory" {
  description = "Memory in MB for App Runner (512, 1024, 2048, 3072, 4096, etc.)"
  type        = string
  default     = "512"
}

variable "custom_domain" {
  description = "Custom domain for the API (e.g., api.home.example.com). Leave empty to skip."
  type        = string
  default     = ""
}
