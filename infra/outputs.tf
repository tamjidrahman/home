output "ecr_repository_url" {
  description = "ECR repository URL for pushing Docker images"
  value       = aws_ecr_repository.home_api.repository_url
}

output "apprunner_service_url" {
  description = "App Runner service URL"
  value       = aws_apprunner_service.home_api.service_url
}

output "apprunner_service_arn" {
  description = "App Runner service ARN"
  value       = aws_apprunner_service.home_api.arn
}

output "custom_domain_dns_records" {
  description = "DNS records to add to Route53 for custom domain validation"
  value = var.custom_domain != "" ? {
    target = aws_apprunner_custom_domain_association.home_api[0].dns_target
    validation_records = [
      for record in aws_apprunner_custom_domain_association.home_api[0].certificate_validation_records : {
        name  = record.name
        type  = record.type
        value = record.value
      }
    ]
  } : null
}
