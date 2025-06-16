import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # default Adam

HEADERS = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json"
}


def text_to_speech(text, output_file="data/reply.wav"):
    try:
        print("🔁 Generating speech with ElevenLabs...")

        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        response = requests.post(
            tts_url,
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            json=payload,
            stream=True
        )

        if response.status_code != 200:
            print(f"ElevenLabs error: {response.status_code}, {response.json()}")
            return None

        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        print(f"Synthesized audio to {output_file}")
        return output_file

    except Exception as e:
        print(f"ElevenLabs exception: {e}")
        return None
