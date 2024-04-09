#module "eks_discworld_grafana" {
#  source         = "git::git@github.com:elationemr/terraform-modules.git//grafana/discworld?ref=RM-26676-cluster-grafana" # TODO: Fix url
#  eks_cluster_name = local.cluster_name
#  prometheus_url = module.eks_discworld.prometheus_endpoint # TODO: Get promethus URL
#  region        = var.region
#}
