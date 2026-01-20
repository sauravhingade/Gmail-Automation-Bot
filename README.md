# 📧 Email Leads Automation

---

## 1️⃣ Problem Statement

In real business workflows, **email is a major source of leads and urgent requests** such as pricing queries, demos, and client issues.

The key problems:

* Gmail inbox contains **mixed emails** (leads, newsletters, spam)
* **High‑priority business emails are easy to miss**
* Teams rely on **manual inbox checking**
* No instant alerting or structured tracking

👉 This leads to **slow response times, missed leads, and revenue loss**.

---

## 2️⃣ Solution Overview

This project automates email monitoring and prioritization.

**Core idea:**

> Detect important emails automatically and notify the team instantly.

What the system does:

* Reads unread emails from Gmail
* Cleans and processes email content
* Uses an **LLM (Groq‑hosted LLaMA)** to understand intent
* Classifies emails by **priority (High / Normal / Low)**
* **Sends Microsoft Teams alerts only for HIGH‑priority emails**
* Send **logical, clean, polite and professional auto replies**
* Stores all emails in Excel for tracking

---

## 3️⃣ End‑to‑End Workflow

```
Gmail Inbox
   ↓ (Gmail API)
Fetch Unread Emails
   ↓
Clean Email Content
   ↓
Groq LLaMA (Intent + Priority)
   ↓
Save to Excel (Leads Database)
   ↓
IF Priority = HIGH → Teams Notification
   ↓
Core → AI Auto Reply via Gmail API
```

---

## 4️⃣ Technical Implementation

### 🔹 Gmail Integration

* Gmail API with **OAuth 2.0**
* Fetches **only unread emails**
* Extracts:

  * From
  * Subject
  * Date
  * Email body (cleaned)

---

### 🔹 Email Cleaning

* Removes HTML tags and noise
* Strips signatures and unnecessary formatting
* Prepares clean text for LLM analysis

---

### 🔹 AI‑Based Priority Classification

* Uses **Groq API with LLaMA model**
* Email subject + body sent to LLM
* LLM returns:

  * Lead category
  * Priority level (High / Normal / Low)

This avoids rigid keyword rules and enables **context‑aware decisions**.

---

### 🔹 AI Auto Reply (Core)

* For relevant emails, an **LLM‑generated reply** is created
* Replies are:

  * Polite
  * Context‑aware
  * Business‑safe
* Sent using Gmail API

This reduces manual responses for common queries.

---

### 🔹 Excel Lead Storage

* All emails saved to `leads.xlsx`
* Columns:

  * From
  * Subject
  * Date
  * Clean Body
  * Lead Category
  * Priority
  * Status

Acts as a **lightweight CRM**.

---

### 🔹 Microsoft Teams Notifications

* Uses **Incoming Webhook**
* Triggered **only for HIGH‑priority emails**
* Real‑time alerts for urgent leads

Example:

```
🚨 HIGH PRIORITY EMAIL
From: client@company.com
Subject: Need pricing urgently
```

---

## 5️⃣ Tech Stack

* Python
* Gmail API
* Groq API (LLaMA)
* OpenPyXL
* Microsoft Teams Incoming Webhook
* Requests

---

## 6️⃣ Project Structure

```
LEAD_AUTOMATION_EMAIL_BOT/
│
├── email_reader/
│   ├── gmail_reader.py        # Read unread emails
│   └── formatter.py           # Clean email content
│
├── gmail_sender/
│   └── send_reply.py          # AI auto replies
│
├── llm/
│   ├── groq_client.py         # Groq API client
│   ├── email_processor.py     # LLM priority analysis
│   └── llm_reply.py           # Reply generation
│
├── teams_notification/
│   └── send_alert.py          # Teams alerts
│
├── storage/
│   ├── excel_manager.py       # Excel operations
│   └── leads.xlsx
│
├── main.py                    # Workflow orchestration
├── credentials.json
├── token.json
└── README.md
```

---

## 7️⃣ Outcome

* High‑priority emails are **never missed**
* Teams receive **instant alerts**
* Core **AI auto replies save time**
* Leads are structured and trackable

This project focuses on **practical automation**, solving a real‑world email management problem using clean architecture and AI where it actually adds value.
