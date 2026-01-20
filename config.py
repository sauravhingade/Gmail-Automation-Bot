# config.py
# -----------------------------
# Configuration file for Lead Automation Email Bot

# Other constants (optional, add more as needed)
INBOX_FOLDER = "inbox"
UNSEEN_CRITERIA = "(UNSEEN)"
# config.py

# Gmail API scopes
# 'gmail.modify' allows reading + marking emails as read/unread
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

reply_templates = {
    "Inquiry": "Hi {name},\n\nThank you for your inquiry. We will get back to you shortly.\n\nBest regards,\nTeam",
    "Complaint": "Hi {name},\n\nWe are sorry to hear about your experience. Our support team will contact you immediately.\n\nBest regards,\nTeam",
    "Feedback": "Hi {name},\n\nThank you for your feedback! We appreciate your time.\n\nBest regards,\nTeam",
    "Opt-out": "Hi {name},\n\nYou have been successfully unsubscribed. Sorry to see you go.\n\nBest regards,\nTeam",
    "General": "Hi {name},\n\nThank you for reaching out. We will review your message and respond if necessary.\n\nBest regards,\nTeam"
}
