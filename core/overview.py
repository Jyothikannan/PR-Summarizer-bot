def concise_overview(pr_data):
    title = pr_data.get("title", "PR")
    files = pr_data.get("changed_files", 0)
    additions = pr_data.get("additions", 0)
    deletions = pr_data.get("deletions", 0)

    return f"""
Overview of Changes:
• Title: {title}
• Files Changed: {files}
• Additions: +{additions}
• Deletions: -{deletions}
    """.strip()
