from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_reply(prompt):
    print("🤖 Calling GPT for quick response...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Respond with short persuasive sales replies under 3 sentences."},
                {"role": "user", "content": prompt[:200]}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT error:", e)
        return "Thanks for your message. We'll follow up shortly."
