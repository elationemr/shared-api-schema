# This can be changed to "resource" instead of data and it will
# stop the after_deploy_job from being recreated on every run.
data "aws_lambda_invocation" "integration_test_api_token" {
  count = local.after_deploy_job_enabled ? 1 : 0

  function_name = "el8-${local.environment}-auth-internal-test-generate-token"

  input = jsonencode({
    "token" = {
      "sub"    = "<test>",
      "scopes" = ["test"], # The lambda only allows the 'test' scope
      "claims" = { "aud" = "api://applications", "practice_ids" = [] },
    }
  })
}

locals {
  integration_test_api_token = local.after_deploy_job_enabled ? jsondecode(sensitive(data.aws_lambda_invocation.integration_test_api_token[0].result))["access_token"] : ""
}
