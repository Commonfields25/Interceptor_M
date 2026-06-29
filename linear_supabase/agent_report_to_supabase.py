#!/usr/bin/env python3
"""
Agent Report to Supabase
Permet aux agents de soumettre leurs rapports quotidiens au format standardisé
Format: [AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS]
"""

import os
import sys
import re
import json
import logging
from datetime import datetime, date
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print as rprint

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()
load_dotenv()


class ReportStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    REVIEWED = "reviewed"
    ARCHIVED = "archived"


@dataclass
class AgentReport:
    """Représentation d'un rapport d'agent"""
    agent_id: str
    report_date: date
    actions_taken: str
    blocages: Optional[str] = None
    besoins: Optional[str] = None
    status: ReportStatus = ReportStatus.SUBMITTED
    raw_format: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire pour Supabase"""
        return {
            "agent_id": self.agent_id,
            "report_date": self.report_date.isoformat(),
            "actions_taken": self.actions_taken,
            "blocages": self.blocages,
            "besoins": self.besoins,
            "status": self.status.value,
            "raw_format": self.raw_format
        }
    
    @classmethod
    def from_formatted_string(cls, text: str) -> Optional['AgentReport']:
        """
        Parse le format: [AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS]
        Les champs BLOCAGES et BESOINS sont optionnels et peuvent être vides
        """
        # Normalise les séparateurs (supporte aussi tabulations)
        text = text.strip()
        
        # Pattern pour le format complet
        pattern = r'^\[([A-Z0-9]+)\]\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)\s*(?:\|(.*?))?(?:\s*\|(.*))?$'
        match = re.match(pattern, text, re.DOTALL)
        
        if not match:
            # Essaye le format alternatif sans crochet
            pattern2 = r'^([A-Z0-9]+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.+?)(?:\s*\|(.*?))?(?:\s*\|(.*))?$'
            match = re.match(pattern2, text, re.DOTALL)
        
        if not match:
            return None
        
        groups = match.groups()
        agent_id = groups[0].strip()
        
        try:
            report_date = datetime.strptime(groups[1].strip(), "%Y-%m-%d").date()
        except ValueError:
            logger.error(f"Date invalide: {groups[1]}")
            return None
        
        actions = groups[2].strip()
        blocages = groups[3].strip() if groups[3] else None
        besoins = groups[4].strip() if groups[4] else None
        
        # Nettoie les valeurs nulles
        if blocages in (None, "", "null", "none"):
            blocages = None
        if besoins in (None, "", "null", "none"):
            besoins = None
        
        return cls(
            agent_id=agent_id,
            report_date=report_date,
            actions_taken=actions,
            blocages=blocages,
            besoins=besoins,
            status=ReportStatus.SUBMITTED,
            raw_format=text
        )


class SupabaseClient:
    """Client pour l'API Supabase"""
    
    def __init__(self, url: str = None, key: str = None):
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL et SUPABASE_KEY sont requis")
        
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """Requête HTTP generic"""
        url = f"{self.url}/rest/v1/{endpoint}"
        
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )
            
            if response.status_code >= 400:
                logger.error(f"Erreur {response.status_code}: {response.text}")
                response.raise_for_status()
            
            return response.json() if response.text else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur de requête: {e}")
            raise
    
    def get_agents(self) -> list:
        """Récupère la liste des agents"""
        return self._request("GET", "agents?select=*&order=agent_id")
    
    def check_agent_exists(self, agent_id: str) -> bool:
        """Vérifie si un agent existe"""
        result = self._request(
            "GET", 
            f"agents?agent_id=eq.{agent_id}&select=agent_id"
        )
        return len(result) > 0
    
    def get_reports_by_agent(self, agent_id: str, limit: int = 10) -> list:
        """Récupère les rapports d'un agent"""
        return self._request(
            "GET",
            f"agent_reports?agent_id=eq.{agent_id}&select=*&order=report_date.desc&limit={limit}"
        )
    
    def get_report_by_date(self, agent_id: str, report_date: date) -> Optional[dict]:
        """Récupère un rapport spécifique"""
        result = self._request(
            "GET",
            f"agent_reports?agent_id=eq.{agent_id}&report_date=eq.{report_date.isoformat()}&select=*"
        )
        return result[0] if result else None
    
    def submit_report(self, report: AgentReport, upsert: bool = True) -> dict:
        """Soumet un rapport à Supabase"""
        
        data = report.to_dict()
        
        if upsert:
            data["on_conflict"] = "agent_id,report_date"
            params = {"conflict": "agent_id,report_date"}
            return self._request("POST", "agent_reports?on_conflict=agent_id,report_date", data, params)
        else:
            return self._request("POST", "agent_reports", data)
    
    def update_report(self, report_id: str, data: dict) -> dict:
        """Met à jour un rapport existant"""
        return self._request("PATCH", f"agent_reports?id=eq.{report_id}", data)
    
    def get_blocages(self, hours_threshold: int = 2) -> list:
        """Récupère les blocages récents"""
        threshold_time = datetime.utcnow().timestamp() - (hours_threshold * 3600)
        
        return self._request(
            "GET",
            f"agent_reports?blocages=not.is.null&select=*,agents(agent_name)&order=created_at.desc"
        )


class ReportValidator:
    """Validation des rapports"""
    
    VALID_AGENT_IDS = [
        "E1", "E2", "E3",  # Exploration
        "D1", "D2", "D3",  # Discrimination
        "AM",               # Auto-Modélisation
        "AC",               # Auto-Correction
        "G1", "G2",         # Gouvernance
        "SIM",              # Simulation
    ]
    
    @classmethod
    def validate_agent_id(cls, agent_id: str) -> bool:
        """Valide l'ID de l'agent"""
        return agent_id.upper() in cls.VALID_AGENT_IDS
    
    @classmethod
    def validate_date(cls, date_str: str) -> bool:
        """Valide le format de date"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @classmethod
    def validate_report(cls, text: str) -> tuple[bool, Optional[str]]:
        """
        Valide le rapport complet
        Retourne (valide, message_erreur)
        """
        if not text or not text.strip():
            return False, "Le rapport ne peut pas être vide"
        
        # Vérifie le format de base
        if '|' not in text:
            return False, "Le rapport doit utiliser le format [AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS]"
        
        parts = text.split('|')
        if len(parts) < 3:
            return False, "Le rapport doit contenir au moins: [AGENT]|[DATE]|[ACTIONS]"
        
        # Valide l'agent
        agent = parts[0].strip().strip('[]')
        if not cls.validate_agent_id(agent):
            return False, f"Agent ID '{agent}' invalide. Valides: {', '.join(cls.VALID_AGENT_IDS)}"
        
        # Valide la date
        date_str = parts[1].strip()
        if not cls.validate_date(date_str):
            return False, f"Format de date '{date_str}' invalide. Utilisez YYYY-MM-DD"
        
        # Valide les actions
        actions = parts[2].strip()
        if len(actions) < 10:
            return False, "La description des actions doit contenir au moins 10 caractères"
        
        return True, None


def interactive_report_submission():
    """Interface interactive pour soumettre un rapport"""
    
    console.print("\n[bold cyan]📝 Rapport Quotidien - Agent Interceptor_M[/bold cyan]\n")
    
    # Sélection de l'agent
    agent_id = Prompt.ask(
        "ID de l'agent",
        choices=["E1", "E2", "E3", "D1", "D2", "D3", "AM", "AC", "G1", "G2", "SIM"],
        default="E1"
    )
    
    # Date (défaut: aujourd'hui)
    default_date = datetime.now().strftime("%Y-%m-%d")
    date_str = Prompt.ask("Date (YYYY-MM-DD)", default=default_date)
    
    if not ReportValidator.validate_date(date_str):
        console.print("[red]❌ Date invalide![/red]")
        sys.exit(1)
    
    # Actions
    console.print("\n[yellow]📋 Décrivez les actions realizadas aujourd'hui:[/yellow]")
    actions = Prompt.ask("Actions", multiline=True)
    
    # Blocages
    console.print("\n[red]🚫 Avez-vous des blocages? (laisser vide si aucun)[/red]")
    blocages = Prompt.ask("Blocages", default="", multiline=True)
    if blocages.lower() in ('', 'aucun', 'none', 'null'):
        blocages = None
    
    # Besoins
    console.print("\n[blue]📦 Avez-vous des besoins? (laisser vide si aucun)[/blue]")
    besoins = Prompt.ask("Besoins", default="", multiline=True)
    if besoins.lower() in ('', 'aucun', 'none', 'null'):
        besoins = None
    
    # Génère le format standard
    raw_format = f"[{agent_id}]|{date_str}|{actions}"
    if blocages:
        raw_format += f"|{blocages}"
    else:
        raw_format += "|"
    if besoins:
        raw_format += f"|{besoins}"
    else:
        raw_format += "|"
    
    # Affiche le résumé
    console.print("\n[bold green]📄 Résumé du rapport:[/bold green]")
    print(raw_format)
    
    if not Confirm.ask("\n[bold]Confirmer la soumission?[/bold]"):
        console.print("[yellow]Rapport annulé.[/yellow]")
        sys.exit(0)
    
    # Crée l'objet rapport
    report = AgentReport(
        agent_id=agent_id,
        report_date=datetime.strptime(date_str, "%Y-%m-%d").date(),
        actions_taken=actions,
        blocages=blocages,
        besoins=besoins,
        status=ReportStatus.SUBMITTED,
        raw_format=raw_format
    )
    
    return report


def display_report_history(agent_id: str, client: SupabaseClient):
    """Affiche l'historique des rapports d'un agent"""
    
    reports = client.get_reports_by_agent(agent_id, limit=10)
    
    if not reports:
        console.print(f"[yellow]Aucun rapport trouvé pour l'agent {agent_id}[/yellow]")
        return
    
    table = Table(title=f"Historique des rapports - Agent {agent_id}")
    table.add_column("Date", style="cyan")
    table.add_column("Statut", style="green")
    table.add_column("Actions (extrait)", style="white")
    table.add_column("Blocages", style="red")
    
    for r in reports:
        actions_preview = r.get("actions_taken", "")[:50] + "..." if len(r.get("actions_taken", "")) > 50 else r.get("actions_taken", "")
        blocages = r.get("blocages", "—") or "—"
        
        table.add_row(
            r.get("report_date", ""),
            r.get("status", ""),
            actions_preview,
            blocages[:30]
        )
    
    console.print(table)


def main():
    """Point d'entrée principal"""
    
    import argparse
    parser = argparse.ArgumentParser(description="Soumission de rapports agents vers Supabase")
    parser.add_argument("--agent", "-a", help="ID de l'agent (E1, E2, etc.)")
    parser.add_argument("--date", "-d", help="Date du rapport (YYYY-MM-DD)")
    parser.add_argument("--actions", help="Actions réalisées")
    parser.add_argument("--blocages", help="Blocages rencontrés")
    parser.add_argument("--besoins", help="Besoins identifiés")
    parser.add_argument("--input-file", "-f", type=argparse.FileType('r'), help="Fichier contenant le rapport formaté")
    parser.add_argument("--history", help="Afficher l'historique des rapports d'un agent")
    parser.add_argument("--interactive", "-i", action="store_true", help="Mode interactif")
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans envoi")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbose")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize Supabase client
        client = SupabaseClient()
        
        # Check if we just want to see history
        if args.history:
            display_report_history(args.history.upper(), client)
            sys.exit(0)
        
        report = None
        
        # Parse input sources
        if args.input_file:
            content = args.input_file.read()
            report = AgentReport.from_formatted_string(content)
            if not report:
                console.print("[red]❌ Format de rapport invalide![/red]")
                console.print("[yellow]Format attendu: [AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS][/yellow]")
                sys.exit(1)
        elif args.interactive or not any([args.agent, args.actions]):
            report = interactive_report_submission()
        else:
            # CLI arguments
            report_date = datetime.strptime(args.date or datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            
            report = AgentReport(
                agent_id=args.agent.upper(),
                report_date=report_date,
                actions_taken=args.actions,
                blocages=args.blocages,
                besoins=args.besoins,
                status=ReportStatus.SUBMITTED
            )
        
        # Validate
        valid, error = ReportValidator.validate_report(report.raw_format or "")
        if not valid and args.input_file:
            console.print(f"[red]❌ Validation échouée: {error}[/red]")
            sys.exit(1)
        
        # Display report
        console.print("\n[bold green]📋 Rapport à soumettre:[/bold green]")
        console.print(f"  Agent: {report.agent_id}")
        console.print(f"  Date: {report.report_date}")
        console.print(f"  Actions: {report.actions_taken[:100]}...")
        if report.blocages:
            console.print(f"  [red]Blocages: {report.blocages}[/red]")
        if report.besoins:
            console.print(f"  [blue]Besoins: {report.besoins}[/blue]")
        
        if args.dry_run:
            console.print("\n[yellow]🔍 Mode DRY-RUN: aucune donnée envoyée[/yellow]")
            sys.exit(0)
        
        # Submit
        result = client.submit_report(report, upsert=True)
        
        if result:
            console.print("\n[bold green]✅ Rapport soumis avec succès![/bold green]")
            
            # Check if blocages were reported - trigger alert info
            if report.blocages:
                console.print("[bold red]⚠️ Blocage détecté! Une alerte sera créée automatiquement.[/bold red]")
        else:
            console.print("[red]❌ Erreur lors de la soumission[/red]")
            sys.exit(1)
        
    except ValueError as e:
        console.print(f"[red]❌ Erreur de configuration: {e}[/red]")
        console.print("[yellow]Vérifiez les variables d'environnement: SUPABASE_URL, SUPABASE_KEY[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Erreur: {e}[/red]")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
