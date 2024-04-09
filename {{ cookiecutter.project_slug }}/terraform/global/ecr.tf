module "ecr_repo" {
  source             = "git::git@github.com:elationemr/terraform-modules.git//ecr"
  name               = local.service_name
  description        = "Image for the ${local.service_name} service."
  mutable_image_tags = true

  # Required for service-bootsrapper to be able to deprovision workspaces
  # https://elationhealth.atlassian.net/browse/RM-38479
  force_delete = true
}
