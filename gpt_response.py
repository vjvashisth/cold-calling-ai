import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_gpt_reply(prompt):
    system_prompt = """
You are a persuasive and personable cold-calling sales agent for the 2026 Intercontinental Commodity Exchange in Dubai.

Use the following script structure:
- Opening Hook
- Value Proposition
- Key Benefits
- Objection Handling
- Closing Techniques (Assumptive/Alternative/Urgency)
- Reinforce Value and Ask for Confirmation

Always be confident but not pushy, and personalize replies based on user input.

Script reference:
• “Good morning [Name], this is [Agent Name] calling from the Intercontinental Commodity Exchange Dubai...”
• “The companies that thrive are those that stay ahead...”
• “Participants are personally selected...”
• “Most attendees gained $2.3M in business...”
• “What would it be worth to be 12–18 months ahead of competitors?”
• “Should I block your seat in VIP or standard?”
""".strip()

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        print(f"🤖 GPT: {reply}")
        return reply

    except Exception as e:
        print(f"❌ GPT error: {e}")
        return "Sorry, I'm having trouble responding right now. Can we follow up later?"
