import pandas as pd
from utils.logger import log_call_result
from voice_call_handler import initiate_call
from linkedin_messenger import send_linkedin_message
from crm_tracker import init_crm, update_crm
import os

# 🔁 Update with your live ngrok TwiML URL
TWIML_URL = "https://a974-2409-40e5-12c-fdf7-b8b0-8d33-bf9f-78b9.ngrok-free.app/voice"  # Replace this

def load_contacts(file_path='contacts.csv'):
    try:
        df = pd.read_csv(file_path, dtype={"phone": str})
        df.columns = [col.strip().lower() for col in df.columns]
        df.dropna(subset=["name", "phone"], inplace=True)

        # Load CRM and exclude "Closed" or 3+ attempts
        if os.path.exists("crm_log.csv"):
            crm = pd.read_csv("crm_log.csv")
            skip_names = crm[(crm["status"].isin(["Closed", "Cold"])) | (crm["attempts"] >= 3)]["name"]
            df = df[~df["name"].isin(skip_names)]

        return df
    except Exception as e:
        print(f"❌ Error loading contacts: {e}")
        return pd.DataFrame()

def main():
    init_crm()

    contacts = load_contacts()
    if contacts.empty:
        print("No contacts to process.")
        return

    print("✅ Contacts Loaded:")
    print(contacts)

    for _, row in contacts.iterrows():
        name = row["name"]
        phone = row["phone"]
        linkedin_url = row.get("linkedin_url", "")
        sector = row.get("sector", "your industry")

        print(f"\n📞 Calling {name} at {phone}...")
        sid = initiate_call(phone, TWIML_URL)

        if sid:
            status = "Follow-up"
            notes = f"SID: {sid} — interested in follow-up"

            try:
                send_linkedin_message(
                    linkedin_url=linkedin_url,
                    name=name,
                    sector=sector
                )
                notes += " | LinkedIn sent"
            except Exception as e:
                notes += f" | LinkedIn failed: {e}"
        else:
            status = "Failed"
            notes = "Error placing call"

        log_call_result(
            name=name,
            phone=phone,
            status=status,
            notes=notes
        )

        update_crm(
            name=name,
            phone=phone,
            linkedin_url=linkedin_url,
            sector=sector,
            status=status,
            notes=notes
        )

if __name__ == "__main__":
    main()
