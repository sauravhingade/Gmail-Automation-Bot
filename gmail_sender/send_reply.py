import base64
from email.mime.text import MIMEText

# Create Gmail payload for in-thread reply
def create_thread_reply(to: str, subject: str, body_text: str, thread_id: str):
    message = MIMEText(body_text)
    message["to"] = to
    message["subject"] = f"Re: {subject}"
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    payload = {
        "raw": raw_message,
        "threadId": thread_id
    }
    return payload


# Send a single reply
def send_reply(email: dict, service):
    if not email.get("auto_reply"):
        print(f"Skipping reply to {email.get('from')} (auto_reply blank)")
        return

    to = email["from"]
    subject = email.get("subject", "")
    body = email["auto_reply"]
    thread_id = email.get("thread_id")

    message_payload = create_thread_reply(to, subject, body, thread_id)

    try:
        sent_message = service.users().messages().send(userId="me", body=message_payload).execute()
        print(f"✅ Replied to {to} | Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"❌ Failed to reply to {to}: {e}")
