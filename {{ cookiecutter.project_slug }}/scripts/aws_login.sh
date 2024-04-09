#!/bin/bash

aws --profile DockerAccess sts get-caller-identity --no-cli-pager >/dev/null 2>&1 || aws sso login --profile DockerAccess >/dev/null 2>&1 
aws ecr get-login-password --profile DockerAccess --region us-west-2 | docker login --username AWS --password-stdin 570488747013.dkr.ecr.us-west-2.amazonaws.com > /dev/null 2>&1 
export CODEARTIFACT_AUTH_TOKEN="$(aws codeartifact get-authorization-token --domain el8-global --domain-owner 570488747013 --query authorizationToken --output text --profile DockerAccess --region us-west-2)" 
export POETRY_HTTP_BASIC_EL8_PASSWORD=$CODEARTIFACT_AUTH_TOKEN