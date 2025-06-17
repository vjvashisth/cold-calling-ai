from flask import Flask, Response, send_from_directory, request
import os

app = Flask(__name__)

@app.route("/voice", methods=["GET", "POST"])
def voice():
    print("✅ Twilio hit /voice")
    xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>https://b481-2409-40e4-10b1-c7d4-75be-3834-bfae-1150.ngrok-free.app/data/intro.wav</Play>
    <Record action="/handle-recording" maxLength="15" method="POST" playBeep="true" timeout="5"/>
</Response>"""
    return Response(xml_response, mimetype='text/xml')

@app.route("/handle-recording", methods=["POST"])
def handle_recording():
    recording_url = request.form.get("RecordingUrl")
    print(f"✅ Received recording at: {recording_url}")
    # You can add further processing logic here
    return Response("<Response><Say>Thanks, goodbye!</Say></Response>", mimetype="text/xml")

@app.route('/data/<path:filename>')
def serve_audio(filename):
    return send_from_directory('audio_samples', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
