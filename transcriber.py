# transcriber.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def transcribe_audio(source):
    print("📝 Transcribing via Whisper API...")

    try:
        if source.startswith("http"):
            # Remote file (Twilio recording)
            audio_data = requests.get(source, timeout=5)
            audio_data.raise_for_status()

            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data.content)

            audio_file_path = "temp_audio.wav"
        else:
            # Local file
            audio_file_path = source

        with open(audio_file_path, "rb") as audio_file:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}"
                },
                files={"file": audio_file},
                data={"model": "whisper-1", "language": "en"}
            )

        response.raise_for_status()
        text = response.json().get("text", "")
        return text.strip() if text else "Sorry, I couldn't understand that."

    except Exception as e:
        print("❌ Whisper error:", e)
        return "Sorry, I couldn't understand that."
