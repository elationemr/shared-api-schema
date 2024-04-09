output "service_role_arn" {
  description = "ARN of the service account role"
  value       = try(module.application[0].service_role_arn, "")
}
