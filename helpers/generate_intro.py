# generate_intro.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from voice_synth import text_to_speech

intro_text = (
    "Biggest challenges i am facing is hiring good talent "
#    "What’s the biggest challenge you're facing in your sector right now?"
)

text_to_speech(intro_text, output_file="test_input.wav")
print("✅ intro.wav generated.")
