#!/bin/bash

# This script generates a JWT authentication token that can be used
# to authenticate requests with microservices in the local development 
# environment.
#
# Usage:
#   * With the "test" scope, no practice IDs, and no User ID:
#     generate_dev_auth_token.sh
#   * With the "test" scope, no practice IDs, and with custom User ID:
#     generate_dev_auth_token.sh -u 123
#   * With custom scopes, specific User ID, and some practice IDs:
#     generate_dev_auth_token.sh -s custom_scope_1,custom_scope_2 -u 123 -p 456,768

set -e

LAMBDA_FUNCTION_NAME="el8-dev-auth-internal-generate-token"
LAMBDA_REGION="us-west-2"
AWS_PROFILE="DockerAccess"

# Default token parameters
TOKEN_SCOPES="test" # A comma-separated list
TOKEN_PRACTICE_IDS='' # A comma-separated list
TOKEN_SUB='<test>'
TOKEN_USER_ID=''
TOKEN_HIPPOSPACE="local_$USER" # Default hippospace for local hippo dev

# Parse arguments
while getopts "hs:u:p:i:" opt; do
  case ${opt} in
    h )
      echo "Usage:"
      echo "    $(basename $0) -h"
      echo "    $(basename $0) [-u user_id] [-i hippospace] [-s scope1,scope2,...] [-p practice_id1,practice_id2,...]"
      exit 0
      ;;
    s )
      TOKEN_SCOPES=$OPTARG
      ;;
    u )
      TOKEN_USER_ID=$OPTARG
      ;;
    i ) # 'ippospace
      TOKEN_HIPPOSPACE=$OPTARG
      ;;
    p )
      TOKEN_PRACTICE_IDS=$OPTARG
      ;;
    * )
     echo "See $(basename $0) -h" 1>&2
     exit 1
     ;;
  esac
done
shift $((OPTIND -1))

# Ensure we're logged in with the profile
aws sts get-caller-identity --profile $AWS_PROFILE > /dev/null 2>&1 || aws sso login --profile $AWS_PROFILE

token_user_id_claim=""
if [[ ! -z "$TOKEN_USER_ID" ]]; then
  token_user_id_claim="\"uid\": $TOKEN_USER_ID,"
fi

token_scopes_no_spaces="${TOKEN_SCOPES// /}"
token_scopes_claim_value="\"${token_scopes_no_spaces//,/\",\"}\""

request_payload=$(cat <<-EOT
{
  "token": {
    "sub": "${TOKEN_SUB}",
    "scopes": [${token_scopes_claim_value}],
    "claims": {
      "aud": "api://applications",
      ${token_user_id_claim}
      "practice_ids": [$TOKEN_PRACTICE_IDS],
      "hsp": "$TOKEN_HIPPOSPACE"
    }
  }
}
EOT
)

lambda_output_filename=$(mktemp -u)
trap "rm -f $lambda_output_filename" EXIT # Ensure the temp file is deleted

aws lambda invoke \
  --region $LAMBDA_REGION \
  --profile $AWS_PROFILE \
  --function-name $LAMBDA_FUNCTION_NAME \
  --payload "$request_payload" \
  --cli-binary-format raw-in-base64-out \
  $lambda_output_filename > /dev/null

cat $lambda_output_filename | jq -r '.access_token'