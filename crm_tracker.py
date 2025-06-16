import os
import pandas as pd
from datetime import datetime

CRM_FILE = "data/crm_log.csv"
FIELDS = ["name", "phone", "linkedin_url", "sector", "status", "last_contacted", "attempts", "notes"]

def init_crm():
    if not os.path.exists(CRM_FILE):
        df = pd.DataFrame(columns=FIELDS)
        df.to_csv(CRM_FILE, index=False)

def update_crm(name, phone, linkedin_url, sector, status, notes=""):
    if os.path.exists(CRM_FILE):
        df = pd.read_csv(CRM_FILE)
    else:
        df = pd.DataFrame(columns=FIELDS)

    if name in df["name"].values:
        df.loc[df["name"] == name, "status"] = status
        df.loc[df["name"] == name, "last_contacted"] = datetime.now().isoformat()
        df.loc[df["name"] == name, "notes"] = notes
        df.loc[df["name"] == name, "attempts"] += 1
    else:
        new_row = pd.DataFrame([{
            "name": name,
            "phone": phone,
            "linkedin_url": linkedin_url,
            "sector": sector,
            "status": status,
            "last_contacted": datetime.now().isoformat(),
            "attempts": 1,
            "notes": notes
        }])
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(CRM_FILE, index=False)
