module "service_alerts" {
  count        = local.is_automation_workspace ? 0 : 1
  environment  = local.workspace_environment
  team         = local.common_labels.team
  system       = local.common_labels.system
  cluster_name = local.cluster_name

  source = "git@github.com:elationemr/terraform-modules.git//managed_alert_manager/service_alerts?ref=managed_alert_manager_service_alerts_v1"
  providers = {
    aws = aws.us-west-2
  }
  no_replicas_config = {
    enabled = true
  }
  latency_config = {
    # We disable in non production environments because these alerts require a higher volume of requests to be effective.
    enabled = local.workspace_environment == "production" ? true : false
    # 99% of requests must operate within 100ms.
    slo = 100
  }
  error_burn_rate_config = {
    # We disable in non production environments because these alerts require a higher volume of requests to be effective.
    enabled = local.workspace_environment == "production" ? true : false
    # 99.9% of requests must have successful HTTP responses over a rolling window.
    slo = 0.999
  }
}
