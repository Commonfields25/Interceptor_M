#!/usr/bin/env python3
"""
Supabase Alerts Monitor
Surveille Supabase pour les blocages > 2 heures et envoie des alertes
"""

import os
import sys
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from threading import Thread, Event
import schedule

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('supabase_alerts.log')
    ]
)
logger = logging.getLogger(__name__)

console = Console()
load_dotenv()


class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    BLOCKAGE = "BLOCKAGE"
    METRIC_THRESHOLD = "METRIC_THRESHOLD"
    TASK_OVERDUE = "TASK_OVERDUE"
    SIMULATION_FAILED = "SIMULATION_FAILED"
    AGENT_INACTIVE = "AGENT_INACTIVE"


@dataclass
class Alert:
    """Représentation d'une alerte"""
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    agent_id: Optional[str] = None
    source_id: Optional[str] = None
    metadata: Optional[Dict] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "title": self.title,
            "message": self.message,
            "agent_id": self.agent_id,
            "source_id": self.source_id,
            "metadata": self.metadata or {}
        }


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
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Requête HTTP générique"""
        url = f"{self.url}/rest/v1/{endpoint}"
        
        response = requests.request(
            method,
            url,
            headers=self.headers,
            json=data,
            timeout=30
        )
        
        if response.status_code >= 400:
            logger.error(f"Erreur {response.status_code}: {response.text}")
            response.raise_for_status()
        
        return response.json() if response.text else {}
    
    def get_active_blocages(self, hours_threshold: int = 2) -> List[Dict]:
        """Récupère les blocages actifs depuis la vue v_active_blocages"""
        threshold_time = (datetime.utcnow() - timedelta(hours=hours_threshold)).isoformat()
        
        # Utilise la vue SQL pour les blocages
        result = self._request(
            "GET",
            f"agent_reports?select=*,agents(agent_name,agent_type,icon)&blocages=not.is.null&order=created_at.desc"
        )
        
        # Filtre par âge
        blocages = []
        for r in result:
            created = r.get("created_at")
            if created:
                created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                if (datetime.utcnow() - created_dt.replace(tzinfo=None)) > timedelta(hours=hours_threshold):
                    blocages.append(r)
        
        return blocages
    
    def get_agent_reports_today(self) -> List[Dict]:
        """Récupère les rapports du jour par agent"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self._request(
            "GET",
            f"agent_reports?report_date=eq.{today}&select=agent_id,status"
        )
    
    def get_inactive_agents(self, hours_threshold: int = 24) -> List[Dict]:
        """Agents sans rapport depuis X heures"""
        threshold_time = (datetime.utcnow() - timedelta(hours=hours_threshold)).isoformat()
        
        # Cette requête nécessite une vue ou une fonction SQL
        # Pour l'instant, on fait une approche simple
        all_agents = self._request("GET", "agents?is_active=eq.true&select=agent_id,agent_name")
        reported_agents = self._request(
            "GET",
            f"agent_reports?created_at=gt.{threshold_time}&select=agent_id"
        )
        reported_ids = {a["agent_id"] for a in reported_agents}
        
        return [a for a in all_agents if a["agent_id"] not in reported_ids]
    
    def get_failed_simulations(self) -> List[Dict]:
        """Récupère les simulations échouées"""
        return self._request(
            "GET",
            "simulation_results?status=eq.failed&order=created_at.desc&limit=10"
        )
    
    def get_overdue_tasks(self) -> List[Dict]:
        """Tâches en retard"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self._request(
            "GET",
            f"linear_tasks?due_date=lt.{today}&state=not.in.(completed,cancelled,done)&select=*"
        )
    
    def create_alert(self, alert: Alert) -> Dict:
        """Crée une alerte dans Supabase"""
        data = alert.to_dict()
        data["status"] = "active"
        return self._request("POST", "alerts", data)
    
    def get_active_alerts(self) -> List[Dict]:
        """Récupère les alertes actives"""
        return self._request(
            "GET",
            "alerts?status=eq.active&order=created_at.desc"
        )


class SlackNotifier:
    """Notification Slack"""
    
    def __init__(self, webhook_url: str = None, channel: str = None):
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        self.channel = channel or os.getenv("SLACK_CHANNEL", "#interceptor-alerts")
        self.enabled = bool(self.webhook_url)
    
    def send_alert(self, alert: Alert) -> bool:
        """Envoie une alerte sur Slack"""
        if not self.enabled:
            logger.debug("Slack notifications désactivées (pas de webhook URL)")
            return False
        
        severity_emoji = {
            AlertSeverity.LOW: "ℹ️",
            AlertSeverity.MEDIUM: "⚠️",
            AlertSeverity.HIGH: "🔶",
            AlertSeverity.CRITICAL: "🚨"
        }
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{severity_emoji.get(alert.severity, '⚠️')} {alert.title}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Type:*\n{alert.alert_type.value}"},
                    {"type": "mrkdwn", "text": f"*Severity:*\n{alert.severity.value}"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": alert.message
                }
            }
        ]
        
        if alert.agent_id:
            blocks.append({
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"Agent: *{alert.agent_id}*"}
                ]
            })
        
        payload = {
            "channel": self.channel,
            "username": "Interceptor Alerts",
            "icon_emoji": ":warning:",
            "blocks": blocks
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                logger.info(f"Alerte Slack envoyée: {alert.title}")
                return True
            else:
                logger.error(f"Erreur Slack: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Erreur envoi Slack: {e}")
            return False


class ConsoleNotifier:
    """Notification console avec formatage riche"""
    
    @staticmethod
    def print_alert(alert: Alert):
        """Affiche une alerte dans la console"""
        severity_colors = {
            AlertSeverity.LOW: "blue",
            AlertSeverity.MEDIUM: "yellow",
            AlertSeverity.HIGH: "red",
            AlertSeverity.CRITICAL: "bold red"
        }
        
        color = severity_colors.get(alert.severity, "yellow")
        
        console.print(f"\n[{color}]╔{'═' * 60}╗[/{color}]")
        console.print(f"[{color}]║ 🚨 ALERT: {alert.title:<50}║[/{color}]")
        console.print(f"[{color}]╠{'═' * 60}╣[/{color}]")
        console.print(f"[{color}]║ Type: {alert.alert_type.value:<54}║[/{color}]")
        console.print(f"[{color}]║ Severity: {alert.severity.value:<48}║[/{color}]")
        if alert.agent_id:
            console.print(f"[{color}]║ Agent: {alert.agent_id:<52}║[/{color}]")
        console.print(f"[{color}]╠{'═' * 60}╣[/{color}]")
        
        # Wrap message
        words = alert.message.split()
        lines = []
        current_line = "║ "
        for word in words:
            if len(current_line) + len(word) + 1 > 61:
                lines.append(current_line + " " * (61 - len(current_line)) + "║")
                current_line = "║ " + word + " "
            else:
                current_line += word + " "
        if current_line != "║ ":
            lines.append(current_line + " " * (61 - len(current_line)) + "║")
        
        for line in lines[:5]:  # Max 5 lignes
            console.print(f"[{color}]{line}[/{color}]")
        
        console.print(f"[{color}]╚{'═' * 60}╝[/{color}]\n")
    
    @staticmethod
    def print_summary(blocages_count: int, inactive_count: int, overdue_count: int, failed_sims: int):
        """Affiche un résumé des alertes"""
        table = Table(title="📊 Résumé des Alertes")
        table.add_column("Type", style="cyan")
        table.add_column("Count", style="yellow")
        table.add_column("Status", style="green")
        
        table.add_row("Blocages Actifs", str(blocages_count), "🔴" if blocages_count > 0 else "✅")
        table.add_row("Agents Inactifs", str(inactive_count), "🔴" if inactive_count > 0 else "✅")
        table.add_row("Tâches en Retard", str(overdue_count), "🔴" if overdue_count > 0 else "✅")
        table.add_row("Simulations Échouées", str(failed_sims), "🔴" if failed_sims > 0 else "✅")
        
        console.print(table)


class AlertMonitor:
    """Moniteur d'alertes principal"""
    
    def __init__(self, supabase_client: SupabaseClient, slack_notifier: SlackNotifier = None):
        self.client = supabase_client
        self.slack = slack_notifier
        self.console_notifier = ConsoleNotifier()
        self.alert_threshold_hours = int(os.getenv("BLOCAGE_THRESHOLD_HOURS", "2"))
        self.inactive_threshold_hours = int(os.getenv("INACTIVE_THRESHOLD_HOURS", "24"))
        
        # Cache pour éviter les doublons
        self.recent_alerts = set()
    
    def check_blocages(self) -> List[Alert]:
        """Vérifie les blocages actifs"""
        alerts = []
        blocages = self.client.get_active_blocages(self.alert_threshold_hours)
        
        for b in blocages:
            alert_id = f"blocage_{b.get('agent_id')}_{b.get('created_at')}"
            
            if alert_id in self.recent_alerts:
                continue
            
            agent_name = b.get("agents", {}).get("agent_name", "Unknown")
            agent_icon = b.get("agents", {}).get("icon", "🤖")
            
            alert = Alert(
                alert_type=AlertType.BLOCKAGE,
                severity=AlertSeverity.HIGH,
                title=f"Blocage Actif - Agent {b.get('agent_id')}",
                message=f"L'agent {b.get('agent_id')} ({agent_name}) a un blocage depuis {self.alert_threshold_hours}+ heures:\n\n{b.get('blocages', 'No description')}",
                agent_id=b.get("agent_id"),
                source_id=b.get("id"),
                metadata={
                    "report_date": b.get("report_date"),
                    "hours_old": self.alert_threshold_hours
                }
            )
            
            alerts.append(alert)
            self.recent_alerts.add(alert_id)
        
        return alerts
    
    def check_inactive_agents(self) -> List[Alert]:
        """Vérifie les agents inactifs"""
        alerts = []
        inactive = self.client.get_inactive_agents(self.inactive_threshold_hours)
        
        for agent in inactive:
            alert_id = f"inactive_{agent.get('agent_id')}"
            
            if alert_id in self.recent_alerts:
                continue
            
            alert = Alert(
                alert_type=AlertType.AGENT_INACTIVE,
                severity=AlertSeverity.MEDIUM,
                title=f"Agent Inactif - {agent.get('agent_id')}",
                message=f"L'agent {agent.get('agent_id')} ({agent.get('agent_name', 'Unknown')}) n'a pas soumis de rapport depuis {self.inactive_threshold_hours}+ heures.",
                agent_id=agent.get("agent_id"),
                metadata={
                    "last_report": "Unknown",
                    "hours_inactive": self.inactive_threshold_hours
                }
            )
            
            alerts.append(alert)
            self.recent_alerts.add(alert_id)
        
        return alerts
    
    def check_overdue_tasks(self) -> List[Alert]:
        """Vérifie les tâches en retard"""
        alerts = []
        overdue = self.client.get_overdue_tasks()
        
        for task in overdue:
            alert_id = f"overdue_{task.get('linear_identifier', task.get('id'))}"
            
            if alert_id in self.recent_alerts:
                continue
            
            alert = Alert(
                alert_type=AlertType.TASK_OVERDUE,
                severity=AlertSeverity.MEDIUM,
                title=f"Tâche en Retard - {task.get('linear_identifier', 'Unknown')}",
                message=f"La tâche '{task.get('title', 'Unknown')}' (due: {task.get('due_date', 'Unknown')}) est en retard.",
                agent_id=task.get("agent_id"),
                source_id=task.get("linear_id"),
                metadata={
                    "due_date": task.get("due_date"),
                    "assignee": task.get("assignee")
                }
            )
            
            alerts.append(alert)
            self.recent_alerts.add(alert_id)
        
        return alerts
    
    def check_failed_simulations(self) -> List[Alert]:
        """Vérifie les simulations échouées"""
        alerts = []
        failed = self.client.get_failed_simulations()
        
        for sim in failed[:5]:  # Limite à 5
            alert_id = f"failed_sim_{sim.get('id')}"
            
            if alert_id in self.recent_alerts:
                continue
            
            alert = Alert(
                alert_type=AlertType.SIMULATION_FAILED,
                severity=AlertSeverity.HIGH,
                title=f"Simulation Échouée - {sim.get('simulation_name', 'Unknown')}",
                message=f"La simulation '{sim.get('simulation_name')}' ({sim.get('simulation_type')}) a échoué.\n\nLogs:\n{sim.get('logs', 'No logs available')[:500]}",
                agent_id=sim.get("agent_id"),
                source_id=sim.get("id"),
                metadata={
                    "simulation_type": sim.get("simulation_type"),
                    "created_at": sim.get("created_at")
                }
            )
            
            alerts.append(alert)
            self.recent_alerts.add(alert_id)
        
        return alerts
    
    def process_alerts(self, alerts: List[Alert]):
        """Traite et envoie les alertes"""
        for alert in alerts:
            # Affiche dans la console
            self.console_notifier.print_alert(alert)
            
            # Envoie sur Slack
            if self.slack:
                self.slack.send_alert(alert)
            
            # Stocke dans Supabase
            try:
                self.client.create_alert(alert)
                logger.info(f"Alerte stockée: {alert.title}")
            except Exception as e:
                logger.error(f"Erreur stockage alerte: {e}")
    
    def run_check(self):
        """Effectue une vérification complète"""
        logger.info("🔍 Vérification des alertes...")
        
        all_alerts = []
        
        # Vérifications
        all_alerts.extend(self.check_blocages())
        all_alerts.extend(self.check_inactive_agents())
        all_alerts.extend(self.check_overdue_tasks())
        all_alerts.extend(self.check_failed_simulations())
        
        # Stats
        blocages = len([a for a in all_alerts if a.alert_type == AlertType.BLOCKAGE])
        inactive = len([a for a in all_alerts if a.alert_type == AlertType.AGENT_INACTIVE])
        overdue = len([a for a in all_alerts if a.alert_type == AlertType.TASK_OVERDUE])
        failed = len([a for a in all_alerts if a.alert_type == AlertType.SIMULATION_FAILED])
        
        self.console_notifier.print_summary(blocages, inactive, overdue, failed)
        
        # Traite les alertes
        if all_alerts:
            logger.info(f"📬 {len(all_alerts)} nouvelles alertes")
            self.process_alerts(all_alerts)
        else:
            logger.info("✅ Aucune nouvelle alerte")
        
        return len(all_alerts)
    
    def run_monitoring_loop(self, interval_seconds: int = 300):
        """Boucle de monitoring continue"""
        logger.info(f"🚀 Démarrage du monitoring (intervalle: {interval_seconds}s)")
        
        while True:
            try:
                self.run_check()
            except Exception as e:
                logger.error(f"Erreur dans la boucle de monitoring: {e}")
            
            time.sleep(interval_seconds)


def main():
    """Point d'entrée principal"""
    
    parser = argparse.ArgumentParser(description="Monitor Supabase for alerts")
    parser.add_argument("--once", "-1", action="store_true", help="Exécute une seule vérification")
    parser.add_argument("--interval", "-i", type=int, default=300, help="Intervalle de vérification (secondes)")
    parser.add_argument("--blocage-hours", type=int, default=2, help="Seuil de temps pour les blocages (heures)")
    parser.add_argument("--inactive-hours", type=int, default=24, help="Seuil d'inactivité (heures)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbose")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Configuration depuis env
    if args.blocage_hours:
        os.environ["BLOCAGE_THRESHOLD_HOURS"] = str(args.blocage_hours)
    if args.inactive_hours:
        os.environ["INACTIVE_THRESHOLD_HOURS"] = str(args.inactive_hours)
    
    try:
        # Initialize clients
        client = SupabaseClient()
        slack = SlackNotifier() if os.getenv("SLACK_WEBHOOK_URL") else None
        
        # Create monitor
        monitor = AlertMonitor(client, slack)
        monitor.alert_threshold_hours = args.blocage_hours
        monitor.inactive_threshold_hours = args.inactive_hours
        
        if args.once:
            # Single check
            alert_count = monitor.run_check()
            sys.exit(0 if alert_count == 0 else 1)
        else:
            # Continuous monitoring
            monitor.run_monitoring_loop(args.interval)
            
    except ValueError as e:
        console.print(f"[red]❌ Erreur de configuration: {e}[/red]")
        console.print("[yellow]Vérifiez les variables d'environnement: SUPABASE_URL, SUPABASE_KEY[/yellow]")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring arrêté.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]❌ Erreur: {e}[/red]")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


import argparse  # Ajout en fin pour éviter les conflits

if __name__ == "__main__":
    main()