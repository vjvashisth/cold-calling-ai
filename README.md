# 📞 Plato-AI: AI-Powered Cold Calling Sales Agent

**Plato-AI** is a real-time AI cold-calling agent that autonomously places calls, records responses, generates intelligent GPT replies, and streams them back as lifelike voice using ElevenLabs. It optionally follows up via LinkedIn.

---

## ✨ Features

- 🔊 **Intro Voice Playback** using ElevenLabs (`intro.wav`)
- 📞 **Call Orchestration** with Twilio API
- 🎙️ **User Speech Recording** (max 15 sec)
- 🧠 **Transcription** via Whisper API
- 💬 **GPT-4 Response Generation** with sales script logic
- 🎧 **Voice Reply Playback** using ElevenLabs TTS
- 🔗 **LinkedIn Follow-up** via `linkedin_messenger.py`
- 🧾 **CRM Logging** with call details & results
- 🛠️ Modular components for debugging, local testing, and expansion

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Flask** for webhook & voice server
- **Twilio Voice API** for call & recording
- **OpenAI Whisper + GPT-4** for transcription and reply
- **ElevenLabs** for dynamic voice synthesis
- **Selenium** (used for optional LinkedIn automation)
- **FFmpeg** for audio processing

---

## 📁 File Overview

```

plato-ai/
├── main.py                 # Triggers outbound call via Twilio
├── dynamic\_voice\_server.py # Main Flask app: handles Twilio voice + response playback
├── twiml\_server.py         # Optional webhook testing stub for Twilio (static XML)
├── gpt\_response.py         # Sales-focused GPT-4 reply logic
├── transcriber.py          # Whisper transcription wrapper
├── voice\_synth.py          # ElevenLabs API integration
├── voice\_call\_handler.py   # Twilio call handler logic (used by main)
├── linkedin\_messenger.py   # (Optional) LinkedIn connect + message automation
├── crm\_tracker.py          # Logs call attempt and contact details
├── .env.example            # Environment variables sample
├── README.md               # This file
└── requirements.txt        # Python dependencies

````

---

## 🔧 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
````

### 2. Configure environment variables

```bash
cp .env.example .env
```

Fill out `.env`:

```env
OPENAI_API_KEY=...
ELEVENLABS_API_KEY=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=...
PUBLIC_AUDIO_BASE_URL=https://your-ngrok-url
LINKEDIN_EMAIL=...
LINKEDIN_PASSWORD=...
```

### 3. Run Flask Voice Server

```bash
python dynamic_voice_server.py
```

### 4. Expose your server with ngrok

```bash
ngrok http 5005
```

Update `PUBLIC_AUDIO_BASE_URL` in `.env` with the generated ngrok HTTPS URL.

### 5. Place test calls

```bash
python main.py
```

---

## 🧪 Local Testing

You can test each module separately:

```bash
python test.py  # Simulates a recording → transcription → GPT → TTS
```

---

## 🔮 Upcoming Features

* [ ] Dynamic Waalaxy follow-up (instead of Selenium)
* [ ] Multi-language support
* [ ] Dashboard for call logs and analytics
* [ ] Voice switching between agents
* [ ] Automatic objection/reschedule handling

---

## ⚠️ Legal

Make sure you have proper user consent and are compliant with telemarketing and data privacy laws (GDPR, TCPA, etc.) before using this in production.

---

## 🙌 Credits

Built by [@vjvashisth](https://github.com/vjvashisth) for AI-powered B2B outreach. If you found this useful, ⭐ the repo and share!