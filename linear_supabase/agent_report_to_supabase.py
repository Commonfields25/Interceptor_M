import os
import argparse
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Initialiser le client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def send_agent_report(agent_id: str, actions: str, blockages: str = None, needs: str = None) -> bool:
    """
    Envoyer un rapport quotidien d'agent à Supabase.
    Format attendu : [AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS]
    """
    try:
        # Préparer les données
        report_data = {
            "agent_id": agent_id,
            "date": datetime.now().date().isoformat(),
            "actions": actions,
            "blockages": blockages if blockages else "Aucun",
            "needs": needs if needs else "Aucun",
            "created_at": datetime.now().isoformat()
        }

        # Insérer dans la table agent_reports
        response = supabase.table("agent_reports").insert(report_data).execute()

        if response.status_code == 201:
            print(f"✅ Rapport envoyé avec succès pour {agent_id} : {actions[:50]}...")
            return True
        else:
            print(f"❌ Échec de l'envoi du rapport pour {agent_id} : {response.error}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du rapport : {e}")
        return False


def check_blockages(agent_id: str, issue_title: str, issue_description: str = None) -> bool:
    """
    Vérifier et enregistrer un blocage pour un agent.
    """
    try:
        blockage_data = {
            "agent_id": agent_id,
            "issue_title": issue_title,
            "issue_description": issue_description if issue_description else "",
            "start_time": datetime.now().isoformat(),
            "status": "OPEN",
            "severity": "MEDIUM"
        }

        response = supabase.table("blockages").insert(blockage_data).execute()

        if response.status_code == 201:
            print(f"⚠️ Blocage enregistré pour {agent_id} : {issue_title}")
            return True
        else:
            print(f"❌ Échec de l'enregistrement du blocage pour {agent_id} : {response.error}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement du blocage : {e}")
        return False


def resolve_blockage(agent_id: str, issue_title: str) -> bool:
    """
    Résoudre un blocage pour un agent.
    """
    try:
        # Trouver le blocage ouvert
        response = supabase.table("blockages")\
            .select("*")\
            .eq("agent_id", agent_id)\
            .eq("issue_title", issue_title)\
            .eq("status", "OPEN")\
            .execute()

        if not response.data:
            print(f"❌ Aucun blocage ouvert trouvé pour {agent_id} : {issue_title}")
            return False

        # Mettre à jour le blocage
        blockage_id = response.data[0]["id"]
        update_response = supabase.table("blockages")\
            .update({"status": "RESOLVED", "end_time": datetime.now().isoformat()})\
            .eq("id", blockage_id)\
            .execute()

        if update_response.status_code == 200:
            print(f"✅ Blocage résolu pour {agent_id} : {issue_title}")
            return True
        else:
            print(f"❌ Échec de la résolution du blocage pour {agent_id} : {update_response.error}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la résolution du blocage : {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Envoyer un rapport d'agent à Supabase")
    parser.add_argument("--agent", type=str, required=True, help="ID de l'agent (ex: E3)")
    parser.add_argument("--actions", type=str, required=True, help="Actions effectuées par l'agent")
    parser.add_argument("--blockages", type=str, default=None, help="Blocages en cours")
    parser.add_argument("--needs", type=str, default=None, help="Besoins pour avancer")
    parser.add_argument("--check-blockage", type=str, default=None, help="Titre du blocage à enregistrer")
    parser.add_argument("--resolve-blockage", type=str, default=None, help="Titre du blocage à résoudre")

    args = parser.parse_args()

    # Envoyer le rapport
    send_agent_report(args.agent, args.actions, args.blockages, args.needs)

    # Vérifier les blocages
    if args.check_blockage:
        check_blockages(args.agent, args.check_blockage)

    # Résoudre un blocage
    if args.resolve_blockage:
        resolve_blockage(args.agent, args.resolve_blockage)
