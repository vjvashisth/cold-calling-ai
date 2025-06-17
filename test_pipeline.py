import os
from transcriber import transcribe_audio
from gpt_response import get_gpt_reply
from voice_synth import text_to_speech

# Replace this with your own local test audio file path
TEST_AUDIO_FILE = "audio_samples/test_input.wav"

def test_full_pipeline():
    print("\n🎧 Step 1: Transcribing test audio...")
    if not os.path.exists(TEST_AUDIO_FILE):
        print(f"❌ Test file not found: {TEST_AUDIO_FILE}")
        return

    # Simulate a Twilio recording URL by reading local file
    try:
        with open(TEST_AUDIO_FILE, "rb") as f:
            audio_bytes = f.read()

        with open("temp_test.wav", "wb") as f:
            f.write(audio_bytes)

        # Run transcription on the saved test file
        transcription = transcribe_audio("temp_test.wav")
        print(f"📝 Transcription: {transcription}")

        # Generate GPT reply
        reply = get_gpt_reply(transcription)
        print(f"🤖 GPT Reply: {reply}")

        # Generate voice audio
        audio_path = text_to_speech(reply)
        print(f"🔊 Synthesized voice reply saved to: {audio_path}")

    except Exception as e:
        print(f"❌ Pipeline error: {e}")

if __name__ == "__main__":
    test_full_pipeline()
