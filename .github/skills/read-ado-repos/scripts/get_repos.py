"""
Fetch Git repositories from an Azure DevOps project using the currently
logged-in Azure CLI credentials (az login).

Usage:
    python get_repos.py <ado_org> <ado_project>

Prerequisites:
    pip install requests
    az login  (or az login --use-device-code)

Note:
    If the ADO organization belongs to a specific Entra tenant, pass the
    tenant ID as the optional third argument. List available tenants with:
    az account list -o table
"""

import sys
import json
import subprocess
import requests

# ADO resource GUID — required scope for Azure DevOps REST API
#ADO_RESOURCE = "499b84ac-1321-427f-aa17-267ca6975798"
API_VERSION = "7.1"


def get_token() -> str:
    """Obtain a bearer token from the active az login session.

    Calls az CLI via subprocess with shell=True so that az.cmd is resolved
    correctly on Windows without requiring the azure-identity package.

  
    """

    cmd = (
        f"az account get-access-token"
        f" --query accessToken"        
        f" --output tsv"
    )

    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"az account get-access-token failed.\n"
            f"Make sure you are logged in with 'az login'.\n"
            f"Error: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def fetch_repos(org: str, project: str, token: str) -> list[dict]:
    """Call the ADO Git repositories API and return a list of repos."""
    url = f"https://dev.azure.com/{org}/{project}/_apis/git/repositories"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = {"api-version": API_VERSION}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    repos = response.json().get("value", [])
    return [
        {
            "name": repo["name"],
            "description": repo.get("description", ""),
            "url": repo["remoteUrl"],
        }
        for repo in repos
    ]


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python get_repos.py <ado_org> <ado_project> ", file=sys.stderr)
        sys.exit(1)

    org = sys.argv[1]
    project = sys.argv[2]
    
    print(f"Fetching repositories for organization: {org}, project: {project}")

    token = get_token()
    repos = fetch_repos(org, project, token)

    print(json.dumps(repos, indent=2))


if __name__ == "__main__":
    main()
