from flask import Flask, request, Response, send_file
from twilio.twiml.voice_response import VoiceResponse
import requests
import os
import uuid
import traceback
from dotenv import load_dotenv
from transcriber import transcribe_audio
from gpt_response import get_gpt_reply
from voice_synth import text_to_speech

# Load environment variables
load_dotenv(dotenv_path=".env")

PUBLIC_AUDIO_BASE_URL = os.getenv("PUBLIC_AUDIO_BASE_URL")
if not PUBLIC_AUDIO_BASE_URL:
    print("❌ PUBLIC_AUDIO_BASE_URL not set in .env. Please update it with your ngrok URL.")
else:
    print(f"✅ PUBLIC_AUDIO_BASE_URL: {PUBLIC_AUDIO_BASE_URL}")

app = Flask(__name__)

@app.route("/voice", methods=["GET", "POST"])
def voice():
    print("🎧 PUBLIC_AUDIO_BASE_URL =", PUBLIC_AUDIO_BASE_URL)
    response = VoiceResponse()
    try:
        intro_url = f"{PUBLIC_AUDIO_BASE_URL}/data/intro.wav"
        print("📣 Playing intro:", intro_url)
        response.play(intro_url)
        response.record(
            action="/handle-recording",
            method="POST",
            max_length=10,
            play_beep=True,
            timeout=4
        )
    except Exception as e:
        print("❌ Error in /voice:", e)
        response.say("Sorry, something went wrong.")
    return Response(str(response), mimetype='text/xml')

@app.route("/handle-recording", methods=["POST"])
def handle_recording():
    response = VoiceResponse()
    fallback_audio = f"{PUBLIC_AUDIO_BASE_URL}/data/fallback.wav"

    try:
        recording_url = request.form.get("RecordingUrl", "")
        if not recording_url:
            raise ValueError("RecordingUrl not found")

        print("\n📥 [STEP 1] Received User Response from Twilio")
        print(f"🔗 Recording URL: {recording_url}")

        # Step 2: Transcribe
        print("\n📝 [STEP 2] Transcribing via Whisper API...")
        transcription = transcribe_audio(recording_url)
        print(f"📝 Transcription Result: {transcription}")

        # Step 3: Get GPT Response
        print("\n🤖 [STEP 3] Generating GPT Reply...")
        reply_text = get_gpt_reply(transcription)
        print(f"🧠 GPT Output: {reply_text}")

        # Step 4: Generate Voice
        print("\n🎙️ [STEP 4] Synthesizing Voice with ElevenLabs...")
        reply_audio_path = text_to_speech(reply_text)
        print(f"🔊 Audio File: {reply_audio_path}")

        # Step 5: Playback
        print("\n📤 [STEP 5] Sending audio reply back to Twilio caller...")
        response.play(f"{PUBLIC_AUDIO_BASE_URL}/data/{os.path.basename(reply_audio_path)}")

    except Exception as e:
        print("❌ Error during call flow:", e)
        traceback.print_exc()
        response.play(fallback_audio)

    response.say("Goodbye.")
    return Response(str(response), mimetype="text/xml")

@app.route('/data/<path:filename>')
def serve_audio(filename):
    try:
        return send_file(os.path.join("audio_samples", filename), mimetype="audio/wav")
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return Response("File not found", status=404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
