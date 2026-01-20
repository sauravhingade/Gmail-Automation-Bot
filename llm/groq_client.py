import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv() 

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def groq_classify_email(subject: str, body: str) -> dict | None:
    """
    Uses Groq ONLY to classify ambiguous emails.
    Returns dict with category, priority, sentiment
    """

    prompt = f"""
You are an email classifier.

Classify the email into ONE category:
- Inquiry
- Complaint
- Feedback
- Opt-out
- General
- System

Also determine:
- priority: High / Medium / Low
- sentiment: Positive / Neutral / Negative

Return ONLY valid JSON.

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

        content = response.choices[0].message.content.strip()
        data = json.loads(content)

        # Validate keys
        if not all(k in data for k in ["category", "priority", "sentiment"]):
            return None

        return data

    except Exception:
        return None
