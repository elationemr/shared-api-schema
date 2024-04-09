####################
# Terraform Config #
####################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.8"
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
      Environment = local.environment
      Service     = local.service_name
    }
  }
}

data "aws_eks_cluster" "cluster" {
  name     = local.cluster_name
  provider = aws
}

provider "aws" {
  alias  = "us-west-2"
  region = "us-west-2"
  default_tags {
    tags = {
      Project     = local.project
      Environment = local.environment
      Service     = local.service_name
    }
  }
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.cluster.id, "--region", local.region]
    command     = "aws"
  }
}
