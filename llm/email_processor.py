import re
from llm.groq_client import groq_classify_email
from llm.llm_reply import generate_llm_reply
from config import reply_templates

# ----------------------------
# Helpers
# ----------------------------
def extract_name(from_field: str) -> str:
    if "<" in from_field:
        return from_field.split("<")[0].strip().title()
    return from_field.split("@")[0].replace(".", " ").title()


def is_system_email(subject: str, body: str) -> bool:
    text = (subject + " " + body).lower()
    patterns = [
        r"verification",
        r"verify your",
        r"successfully",
        r"no-reply",
        r"do not reply",
        r"login alert",
        r"security alert",
        r"password reset",
        r"otp",
        r"one time password"
    ]
    return any(re.search(p, text) for p in patterns)


# ----------------------------
# MAIN PROCESSOR (FINAL)
# ----------------------------
def process_email_advanced(email: dict) -> dict:
    subject = email.get("subject", "")
    body = email.get("body", "")
    from_field = email.get("from", "")
    combined_text = (subject + " " + body).lower()

    # SYSTEM EMAIL — HARD STOP
    if is_system_email(subject, body):
        email.update({
            "category": "System",
            "priority": "Low",
            "sentiment": "Neutral",
            "owner_action": "Not Required",
            "auto_reply": ""
        })
        return email

    # RULE-BASED FAST CLASSIFICATION
    if re.search(r"\b(pricing|price|cost|plan|quote)\b", combined_text):
        category = "Inquiry"
    elif re.search(r"\b(complaint|issue|problem|bad|dont like|hate|poor)\b", combined_text):
        category = "Complaint"
    elif re.search(r"\b(unsubscribe|remove me)\b", combined_text):
        category = "Opt-out"
    else:
        category = "General"

    # GROQ UNDERSTANDING (IMPORTANT)
    groq_result = groq_classify_email(subject, body)
    if groq_result:
        category = groq_result["category"]
        priority = groq_result["priority"]
        sentiment = groq_result["sentiment"]
    else:
        # fallback safety
        sentiment = "Neutral"
        priority = "Low"

    # 4️⃣ OWNER ACTION
    owner_action = "Required" if category != "System" else "Not Required"

    # AUTO REPLY (ACKNOWLEDGEMENT ONLY)
    auto_reply = ""
    name = extract_name(from_field)

    if category == "Complaint":
        auto_reply = reply_templates["Complaint"].replace("{name}", name)

    elif category in ["Inquiry", "Feedback", "General"]:
        llm_reply = generate_llm_reply(subject, body)
        if llm_reply:
            auto_reply = llm_reply

    # FINAL UPDATE
    email.update({
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "owner_action": owner_action,
        "auto_reply": auto_reply
    })

    return email
