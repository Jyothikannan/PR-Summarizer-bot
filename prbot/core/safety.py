def merge_safety_check(pr_data):
    mergeable = pr_data.get("mergeable")

    if mergeable is True:
        return "✔ This PR is safe to merge. No conflicts."

    elif mergeable is False:
        return " Merge conflicts detected. PR is NOT safe to merge."

    return "⚠ Mergeability unknown. GitHub has not computed it yet."
