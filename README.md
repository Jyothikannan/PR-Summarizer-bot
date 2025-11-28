PR Summarizer Bot

A Django-based bot that analyzes GitHub Pull Requests and generates:

🔹 PR overview

🔹 Code review suggestions

🔹 Safety issue detection

🔹 Summary of changes

🔹 File-level diff insights

This bot is designed to integrate with Zoho Cliq through a webhook, letting users send a GitHub PR URL and receive a structured analysis.

🚀 Features
1. PR Metadata Extraction

Title

Description

Author

Number of commits

Files changed

Additions and deletions

2. Smart Code Review

Detects common code issues

Highlights poor coding practices

Suggests improvements

3. Safety & Security Checks

Hardcoded secrets

Dangerous functions

Unsafe patterns

4. Summarization

Generates human-readable summaries of PR changes

Helps reviewers quickly understand the update

5. File-Level Insights

Patch-based analysis

Highlights changed lines

Understands context of modifications

🛠️ Tech Stack

Python 3

Django

Ngrok (local tunnel)

GitHub REST API

Zoho Cliq Webhooks

📌 Environment Variables

Create a .env file in the project root:

SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,your-ngrok-url
GITHUB_TOKEN=your-github-personal-access-token
NGROK_URL=your-ngrok-https-url

▶️ How to Run
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Expose your local server:

ngrok http 8000


Update your .env with the new ngrok URL.

🤝 How to Use with Zoho Cliq

Go to Cliq > Bots & Tools > Webhooks

Create a new webhook

Use:

POST URL → your-ngrok-url/analyze/

Type → Bot

In any Cliq chat, send a PR URL:

https://github.com/user/repo/pull/123


You will get:

✔️ Summary

✔️ Review

✔️ Safety report

✔️ File changes

 Project Structure
 /
├── core/
│   ├── github_utils.py
│   ├── reviewer.py
│   ├── summarizer.py
│   ├── safety.py
│   ├── views.py
│   └── urls.py
├── prbot/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── .gitignore
├── manage.py
└── README.md
