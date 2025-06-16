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

load_dotenv(dotenv_path="/.env")
print(os.getenv("PUBLIC_AUDIO_BASE_URL"))
app = Flask(__name__)


@app.route("/voice", methods=["GET", "POST"])
def voice():
    response = VoiceResponse()
    response.play(url=f"{os.getenv('PUBLIC_AUDIO_BASE_URL')}/data/intro.wav")
    response.record(
        action="/handle-recording",
        method="POST",
        max_length=15,
        play_beep=True,
        timeout=5
    )
    return Response(str(response), mimetype='text/xml')


@app.route("/handle-recording", methods=["POST"])
def handle_recording():
    try:
        recording_url = request.form.get("RecordingUrl", "")
        print(f"Got recording URL: {recording_url}")

        if not recording_url:
            raise Exception("RecordingUrl missing in request")

        # Step 1: Download the recording as .wav
        wav_filename = f"recording_{uuid.uuid4().hex}.wav"
        response = requests.get(recording_url + ".wav")
        with open(wav_filename, 'wb') as f:
            f.write(response.content)

        print(f"Saved WAV file: {wav_filename} ({os.path.getsize(wav_filename)} bytes)")

        # Step 2: Transcribe
        user_input = transcribe_audio(wav_filename)
        print(f"Transcription: {user_input}")

        # Step 3: Get GPT reply
        gpt_reply = get_gpt_reply(user_input)
        print(f"GPT: {gpt_reply}")

        # Step 4: Generate voice reply
        reply_audio = text_to_speech(gpt_reply, output_file="reply.wav")
        if not reply_audio or not os.path.exists("reply.wav"):
            raise Exception("reply.wav was not generated")

        # Step 5: Respond with voice
        response = VoiceResponse()
        response.play(url=f"{os.getenv('PUBLIC_AUDIO_BASE_URL')}/reply.wav")
        return Response(str(response), mimetype='text/xml')

    except Exception as e:
        print("Error during call handling:")
        traceback.print_exc()
        response = VoiceResponse()
        response.say("Unfortunately, an internal error occurred. Please try again later.")
        return Response(str(response), mimetype='text/xml')


@app.route("/reply.wav")
def serve_reply_audio():
    if os.path.exists("reply.wav"):
        return send_file("reply.wav", mimetype="audio/wav")
    return Response("Audio file not found", status=404)


@app.route("/intro.wav")
def serve_intro_audio():
    if os.path.exists("intro.wav"):
        return send_file("intro.wav", mimetype="audio/wav")
    return Response("Intro audio file not found", status=404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
