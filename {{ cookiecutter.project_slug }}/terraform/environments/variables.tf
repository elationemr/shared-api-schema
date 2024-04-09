variable "argo_branch" {
  default     = "main"
  description = "The branch that ArgoCD should monitor."
  type        = string
}

variable "container_image" {
  description = "The full pod container image with a tag."
  type        = string
  # Setting a fake default value for the variable to ensure the
  # TF workspace can be destroyed during a service tear down without
  # having to set all the variables.
  default = "image:tag"
}
