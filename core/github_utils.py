import os
import requests
from urllib.parse import urlparse

# 1️⃣ Read token from environment
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # make sure it's in your .env

# --------------------------------------------------------
# Fetch PR metadata + file-level diffs
# --------------------------------------------------------
def fetch_pr_data(pr_url):
    try:
        parsed = urlparse(pr_url)
        parts = parsed.path.strip("/").split("/")

        if len(parts) < 4:
            return {"error": "Invalid PR URL format"}

        owner, repo, _, pr_number = parts

        # 2️⃣ Use token in headers if available
        headers = {}
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'

        # Fetch PR metadata
        meta_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
        meta_resp = requests.get(meta_url, headers=headers)
        if meta_resp.status_code != 200:
            return {"error": "Failed to fetch PR metadata"}

        metadata = meta_resp.json()

        # Fetch file-level diffs (patches)
        files_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files?per_page=100"
        files_resp = requests.get(files_url, headers=headers)
        metadata["files"] = files_resp.json() if files_resp.status_code == 200 else []

        return metadata

    except Exception as e:
        return {"error": str(e)}


# --------------------------------------------------------
# Extract clean metadata for bot response
# --------------------------------------------------------
def extract_pr_metadata(data):
    return {
        "title": data.get("title", "Unknown"),
        "body": data.get("body", "No description provided."),
        "author": data.get("user", {}).get("login", "Unknown"),
        "files_changed": data.get("changed_files", 0),
        "commits": data.get("commits", 0),
        "additions": data.get("additions", 0),
        "deletions": data.get("deletions", 0),
        "files": data.get("files", [])
    }
