##############################
# Environment-wide variables #
##############################

# User `local.region` for region

locals {
  project               = "el8"
  service_name          = "{{ cookiecutter.project_slug }}"
  workspace_environment = split("_", terraform.workspace)[1]
  environment_config    = data.terraform_remote_state.meta.outputs.environment_config[local.workspace_environment]
  region                = local.environment_config.region
}

##############################
# Ease-of-use AWS properties #
##############################
data "aws_caller_identity" "current" {} # Account ID

################
# Remote State #
################
data "terraform_remote_state" "meta" {
  backend = "remote"

  config = {
    organization = "elation"
    workspaces = {
      name = "el8-meta"
    }
  }
}
