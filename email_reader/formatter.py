import re

def format_email(email: dict) -> dict:
    """
    Client-facing formatter:
    - Removes URLs and surrounding parentheses
    - Removes citation markers like [6], [7]
    - Normalizes spaces and punctuation
    """

    raw_body = email.get("body", "")

    if not raw_body:
        clean_body = ""
    else:
        text = raw_body

        # Remove URLs with optional surrounding parentheses
        text = re.sub(r'\(?https?://[^\s()]+(?:\([^\s()]*\))?[^\s()]*\)?', '', text)

        # Remove citation markers like [6], [7]
        text = re.sub(r'\[\d+\]', '', text)

        # Remove extra spaces before punctuation like )
        text = re.sub(r'\s+([.,)])', r'\1', text)

        # Normalize multiple spaces to single space
        text = re.sub(r'\s+', ' ', text).strip()

    return {
        "message_id": email.get("message_id",""),
        "thread_id": email.get("message_id","thread_id"),
        "from": email.get("from", ""),
        "subject": email.get("subject", ""),
        "date": email.get("date", ""),
        "body": text,
        "raw_body":email.get("date", "raw_body"),
        "body_with_links": raw_body,
    }
