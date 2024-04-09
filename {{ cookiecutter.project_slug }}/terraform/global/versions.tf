####################
# Terraform Config #
####################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  required_version = "~> {{ cookiecutter.terraform_version }}"

  cloud {
    organization = "elation"
    workspaces {
      tags = ["{{ cookiecutter.project_slug }}"]
    }
  }
}

###################
# Provider Config #
###################

provider "aws" {
  region = local.region
  default_tags {
    tags = {
      Project     = local.project
      Environment = local.workspace_environment
      Service     = local.service_name
    }
  }
}
