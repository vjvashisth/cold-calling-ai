from flask import Flask, Response

app = Flask(__name__)

@app.route("/voice", methods=["GET", "POST"])
def voice():
    print("✅ Twilio hit /voice")
    xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">Hello from Vijayendra. This message is from your AI cold calling system. Swati - I LOVE YOU</Say>
</Response>
"""
    return Response(xml_response, mimetype='text/xml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
