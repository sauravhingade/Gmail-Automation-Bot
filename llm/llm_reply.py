import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_llm_reply(subject: str, body: str) -> str | None:
    """
    GROQ-based acknowledgement reply.
    AI does NOT know business details.
    """

    prompt = f"""
You are a customer support assistant.

STRICT RULES:
- Do NOT mention pricing, products, plans, or services
- Do NOT ask follow-up questions
- Do NOT make assumptions
- Do NOT use placeholders like [Your Name]
- Keep it short, polite, professional
- Purpose: acknowledge receipt only
- End with: Customer Support Team

Email:
Subject: {subject}
Body: {body}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        reply = response.choices[0].message.content.strip()

        # Safety checks
        if len(reply) < 40:
            return None

        if reply.lower() in body.lower():
            return None

        return reply

    except Exception:
        return None
