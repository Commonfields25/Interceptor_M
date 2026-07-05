import csv
import json
import os
from supabase import create_client, Client

def upload():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("Missing Supabase credentials")
        return

    supabase: Client = create_client(url, key)

    # Files to upload
    files = ["report_PN.csv", "report_APN.csv"]

    for filename in files:
        path = f"simulation/exports/{filename}"
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue

        with open(path, mode='r') as f:
            reader = csv.DictReader(f)
            # Fix F821 row name issue
            data_list = []
            for r in reader:
                data_list.append(r)

            mode = "PN" if "PN" in filename else "APN"

            payload = {
                "agent_id": "E3",
                "simulation_name": f"Monte Carlo Intercept ({mode})",
                "parameters": {"mode": mode, "iterations": len(data_list)},
                "results": {"data": data_list[:20]},
                "status": "COMPLETED"
            }

            supabase.table("simulation_results").insert(payload).execute()
            print(f"Prepared upload for {filename}")

if __name__ == "__main__":
    upload()
