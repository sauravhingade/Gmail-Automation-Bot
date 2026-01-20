import os
import requests
from dotenv import load_dotenv

load_dotenv()

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")


def send_teams_alert(email: dict):
    """
    Send high-priority email alert to Microsoft Teams.
    """
    if not TEAMS_WEBHOOK_URL:
        print("❌ Teams webhook not configured")
        return

    message = {
    "text": (
        "🚨 **High Priority Email Alert**  \n"  # double space before newline
        f"**From:** {email.get('from')}  \n"
        f"**Subject:** {email.get('subject')}  \n"
        f"**Category:** {email.get('category')}  \n"
        f"**Sentiment:** {email.get('sentiment')}  \n"
        f"**Priority:** {email.get('priority')}  \n\n"
        "**Action Required by Owner**"
    )
    }


    try:
        response = requests.post(TEAMS_WEBHOOK_URL, json=message)
        if response.status_code != 200:
            print("❌ Failed to send Teams alert:", response.text)
        else:
            print(f"✅ Teams alert sent for: {email.get('subject')}")
    except Exception as e:
        print("❌ Teams error:", e)
