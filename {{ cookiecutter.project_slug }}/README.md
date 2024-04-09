# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Address
{% if cookiecutter.ingress_traffic_type == "none" -%}
The service was created with `ingress_traffic_type` set to `none`. It is not available outside of the K8s cluster.
{% else -%}
{%- set address_suffix = "internal" if cookiecutter.ingress_traffic_type == "internal" else "el8.io" -%}
The service is deployed at:
* Dev: https://{{ cookiecutter.project_slug }}-dev.el8-dev-services.{{ address_suffix }}/
* Stage: https://{{ cookiecutter.project_slug }}-stage.el8-stage-services.{{ address_suffix }}/
* Sandbox: https://{{ cookiecutter.project_slug }}-sandbox.el8-sandbox-services.{{ address_suffix }}/
* Production: https://{{ cookiecutter.project_slug }}-production.el8-production-services.{{ address_suffix }}/
{%- endif %}

To change the ingress traffic type, set the `ingress_traffic_type` variable in [terraform/automation/setup.tf](terraform/automation/setup.tf) and [terraform/environment/setup.tf](terraform/environment/setup.tf) to `internal`, `external`, or `none`.

The service dashboards are available at:

* [Dev](https://el8.grafana.net/d/ffov1RkVk/services-single-pane-dashboard?orgId=1&refresh=30s&var-Namespace={{ cookiecutter.project_slug }}-dev&var-datasource=el8-dev-services)
* [Stage](https://el8.grafana.net/d/ffov1RkVk/services-single-pane-dashboard?orgId=1&refresh=30s&var-Namespace={{ cookiecutter.project_slug }}-stage&var-datasource=el8-stage-services)
* [Sandbox](https://el8.grafana.net/d/ffov1RkVk/services-single-pane-dashboard?orgId=1&refresh=30s&var-Namespace={{ cookiecutter.project_slug }}-sandbox&var-datasource=el8-sandbox-services)
* [Production](https://el8.grafana.net/d/ffov1RkVk/services-single-pane-dashboard?orgId=1&refresh=30s&var-Namespace={{ cookiecutter.project_slug }}-production&var-datasource=el8-production-services)

## Logs

You can find logs in the global Graylog. Okta credentials and 2FA are used to login.

* [Graylog](https://graylog.el8-global-services.internal/)

Useful attributes to query on include:
* source
* k8s_namespace_name
* cluster_name

## Argo CD

You can review service health and deployment status using Argo Cd. Okta credentials and 2FA are used to login.

Your Argo CD dashboards are available at: 

* [Dev](https://argocd.el8-dev-services.internal/)
* [Demo](https://argocd.el8-demo-services.internal/)
* [Stage](https://argocd.el8-stage-services.internal/)
* [Sandbox](https://argocd.el8-sandbox-services.internal/)
* [Production](https://argocd.el8-production-services.internal/)


## Local development

### CodeArtifact authentication

```sh
source ./scripts/aws_login.sh
```

### Docker build
```sh
DOCKER_BUILDKIT=1 docker build --secret id=CODEARTIFACT_AUTH_TOKEN,env=CODEARTIFACT_AUTH_TOKEN .
```

### Install dependencies (for development)
```sh
poetry install
```

### Install pre-commit
This will add commit hooks that will validate formatting, linting, type checking, and unit tests pass w/ enough coverage

```sh
brew install pre-commit
pre-commit install
```

### Running Uvicorn with auto-reload
```sh
poetry run uvicorn app.main:app --port 8080 --reload --reload-dir app
```
or just
```sh
uvicorn app.main:app --port 8080 --reload --reload-dir app
```
if you're already inside `poetry shell`.

### Authentication
To generate an authentication token for local development purposes:
```sh
./scripts/generate_dev_auth_token.sh
```

### Custom Scripts

[Poe The Poet](https://poethepoet.natn.io/index.html) makes it easier to run custom poetry commands


### Unit-testing
```sh
poetry run pytest
```
OR
```sh
poetry run pytest --cov app --cov-report xml --cov-report term
```
This will print the coverage details to the terminal and create a `coverage.xml`
with coverage details. It can be used with the
[VSCode Coverage Gutters add-on](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters)

### Formatting
```sh
poetry run black .
```

### Linting
```sh
poetry run flake8
```

### Type checking
```sh
poetry run mypy
```

## After deploy integration tests
The [integration](integration) directory contains `pytest` tests that are automatically executed after every deployment.

### Running the integration tests locally
The tests assume the service is running and is available at http://localhost:8080 (configured [here](integration/settings.py))
```sh
poetry run pytest integration
```
NOTE: the `SERVICE_URL` environment variable value will be set to the appropriate service URL for each environment during deployment.

### Disabling/enabling the integration tests during deployments
The tests can be enabled or disabled by modifying the `after_deploy_job_config.enabled` Terraform local variable in [setup.tf](terraform/environments/setup.tf).

## Deploying to environments
To enable/disable environments the service should be deployed to change the `DEPLOY_TO_ENVIRONMENTS` variable in [main_branch_deployment.yml](.github/workflows/main_branch_deployment.yml#L14).
