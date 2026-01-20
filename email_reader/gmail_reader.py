import os
import base64
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from bs4 import BeautifulSoup
from config import SCOPES


# -------------------- Constants --------------------

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


# -------------------- Gmail Authentication --------------------

def gmail_authenticate():
    """
    Authenticate with Gmail API using OAuth2.

    - Loads existing token if available
    - Refreshes token if expired
    - Initiates OAuth flow if no valid token exists

    Returns:
        Gmail API service object
    """
    creds = None

    # Load saved token if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If credentials are missing or invalid, refresh or re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # If refresh fails, delete token and re-authenticate
                os.remove(TOKEN_FILE)
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES
                )
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save new token
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


# -------------------- Email Body Extraction --------------------

def get_email_body(message):
    """
    Extracts email body from Gmail message payload.
    Supports nested multipart emails (text/plain & text/html).

    Args:
        message (dict): Gmail message object

    Returns:
        str: Extracted email body
    """

    def extract_parts(parts):
        text = ""

        for part in parts:
            # Recursively extract nested parts
            if part.get("parts"):
                text += extract_parts(part["parts"])
            else:
                data = part.get("body", {}).get("data")
                if not data:
                    continue

                decoded = base64.urlsafe_b64decode(data).decode(
                    "utf-8", errors="ignore"
                )

                if part.get("mimeType") == "text/plain":
                    text += decoded + "\n"
                elif part.get("mimeType") == "text/html" and not text:
                    text += BeautifulSoup(decoded, "html.parser").get_text() + "\n"

        return text

    payload = message.get("payload", {})

    if payload.get("parts"):
        return extract_parts(payload["parts"])

    # Fallback for single-part messages
    data = payload.get("body", {}).get("data")
    if data:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return ""


# -------------------- Email Cleaning --------------------

def clean_email_body(body):
    """
    Cleans email body text by:
    - Removing excessive newlines
    - Stripping HTML tags
    - Normalizing whitespace

    Args:
        body (str): Raw email body

    Returns:
        str: Cleaned email body
    """
    body = re.sub(r'\n+', ' ', body)
    body = re.sub(r'<[^>]+>', '', body)
    body = re.sub(r'\s{2,}', ' ', body)
    return body.strip()


# -------------------- Read Unread Emails --------------------

def read_unread_emails():
    """
    Fetches unread emails from Gmail inbox,
    extracts relevant fields, cleans body,
    and marks emails as read.

    Returns:
        tuple:
            - list of processed email dictionaries
            - total unread email count
            - Gmail service object
    """
    service = gmail_authenticate()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    messages = results.get("messages", [])
    email_data_list = []

    for msg in messages:
        msg_id = msg["id"]

        # Fetch full email data
        message = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        headers = message.get("payload", {}).get("headers", [])

        email_from = next((h["value"] for h in headers if h["name"] == "From"), "")
        email_subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        email_date = next((h["value"] for h in headers if h["name"] == "Date"), "")

        raw_body = get_email_body(message)
        clean_body = clean_email_body(raw_body)

        # Store extracted email data
        email_data_list.append({
            "message_id": message["id"],
            "thread_id": message["threadId"],
            "from": email_from,
            "subject": email_subject,
            "date": email_date,
            "raw_body": raw_body,   # ✅ preserved exactly
            "body": clean_body
        })

        # Mark email as read
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    return email_data_list, len(email_data_list), service
