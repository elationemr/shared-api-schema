##############################
# Environment-wide variables #
##############################

# Use `local.environment` for environment

# User `local.region` for region

locals {
  project                 = "el8"
  service_name            = "{{ cookiecutter.project_slug }}"
  workspace_environment   = split("_", terraform.workspace)[1]
  is_automation_workspace = local.workspace_environment == "automation"
  environment             = local.is_automation_workspace ? "dev" : local.workspace_environment
  event_streaming_enabled = contains(["dev", "stage", "sandbox", "production"], local.environment)
  environment_config      = data.terraform_remote_state.meta.outputs.environment_config[local.workspace_environment]
  cluster_name            = local.environment_config.cluster_name
  region                  = local.environment_config.region
  image_tag               = split(":", var.container_image)[1]

  # Service
  common_labels = {
    system                       = "{{ cookiecutter.project_slug }}"
    team                         = "{{ cookiecutter.team_name }}"
    "tags.datadoghq.com/env"     = local.workspace_environment
    "tags.datadoghq.com/service" = local.service_name
    "tags.datadoghq.com/version" = local.image_tag
    # Enables Datadog Cluster Agent to configure the APM library.
    "admission.datadoghq.com/enabled" = true
  }
  use_service_account   = {{ 'true' if cookiecutter.use_service_account == "True" else 'false' }}
  default_replica_count = 1
  deployment_strategy = {
    type = "RollingUpdate"
  }
  environment_variables = {
    # Add extra ENV variables here
    DATADOG_ENABLED = true
    /*
    MY_AWS_RESOURCE_ARN = aws_resource.my_resource.arn
    */
  }
  secrets = {
    # Add AWS Secrets Manager or SSM Parameter Store secrets
    # to be mounted into the service container.
    #
    # NOTE: The service account IAM role must have the
    # secretsmanager:DescribeSecret and secretsmanager:GetSecretValue
    # permissions for the given secret(s).


    # my_secret will be mounted to /var/run/secrets/aws-secrets/my_secret
    # The application needs to source this file in order to access the secret.
    # e.g.
    /*
      ```python
      with open("/var/run/secrets/aws-secrets/my_secret") as f:
        content = f.read()
      ```
    */
    /*
    my_secret = {
      secret   = aws_secretsmanager_secret.my_secret.arn,
      type     = "secretsmanager",
      jmesPath = []
      # Optional list of JSON attributes to extract from the
      # JSON formatted secret and mount as individual files.
      # jmesPath = [
      #   {
      #     path = "my_secret_attribute",
      #     objectAlias = "my_secret_attribute"
      #   }
      #]
    }
    */
  }

   # Dapr
  dapr = {
    enabled = false # set to true to enable

    # See https://docs.dapr.io/reference/arguments-annotations-overview/
    # pod_annotations = {
    #   log-level = "debug"
      # We'll default:
      #   dapr.io/enabled to the enabled flag above
      #   dapr.io/app-id to service name, e.g. my-service
      #   dapr.io/app-port to "8080" (the microservice chart default)
      #   dapr.io/config to the sidecar config below
    # }

    # See https://docs.dapr.io/reference/resource-specs/configuration-schema/#sidecar-format
    # sidecar_config = {
    #   tracing = {
    #    samplingRate = "1"
    #  }
    # }

    # - https://docs.dapr.io/reference/resource-specs/component-schema/
    # - https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-apache-kafka/
    # kafka_pubsub = local.event_streaming_enabled ? [
    #  {
        # Must match pubsub name in app subscription (`@dapr_app.subscribe(pubsub="events",...`).
        # Used as the Component name in k8s: it must be unique within this dapr app.
    #    name = "kafka-pubsub"
        # Doesn't require the secret to be defined in the CSI "secrets" elsewhere in setup.tf.
        # We'll automatically create a k8s synced Secret and generate auth metadata pointing at it.
        # Relies on us following a consistent format for all kafka secrets.
    #    secret_arn = data.aws_secretsmanager_secret.dapr_demo_event_stream_credentials[0].arn
        # See https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-apache-kafka/#spec-metadata-fields
    #    metadata = []
    #  }
    #] : []
  }

  # Keda enabled with default config
  keda = {
    enabled = true
  }

  /*
   For Reasoning behind these limits/requests see:
    https://elationhealth.atlassian.net/wiki/spaces/infra/pages/2344190121/CPU+requests+and+Memory+limits
  */
  resources_requests = {
    cpu    = "500m"
    memory = local.workspace_environment == "production" ? "500Mi" : "300Mi"
  }
  resources_limits = {
    cpu    = null
    memory = local.workspace_environment == "production" ? "500Mi" : "300Mi"
  }

  # Helm
  helm_chart_revision = "v1"

  # Ingress
  ingress_traffic_type = "{{ cookiecutter.ingress_traffic_type }}"
  ingress_rules = [{
    match    = "Host(`{hostname}`)"
    priority = 10
  }]

  # Defines a list of routes that should be reachable from the Hippo front-end JavaScript code
  # via XHR requests and authenticated using the Hippo session cookie.
  # NOTE: ingress_traffic_type must be set to "internal" in order to use this.
  ingress_frontend_gateway_endpoints = [
    /*
    # Will be available at `GET /gw/{{ cookiecutter.project_slug }}/frontend/exposed/route/{param}` in Hippo.
    {
      method      = "GET",
      path_prefix = "/frontend/exposed/route/{param}"
    }
    */
  ]

  # After Deploy integration tests
  # Set after_deploy_job_enabled=false if you don't want to run the after deploy
  # integration tests. It can also be enabled/disabled only for
  # specific environments. For example:
  #   after_deploy_job_enabled = local.workspace_environment !== "production"
  after_deploy_job_enabled = true
  after_deploy_job_config = {
    enabled = local.after_deploy_job_enabled
    command = ["poetry", "run", "pytest", "integration"]

    # Job environment variables.
    # {service_url} will be replaced with the K8s internal URL
    # for the deployed service.
    environment_variables = {
      SERVICE_URL    = "{service_url}"
      API_AUTH_TOKEN = local.integration_test_api_token
    }
  }
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

data "terraform_remote_state" "global" {
  backend = "remote"

  config = {
    organization = "elation"
    workspaces = {
      name = "${local.service_name}_global"
    }
  }
}

# Special case: referencing the "dev" workspace from the "automation" workspace
# only as the "automation" resources are deployed to the dev environment.
data "terraform_remote_state" "dev" {
  count   = local.is_automation_workspace ? 1 : 0
  backend = "remote"

  config = {
    organization = "elation"
    workspaces = {
      name = "${local.service_name}_dev"
    }
  }
}
