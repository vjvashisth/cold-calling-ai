import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # fallback to default

text = "Biggest challenges i am facing is hiring good talent"

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}
payload = {
    "text": text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75
    }
}

print("🎙️ Generating fallback.wav...")

response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()

output_path = os.path.join("audio_samples", "test_input.wav")
with open(output_path, "wb") as f:
    f.write(response.content)

print(f"✅ fallback.wav saved to {output_path}")
