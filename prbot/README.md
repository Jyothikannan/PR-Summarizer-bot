PR Summarizer Bot

A Django-based bot that analyzes GitHub Pull Requests and generates:

  PR overview
  Code review suggestions
  Safety issue detection
  Summary of changes
  File-level diff insights
  Integrates with Zoho Cliq Custom Bot, allowing users to send a GitHub PR URL and receive a structured analysis.

Features

  PR Metadata Extraction
  Title, Description, Author, Commits, Files changed, Additions/Deletions
  Smart Code Review
  Detects common issues, highlights poor coding practices, suggests improvements
  Safety & Security Checks
  Detects hardcoded secrets, dangerous functions, unsafe patterns
  Summarization
  Human-readable summaries of PR changes
  File-Level Insights
  Patch-based analysis, highlights changed lines, understands context

Tech Stack

  Python 3 | Django | Ngrok | GitHub REST API | Zoho Cliq Custom Bot

Environment Variables

  Create a .env file in project root:
  SECRET_KEY=your-django-secret-key
  DEBUG=True
  ALLOWED_HOSTS=127.0.0.1,localhost,your-ngrok-url
  GITHUB_TOKEN=your-github-personal-access-token
  NGROK_URL=your-ngrok-https-url

Zoho Cliq Integration (Contest Setup)

1.Create a Custom Bot
  Cliq → Bots → Build Bot → Custom Bot

2.Configure the Bot
  Add bot name & description

3.Enable Message Handler
  Add Deluge Script in Message Handler

response = Map();
text = "";
if(message != null) text = message.toString();

if(text != "" && text.contains("https://github.com") && text.contains("/pull/")) {
    url = "https://your-ngrok-url/analyze/"; // Replace with your ngrok URL
    payload = Map();
    payload.put("pr_url", text);

    try {
        result = invokeurl [
            url : url
            type : POST
            body : payload.toString()
            headers : {"Content-Type" : "application/json"}
        ];

        if(result != null){
            final_msg = "PR Summary\n-----------\n" + result.get("summary") + "\n\n";
            final_msg += "Code Insights\n-----------\n" + result.get("code_insights") + "\n\n";
            final_msg += "Code Explanation\n-----------\n" + result.get("code_explanation") + "\n\n";
            final_msg += "Warnings\n-----------\n" + result.get("warnings") + "\n\n";
            final_msg += "Tests Present\n-----------\n" + result.get("tests_present") + "\n\n";
            final_msg += "Risk Score\n-----------\n" + result.get("risk_score") + "\n\n";
            final_msg += "Automated Review\n-----------\n" + result.get("automated_review") + "\n\n";
            final_msg += "Merge Safety\n-----------\n" + result.get("merge_safety") + "\n\n";
            final_msg += "Concise Overview\n-----------\n" + result.get("concise_overview");
            response.put("text", final_msg);
        } else response.put("text", "Could not get summary from API.");
    } catch(e) { response.put("text", "Error calling summarization API."); }

} else { response.put("text", "Send me a PR link to summarize!"); }

return response;

Send a PR URL in Cliq

https://github.com/user/repo/pull/123


Receive: ✅ Summary | ✅ Review | ✅ Safety report | ✅ File changes