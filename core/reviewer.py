def auto_review(pr_data):
    additions = pr_data.get("additions", 0)
    deletions = pr_data.get("deletions", 0)

    comments = []

    if additions > 500:
        comments.append("⚠ Large amount of code added. Consider splitting into smaller PRs.")

    if deletions == 0:
        comments.append("ℹ No deletions — consider cleaning unused code.")

    if additions < 20:
        comments.append("✔ Small PR — easy to review.")

    if not comments:
        comments.append("✔ Code changes look reasonable. No major issues detected.")

    return "\n".join(comments)
