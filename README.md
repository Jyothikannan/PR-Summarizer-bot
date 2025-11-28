PR Summarizer Bot

A Django-based bot that analyzes GitHub Pull Requests and generates:

🔹 PR overview

🔹 Code review suggestions

🔹 Safety issue detection

🔹 Summary of changes

🔹 File-level diff insights

This bot integrates with Zoho Cliq through a Custom Bot, allowing users to send a GitHub PR URL and receive a structured analysis.

🚀 Features

PR Metadata Extraction

Title

Description

Author

Number of commits

Files changed

Additions and deletions

Smart Code Review

Detects common code issues

Highlights poor coding practices

Suggests improvements

Safety & Security Checks

Hardcoded secrets

Dangerous functions

Unsafe patterns

Summarization

Generates human-readable summaries of PR changes

Helps reviewers quickly understand updates

File-Level Insights

Patch-based analysis

Highlights changed lines

Understands context of modifications

🛠️ Tech Stack

Python 3

Django

Ngrok (local tunnel)

GitHub REST API

Zoho Cliq Custom Bot

📌 Environment Variables

Create a .env file in the project root with:

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

🤝 How to Use with Zoho Cliq (Contest Setup)

This project works with a Zoho Cliq Custom Bot, not webhooks.

1️⃣ Create a Custom Bot
Go to: Cliq → Bots → Build Bot → Custom Bot

2️⃣ Configure the Bot

Add a bot name

Add a description

Enable Message Handler

3️⃣ Add this Deluge Script in “Message Handler”

response = Map();
text = "";

if(message != null)
{
    text = message.toString();
}

if(text != "" && text.contains("https://github.com") && text.contains("/pull/"))
{
    url = "https://your-ngrok-url/analyze/";  // Replace with your ngrok URL
    payload = Map();
    payload.put("pr_url", text);

    try
    {
        result = invokeurl
        [
            url : url
            type : POST
            body : payload.toString()
            headers : {"Content-Type" : "application/json"}
        ];

        if(result != null)
        {
            summary = result.get("summary");
            review = result.get("automated_review");
            safety = result.get("merge_safety");
            overview = result.get("concise_overview");

            codeInsights = result.get("code_insights");
            codeExplanation = result.get("code_explanation");
            warnings = result.get("warnings");
            tests = result.get("tests_present");
            riskScore = result.get("risk_score");

            final_msg = "";
            final_msg += "PR Summary\n-----------\n" + summary + "\n\n";

            if(codeInsights != null) final_msg += "Code Insights\n-----------\n" + codeInsights + "\n\n";
            if(codeExplanation != null) final_msg += "Code Explanation\n-----------\n" + codeExplanation + "\n\n";
            if(warnings != null) final_msg += "Warnings\n-----------\n" + warnings + "\n\n";
            if(tests != null) final_msg += "Tests Present\n-----------\n" + tests + "\n\n";
            if(riskScore != null) final_msg += "Risk Score\n-----------\n" + riskScore + "\n\n";

            final_msg += "Automated Review\n-----------\n" + review + "\n\n";
            final_msg += "Merge Safety\n-----------\n" + safety + "\n\n";
            final_msg += "Concise Overview\n-----------\n" + overview;

            response.put("text", final_msg);
        }
        else
        {
            response.put("text", "Could not get summary from API.");
        }
    }
    catch(e)
    {
        response.put("text", "Error calling summarization API.");
    }
}
else
{
    response.put("text", "Send me a PR link to summarize!");
}

return response;


⚠️ Important: Replace https://your-ngrok-url/analyze/ with your ngrok HTTPS forwarding URL.

4️⃣ Send a PR URL in Cliq:

https://github.com/user/repo/pull/123


You will receive:

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
