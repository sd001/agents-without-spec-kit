#!/bin/bash
# Fetch Git repositories from an Azure DevOps project using the currently
# logged-in Azure CLI credentials (az login).
#
# Usage:
#   bash get_repos.sh <ado_org> <ado_project>
#
# Prerequisites:
#   az login  (or az login --use-device-code)
#   jq        (for JSON formatting — optional, falls back to raw output)

set -euo pipefail

ADO_ORG="${1:?Usage: get_repos.sh <ado_org> <ado_project>}"
ADO_PROJECT="${2:?Usage: get_repos.sh <ado_org> <ado_project>}"

# ADO resource GUID — required scope for Azure DevOps REST API
ADO_RESOURCE="499b84ac-1321-427f-aa17-267ca6975798"
API_VERSION="7.1"

echo "Fetching repositories for organization: ${ADO_ORG}, project: ${ADO_PROJECT}"

# Obtain a short-lived bearer token from the active az login session
TOKEN=$(az account get-access-token \
  --resource "${ADO_RESOURCE}" \
  --query accessToken \
  --output tsv)

URL="https://dev.azure.com/${ADO_ORG}/$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "${ADO_PROJECT}")/_apis/git/repositories?api-version=${API_VERSION}"

RESPONSE=$(curl -s \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${URL}")

# Pretty-print and extract name / description / remoteUrl
if command -v jq &>/dev/null; then
  echo "${RESPONSE}" | jq '[.value[] | {name: .name, description: (.description // ""), url: .remoteUrl}]'
else
  echo "${RESPONSE}"
fi
