import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
        print(f"Transcription: {transcript.text}")
        return transcript.text
    except Exception as e:
        print(f"Whisper error: {e}")
        return "Sorry, I couldn't understand that."
