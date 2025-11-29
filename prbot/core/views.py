from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .github_utils import fetch_pr_data, extract_pr_metadata
from .summarizer import generate_summary
from .reviewer import auto_review
from .safety import merge_safety_check
from .overview import concise_overview


@csrf_exempt
def analyze_pr(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        pr_url = body.get("pr_url")

        if not pr_url:
            return JsonResponse({"error": "Missing pr_url"}, status=400)

        # 1️⃣ Fetch raw PR data
        pr_data = fetch_pr_data(pr_url)
        if "error" in pr_data:
            return JsonResponse(pr_data, status=400)

        # 2️⃣ Extract metadata
        metadata = extract_pr_metadata(pr_data)

        # 3️⃣ Generate summary
        summary = generate_summary(pr_data)

        # 4️⃣ Auto code review
        review = auto_review(pr_data)

        # 5️⃣ Merge safety checker
        safety = merge_safety_check(pr_data)

        # 6️⃣ Concise changes overview
        overview_text = concise_overview(pr_data)

        # Final response packet
        response = {
            "pr_url": pr_url,
            "title": metadata["title"],
            "author": metadata["author"],
            "files_changed": metadata["files_changed"],
            "commits": metadata["commits"],
            "additions": metadata["additions"],
            "deletions": metadata["deletions"],
            "summary": summary,
            "automated_review": review,
            "merge_safety": safety,
            "concise_overview": overview_text
        }

        return JsonResponse(response, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
