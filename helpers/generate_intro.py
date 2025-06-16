# generate_intro.py

from voice_synth import text_to_speech

intro_text = (
    "Hello, this is Vijayendra from the Intercontinental Commodity Exchange Dubai. "
    "What’s the biggest challenge you're facing in your sector right now?"
)

text_to_speech(intro_text, output_file="intro.wav")
print("✅ intro.wav generated.")
