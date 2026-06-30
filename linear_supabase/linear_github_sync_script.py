import os
import requests
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_TEAM_ID = os.getenv("LINEAR_TEAM_ID")
REPO_OWNER = "Commonfields25"
REPO_NAME = "Interceptor_M"

# Headers pour les requêtes
GITHUB_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

LINEAR_HEADERS = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json"
}

# URL de base
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
LINEAR_API_URL = "https://api.linear.app/graphql"

# Requête GraphQL pour créer une tâche dans Linear
CREATE_LINEAR_ISSUE_MUTATION = """
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      title
      url
    }
  }
}
"""

def fetch_github_issues():
    """Récupérer les issues depuis GitHub."""
    response = requests.get(GITHUB_API_URL, headers=GITHUB_HEADERS)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération des issues GitHub: {response.status_code}")
        return []
    return response.json()

def create_linear_issue(title, description, agent_id=None):
    """Créer une tâche dans Linear."""
    variables = {
        "input": {
            "title": title,
            "description": description,
            "teamId": LINEAR_TEAM_ID,
            "labels": [{"name": agent_id}] if agent_id else []
        }
    }

    payload = {
        "query": CREATE_LINEAR_ISSUE_MUTATION,
        "variables": variables
    }

    response = requests.post(LINEAR_API_URL, headers=LINEAR_HEADERS, json=payload)
    if response.status_code != 200:
        print(f"Erreur lors de la création de la tâche Linear: {response.status_code}")
        return None

    result = response.json()
    if result.get("errors"):
        print(f"Erreur GraphQL: {result['errors']}")
        return None

    return result.get("data", {}).get("issueCreate", {}).get("issue")

def sync_github_to_linear():
    """Synchroniser les issues GitHub vers Linear."""
    issues = fetch_github_issues()
    if not issues:
        print("Aucune issue trouvée sur GitHub.")
        return

    for issue in issues:
        title = issue.get("title", "Sans titre")
        description = issue.get("body", "")
        labels = issue.get("labels", [])
        agent_id = None

        # Extraire l'agent depuis les labels (ex: "agent:E3")
        for label in labels:
            label_name = label.get("name", "")
            if label_name.startswith("agent:"):
                agent_id = label_name.split(":")[1]
                break

        # Créer la tâche dans Linear
        linear_issue = create_linear_issue(title, description, agent_id)
        if linear_issue:
            print(f"Tâche créée dans Linear: {linear_issue.get('title')} (URL: {linear_issue.get('url')})")
        else:
            print(f"Échec de la création de la tâche: {title}")

if __name__ == "__main__":
    print("Début de la synchronisation GitHub → Linear...")
    sync_github_to_linear()
    print("Synchronisation terminée.")
