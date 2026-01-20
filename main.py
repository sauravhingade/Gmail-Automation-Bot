"""
Main entry point for the Email Automation System.

Flow:
1. Read unread emails from Gmail
2. Normalize/clean email data
3. Process email using LLM (priority, intent, reply, etc.)
4. Send automatic replies
5. Send Teams alert for high-priority emails
6. Store processed emails in Excel
"""

# -------------------- Imports --------------------

from email_reader.gmail_reader import read_unread_emails
from email_reader.formatter import format_email

from llm.email_processor import process_email_advanced

from gmail_sender.send_reply import send_reply
# from gmail_sender.send_reply import send_replies_batch  # Optional batch mode

from teams_notification.send_alert import send_teams_alert
from storage.excel_manager import save_emails_to_excel


# -------------------- Main Logic --------------------

def main():
    """
    Executes the full email automation pipeline.
    """

    # Step 1: Read unread emails from Gmail
    emails, total_unread, service = read_unread_emails()

    if total_unread == 0:
        print("No unread emails found.")
        return

    print(f"Total unread emails fetched: {total_unread}")

    # Step 2: Clean and normalize raw Gmail emails
    clean_emails = [format_email(email) for email in emails]

    # Step 3–5: Process each email, reply, and send alerts
    for email in clean_emails:
        # Enrich email using LLM (priority, summary, reply, etc.)
        processed_email = process_email_advanced(email)

        # Send automated reply
        send_reply(processed_email, service)

        # Send Teams alert for high-priority emails
        if processed_email.get("priority") == "High":
            send_teams_alert(processed_email)

    # Step 6: Store all processed emails in Excel
    save_emails_to_excel(clean_emails)

    print("Email processing pipeline completed successfully.")


# -------------------- Script Entry --------------------

if __name__ == "__main__":
    main()
