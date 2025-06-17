import os
import uuid
import requests
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # default ElevenLabs voice

def text_to_speech(text):
    print("🔁 Generating speech with ElevenLabs...")
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text[:400],
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, headers=headers, json=payload, timeout=8)
        response.raise_for_status()

        filename = f"reply_{uuid.uuid4().hex[:8]}.wav"
        output_path = os.path.join("audio_samples", filename)

        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Synthesized audio to {output_path}")
        return normalize_audio_for_twilio(output_path)

    except Exception as e:
        print("❌ ElevenLabs error:", e)
        raise

def normalize_audio_for_twilio(filepath):
    try:
        print("🎧 Normalizing audio for Twilio (mono, 16kHz, 16-bit PCM)...")
        audio = AudioSegment.from_file(filepath)
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)

        normalized_path = filepath.replace(".wav", "_twilio.wav")
        audio.export(normalized_path, format="wav")

        print(f"✅ Normalized audio saved to {normalized_path}")
        return normalized_path

    except Exception as e:
        print("❌ Audio normalization failed:", e)
        raise
