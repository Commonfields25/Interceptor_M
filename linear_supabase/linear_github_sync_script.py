#!/usr/bin/env python3
"""
Linear GitHub Sync Script
Synchronise les issues GitHub avec Linear pour le projet Interceptor_M
"""

import os
import sys
import json
import logging
import hashlib
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('linear_sync.log')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()


@dataclass
class LinearConfig:
    """Configuration Linear"""
    api_key: str
    team_id: str
    workspace_id: str
    api_url: str = "https://api.linear.app/graphql"
    
    @classmethod
    def from_env(cls) -> 'LinearConfig':
        """Charge la config depuis les variables d'environnement"""
        api_key = os.getenv("LINEAR_API_KEY")
        if not api_key:
            raise ValueError("LINEAR_API_KEY manquant dans l'environnement")
        
        return cls(
            api_key=api_key,
            team_id=os.getenv("LINEAR_TEAM_ID", "INTERCEPTOR-TEAM"),
            workspace_id=os.getenv("LINEAR_WORKSPACE_ID", "")
        )


@dataclass
class GitHubConfig:
    """Configuration GitHub"""
    token: str
    owner: str
    repo: str
    api_url: str = "https://api.github.com"
    
    @classmethod
    def from_env(cls) -> 'GitHubConfig':
        """Charge la config depuis les variables d'environnement"""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN manquant dans l'environnement")
        
        return cls(
            token=token,
            owner=os.getenv("GITHUB_OWNER", "Commonfields25"),
            repo=os.getenv("GITHUB_REPO", "Interceptor_M")
        )


class RateLimiter:
    """Gestion du rate limiting"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
    
    def wait_if_needed(self):
        """Attend si nécessaire pour éviter le rate limiting"""
        now = datetime.now().timestamp()
        self.requests = [r for r in self.requests if now - r < self.window_seconds]
        
        if len(self.requests) >= self.max_requests:
            wait_time = self.window_seconds - (now - self.requests[0])
            if wait_time > 0:
                logger.warning(f"Rate limit atteint. Attente de {wait_time:.1f}s")
                import time
                time.sleep(wait_time)
        
        self.requests.append(now)


class LinearAPIClient:
    """Client pour l'API Linear"""
    
    def __init__(self, config: LinearConfig):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
    
    def _execute(self, query: str, variables: dict = None) -> dict:
        """Exécute une requête GraphQL"""
        rate_limiter.wait_if_needed()
        
        response = requests.post(
            self.config.api_url,
            headers=self.headers,
            json={"query": query, "variables": variables or {}},
            timeout=30
        )
        
        if response.status_code == 429:
            logger.warning("Rate limit Linear atteint")
            import time
            time.sleep(60)
            return self._execute(query, variables)
        
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            logger.error(f"Erreurs GraphQL: {data['errors']}")
            raise Exception(f"Erreur GraphQL: {data['errors']}")
        
        return data.get("data", {})
    
    def create_issue(self, title: str, description: str, label_ids: list = None, 
                    assignee_id: str = None, priority: int = 0) -> Optional[str]:
        """Crée une issue dans Linear"""
        
        mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                }
            }
        }
        """
        
        variables = {
            "input": {
                "teamId": self.config.team_id,
                "title": title,
                "body": description,
                "priority": priority
            }
        }
        
        if label_ids:
            variables["input"]["labelIds"] = label_ids
        
        if assignee_id:
            variables["input"]["assigneeId"] = assignee_id
        
        try:
            data = self._execute(mutation, variables)
            if data.get("issueCreate", {}).get("success"):
                identifier = data["issueCreate"]["issue"]["identifier"]
                logger.info(f"✅ Issue Linear créée: {identifier}")
                return identifier
        except Exception as e:
            logger.error(f"❌ Erreur création issue: {e}")
        
        return None
    
    def get_issues(self, status: str = None) -> list:
        """Récupère les issues existantes"""
        
        query = """
        query GetIssues($teamId: String!) {
            issues((first: 100, filter: {team: {id: {eq: $teamId}}}) {
                nodes {
                    id
                    identifier
                    title
                    state {
                        name
                    }
                }
            }
        }
        """
        
        try:
            data = self._execute(query, {"teamId": self.config.team_id})
            return data.get("issues", {}).get("nodes", [])
        except Exception as e:
            logger.error(f"Erreur récupération issues: {e}")
            return []


class GitHubAPIClient:
    """Client pour l'API GitHub"""
    
    def __init__(self, config: GitHubConfig):
        self.config = config
        self.headers = {
            "Authorization": f"token {config.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.rate_limiter = RateLimiter(max_requests=50, window_seconds=60)
    
    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Requête GET"""
        self.rate_limiter.wait_if_needed()
        
        response = requests.get(
            f"{self.config.api_url}/{endpoint}",
            headers=self.headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 403:
            logger.warning("Rate limit GitHub atteint")
            reset_time = response.headers.get("X-RateLimit-Reset", 0)
            import time
            wait_seconds = int(reset_time) - int(time.time()) + 5
            if wait_seconds > 0:
                logger.info(f"Attente rate limit: {wait_seconds}s")
                time.sleep(wait_seconds)
                return self._get(endpoint, params)
        
        response.raise_for_status()
        return response.json()
    
    def get_issues(self, state: str = "open") -> list:
        """Récupère les issues GitHub"""
        issues = []
        page = 1
        
        while True:
            data = self._get(
                f"repos/{self.config.owner}/{self.config.repo}/issues",
                params={"state": state, "per_page": 100, "page": page}
            )
            
            if not data:
                break
            
            issues.extend(data)
            
            if len(data) < 100:
                break
            
            page += 1
        
        logger.info(f"Récupéré {len(issues)} issues GitHub")
        return issues


def create_hash(title: str) -> str:
    """Génère un hash pour identifier les issues"""
    return hashlib.md5(title.encode()).hexdigest()[:12]


def get_linear_labels(linear_client: LinearAPIClient) -> dict:
    """Récupère les labels Linear existants"""
    
    query = """
    query GetLabels($teamId: String!) {
        labels(first: 50, filter: {team: {id: {eq: $teamId}}}) {
            nodes {
                id
                name
            }
        }
    }
    """
    
    try:
        data = linear_client._execute(query, {"teamId": linear_client.config.team_id})
        labels = data.get("labels", {}).get("nodes", [])
        return {label["name"]: label["id"] for label in labels}
    except Exception as e:
        logger.error(f"Erreur récupération labels: {e}")
        return {}


def map_github_to_linear_label(label_name: str) -> str:
    """Mappe les labels GitHub aux labels Linear"""
    
    mapping = {
        "bug": "bug",
        "enhancement": "feature",
        "documentation": "documentation",
        "help wanted": "help-wanted",
        "good first issue": "good-first-issue",
        "priority: high": "sprint-p1",
        "priority: critical": "sprint-p1",
        "rl-pipeline": "rl-pipeline",
        "simulation": "simulation"
    }
    
    label_lower = label_name.lower()
    return mapping.get(label_lower, label_name.lower())


def sync_issues(linear_client: GitHubConfig, github_client: GitHubConfig, dry_run: bool = False):
    """Synchronise les issues GitHub vers Linear"""
    
    logger.info("🚀 Démarrage de la synchronisation GitHub → Linear")
    
    # Récupère les issues GitHub
    github_issues = github_client.get_issues(state="open")
    
    # Récupère les labels Linear
    linear_labels = get_linear_labels(linear_client)
    logger.info(f"Labels Linear disponibles: {list(linear_labels.keys())}")
    
    # Filtre les issues (ignore les PRs)
    github_issues = [i for i in github_issues if "pull_request" not in i]
    
    synced_count = 0
    skipped_count = 0
    
    for issue in github_issues:
        title = issue.get("title", "")
        body = issue.get("body", "") or ""
        labels = [l["name"] for l in issue.get("labels", [])]
        issue_url = issue.get("html_url", "")
        
        # Mappe les labels
        linear_label_ids = []
        for label in labels:
            linear_label_name = map_github_to_linear_label(label)
            if linear_label_name in linear_labels:
                linear_label_ids.append(linear_labels[linear_label_name])
            else:
                logger.warning(f"Label GitHub '{label}' non trouvé dans Linear")
        
        # Description avec référence GitHub
        full_description = f"""
## 📌 GitHub Issue
**URL:** {issue_url}

---

{body}

---
*Synchronisé depuis GitHub le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Crée l'issue dans Linear
        if not dry_run:
            identifier = linear_client.create_issue(
                title=title,
                description=full_description,
                label_ids=linear_label_ids,
                priority=2  # Medium par défaut
            )
            
            if identifier:
                synced_count += 1
            else:
                skipped_count += 1
        else:
            logger.info(f"[DRY-RUN] Créerait: {title}")
            synced_count += 1
    
    logger.info(f"""
╔════════════════════════════════════════╗
║     Synchronisation terminée            ║
╠════════════════════════════════════════╣
║  ✅ Synchronisées: {synced_count}               ║
║  ⚠️  Ignorées: {skipped_count}                  ║
╚════════════════════════════════════════╝
""")


def create_linear_labels_from_github(linear_client: LinearAPIClient, github_client: GitHubAPIClient):
    """Crée les labels Linear depuis GitHub"""
    
    logger.info("📋 Synchronisation des labels GitHub → Linear")
    
    github_issues = github_client.get_issues()
    all_labels = set()
    
    for issue in github_issues:
        for label in issue.get("labels", []):
            all_labels.add(label["name"])
    
    logger.info(f"Labels GitHub trouvés: {all_labels}")
    
    # Note: La création de labels nécessite des permissions admin


def main():
    """Point d'entrée principal"""
    
    parser = argparse.ArgumentParser(description="Sync GitHub Issues to Linear")
    parser.add_argument("--dry-run", action="store_true", help="Mode simulation")
    parser.add_argument("--sync-labels", action="store_true", help="Sync labels")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbose")
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Charge la configuration
        linear_config = LinearConfig.from_env()
        github_config = GitHubConfig.from_env()
        
        # Crée les clients
        linear_client = LinearAPIClient(linear_config)
        github_client = GitHubAPIClient(github_config)
        
        # Synchronise
        if args.sync_labels:
            create_linear_labels_from_github(linear_client, github_client)
        
        sync_issues(linear_client, github_client, dry_run=args.dry_run)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Vérifiez les variables d'environnement:")
        logger.error("  - LINEAR_API_KEY")
        logger.error("  - LINEAR_TEAM_ID")
        logger.error("  - GITHUB_TOKEN")
        logger.error("  - GITHUB_OWNER")
        logger.error("  - GITHUB_REPO")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


import argparse  # Ajout pour les arguments CLI

if __name__ == "__main__":
    main()
