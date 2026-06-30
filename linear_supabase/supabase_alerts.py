import os
import time
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Initialiser le client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def check_long_blockages():
    """
    Vérifier les blocages ouverts depuis plus de 2 heures et envoyer des alertes.
    """
    try:
        # Récupérer les blocages ouverts depuis plus de 2h
        two_hours_ago = (datetime.now() - timedelta(hours=2)).isoformat()

        response = supabase.table("blockages")\
            .select("*, agents(name)")\
            .eq("status", "OPEN")\
            .lt("start_time", two_hours_ago)\
            .execute()

        if not response.data:
            print("✅ Aucun blocage > 2h détecté.")
            return

        # Envoyer une alerte pour chaque blocage
        for blockage in response.data:
            agent_id = blockage["agent_id"]
            agent_name = blockage["agents"]["name"] if blockage["agents"] else agent_id
            issue_title = blockage["issue_title"]
            start_time = blockage["start_time"]

            # Calculer la durée
            start_datetime = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            duration = datetime.now() - start_datetime
            duration_hours = duration.total_seconds() / 3600

            # Créer un message d'alerte
            alert_message = (
                f"⚠️ **ALERTE BLOCAGE** ⚠️\n"
                f"Agent: **{agent_name} ({agent_id})**\n"
                f"Blocage: **{issue_title}**\n"
                f"Durée: **{duration_hours:.1f} heures**\n"
                f"Début: {start_time}"
            )

            # Enregistrer l'alerte dans Supabase
            alert_data = {
                "agent_id": agent_id,
                "message": alert_message,
                "type": "BLOCKAGE",
                "created_at": datetime.now().isoformat()
            }

            supabase.table("alerts").insert(alert_data).execute()

            # Envoyer une notification Slack (si configuré)
            if SLACK_WEBHOOK_URL:
                slack_payload = {
                    "text": alert_message,
                    "username": "Interceptor_M Alert Bot",
                    "icon_emoji": ":rotating_light:"
                }
                requests.post(SLACK_WEBHOOK_URL, json=slack_payload)

            print(f"⚠️ Alerte envoyée pour {agent_id} : {issue_title} (durée: {duration_hours:.1f}h)")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des blocages : {e}")


def monitor_agent_reports():
    """
    Surveiller les rapports des agents pour détecter les anomalies.
    """
    try:
        # Récupérer les rapports des dernières 24h
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()

        response = supabase.table("agent_reports")\
            .select("*, agents(name)")\
            .gte("date", yesterday)\
            .execute()

        if not response.data:
            print("⚠️ Aucun rapport récent trouvé.")
            return

        # Vérifier les agents qui n'ont pas envoyé de rapport
        agents_without_reports = []
        agents_response = supabase.table("agents").select("id, name").execute()
        reported_agent_ids = {report["agent_id"] for report in response.data}

        for agent in agents_response.data:
            if agent["id"] not in reported_agent_ids:
                agents_without_reports.append(agent)

        if agents_without_reports:
            for agent in agents_without_reports:
                alert_message = (
                    f"⚠️ **RAPPORT MANQUANT** ⚠️\n"
                    f"Agent: **{agent['name']} ({agent['id']})**\n"
                    f"Dernier rapport: **Aucun dans les 24 dernières heures**"
                )

                alert_data = {
                    "agent_id": agent["id"],
                    "message": alert_message,
                    "type": "MISSING_REPORT",
                    "created_at": datetime.now().isoformat()
                }

                supabase.table("alerts").insert(alert_data).execute()

                if SLACK_WEBHOOK_URL:
                    slack_payload = {
                        "text": alert_message,
                        "username": "Interceptor_M Alert Bot",
                        "icon_emoji": ":warning:"
                    }
                    requests.post(SLACK_WEBHOOK_URL, json=slack_payload)

                print(f"⚠️ Alerte envoyée pour {agent['id']} : Rapport manquant")
        else:
            print("✅ Tous les agents ont envoyé un rapport récent.")
    except Exception as e:
        print(f"❌ Erreur lors de la surveillance des rapports : {e}")


if __name__ == "__main__":
    print("🚀 Démarrage de la surveillance des alertes...")

    while True:
        print("\n--- Vérification des blocages et rapports ---")
        check_long_blockages()
        monitor_agent_reports()

        # Attendre 1 heure avant la prochaine vérification
        print("\n⏳ Attente de 1 heure avant la prochaine vérification...")
        time.sleep(3600)  # 1 heure
