import csv
import os
from datetime import datetime

LOG_FILE = "call_logs.csv"
FIELDNAMES = ["timestamp", "name", "phone", "status", "notes"]

def log_call_result(name, phone, status, notes=""):
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "phone": phone,
            "status": status,
            "notes": notes
        })