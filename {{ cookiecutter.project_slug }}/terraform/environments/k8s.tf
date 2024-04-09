module "application" {
  count = local.is_automation_workspace ? 0 : 1 # Only in non-automation workspaces

  source                     = "git::git@github.com:elationemr/terraform-modules.git//argocd_application/service?ref=argocd_application_service_v1"
  branch_name                = var.argo_branch
  service_name               = local.service_name
  environment                = local.workspace_environment
  cluster_name               = local.cluster_name
  labels                     = local.common_labels
  container_image_repository = split(":", var.container_image)[0]
  container_image_tag        = local.image_tag

  # Service
  default_replica_count       = local.default_replica_count
  deployment_strategy         = local.deployment_strategy
  create_service_account_role = local.use_service_account
  environment_variables       = local.environment_variables
  secrets                     = local.secrets
  dapr                        = local.dapr
  resources_requests          = local.resources_requests
  resources_limits            = local.resources_limits
  keda                        = local.keda

  # Helm
  helm_chart_revision = local.helm_chart_revision

  # Ingress
  ingress_traffic_type               = local.ingress_traffic_type
  ingress_rules                      = local.ingress_rules
  ingress_frontend_gateway_endpoints = local.ingress_frontend_gateway_endpoints

  # Deployed tests
  after_deploy_job = merge(local.after_deploy_job_config, {
    container_image_repository = split(":", var.container_image)[0]
    container_image_tag        = join("-", [split(":", var.container_image)[1], "tests"])
  })
}
