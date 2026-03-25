---
name: read-ado-repos
description: Fetch list of Git repositories from an Azure DevOps organization and project using logged-in Azure CLI credentials
---

# When to use
Use this skill when the user asks for:
- list of repositories in Azure DevOps (ADO)
- scan repositories in an ADO organization or project
- get repo names from Azure DevOps for analysis

# Prerequisites
- Azure CLI installed (`az` on PATH)
- Logged in: `az login`  (or `az login --use-device-code` for headless environments)
- Python: `pip install azure-identity requests`

# Inputs
- ado_org     — Azure DevOps organization name (e.g. `myorg`)
- ado_project — Azure DevOps project name (e.g. `MyProject`)

# Authentication
Uses the active Azure CLI session — NO PAT tokens or hardcoded credentials required.

- Python script: `azure-identity` → `AzureCliCredential` reads the cached az login session.
- Shell script:  `az account get-access-token` obtains a short-lived bearer token.

Both scripts target the ADO REST resource:
`499b84ac-1321-427f-aa17-267ca6975798`

# Steps

1. Verify `az account show` returns the expected tenant/subscription
2. Run the appropriate script:
   - Python: `python scripts/get_repos.py <ado_org> <ado_project>`
   - Shell:  `bash scripts/get_repos.sh <ado_org> <ado_project>`
3. Parse the JSON response
4. Extract:
   - repo name
   - description
   - remote URL
5. Return repository list in JSON

# Output

[
  {
    "name": "repo1",
    "description": "Sample repo",
    "url": "https://dev.azure.com/myorg/MyProject/_git/repo1"
  }
]
