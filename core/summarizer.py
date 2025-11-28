import re

def extract_code_insights(files_changed):
    functions = []
    classes = []

    for file in files_changed:
        diff = file.get("patch", "") or ""

        # Detect added functions (python-style)
        fn_matches = re.findall(r'^\+.*def (\w+)\(.*\):', diff, re.MULTILINE)
        # Detect added classes
        class_matches = re.findall(r'^\+.*class (\w+)\(.*\):', diff, re.MULTILINE)

        functions.extend(fn_matches)
        classes.extend(class_matches)

    return functions, classes


def detect_code_warnings(files_changed):
    warnings = []

    combined_diff = ""
    for file in files_changed:
        combined_diff += (file.get("patch", "") or "") + "\n"

    # Division by zero check (very simple)
    if re.search(r'/\s*0\b', combined_diff):
        warnings.append("Possible division by zero detected.")

    # Basic: functions added but no obvious validation keywords near them
    # This is a heuristic: if functions are added and words like 'validate'/'check' not in diff
    if "def " in combined_diff and not re.search(r'validate|check|assert|raise', combined_diff, re.IGNORECASE):
        warnings.append("New functions added but no validation/guards seen (heuristic).")

    # Example: magic numbers or TODO markers
    if "TODO" in combined_diff or "FIXME" in combined_diff:
        warnings.append("TODO/FIXME markers found in diff.")

    return list(dict.fromkeys(warnings))  # deduplicate while preserving order


def explain_function_from_patch(fn_name, files_changed, max_lines=4):
    """
    Try to create a short natural-language explanation for a function by scanning
    the added lines around its definition in the patch and docstring lines.
    This is heuristic — looks for docstrings, comments, and named patterns.
    """
    for file in files_changed:
        diff = file.get("patch", "") or ""
        # find the function definition line and a few subsequent added lines
        # pattern matches lines that start with +def fn_name(...):
        pattern = rf'(^\+.*def\s+{re.escape(fn_name)}\s*\(.*\):[\s\S]{{0,400}})'
        m = re.search(pattern, diff, re.MULTILINE)
        if m:
            block = m.group(0)
            # try to extract docstring inside the added block
            doc_m = re.search(r'["\']{3}([\s\S]*?)["\']{3}', block)
            if doc_m:
                text = doc_m.group(1).strip().splitlines()[0: max_lines]
                return " ".join([t.strip() for t in text]).strip()
            # otherwise look for comment lines or obvious return/compute lines
            comment_lines = re.findall(r'^\+\s*#\s*(.*)$', block, re.MULTILINE)
            if comment_lines:
                return comment_lines[0].strip()
            # fallback: use function name heuristics
            # split camelCase or snake_case into words
            words = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', fn_name)  # camelCase -> words
            words = words.replace("_", " ")
            return f"Performs operation related to `{words}`."
    # if nothing found
    words = fn_name.replace("_", " ")
    return f"Performs operation related to `{words}`."


def compute_risk_score(files_changed, additions, deletions, warnings, tests_found):
    """
    Heuristic risk score (0 low - 10 high):
    - Start with a base from size
    - Increase with deletions, warnings, and if no tests found
    """
    score = 0.0

    # size impact
    total_changes = additions + deletions
    if total_changes <= 10:
        score += 1.0
    elif total_changes <= 50:
        score += 3.0
    elif total_changes <= 200:
        score += 5.0
    else:
        score += 7.0

    # files changed
    if len(files_changed) >= 5:
        score += 1.5
    elif len(files_changed) >= 2:
        score += 0.7

    # deletions tend to increase risk
    if deletions > 0:
        score += min(deletions * 0.05, 2.0)

    # warnings increase risk
    score += len(warnings) * 1.2

    # no tests => bump
    if not tests_found:
        score += 1.5

    # clamp to 0-10 and round to one decimal
    score = max(0.0, min(10.0, score))
    return round(score, 1)


def detect_tests_present(files_changed):
    """
    Heuristic detection whether PR includes tests:
    - filename contains 'test' or in a 'tests/' directory
    - or added functions inside files named test_*.py
    """
    for file in files_changed:
        fname = file.get("filename", "").lower()
        if "/tests/" in fname or fname.startswith("tests/") or "test_" in fname or "/test_" in fname:
            return True
    # also scan for functions that look like tests in diffs (pytest style)
    for file in files_changed:
        diff = file.get("patch", "") or ""
        if re.search(r'^\+.*def\s+test_', diff, re.MULTILINE):
            return True
    return False


def generate_summary(pr_data):
    title = pr_data.get("title", "").strip()
    body = pr_data.get("body", "") or ""
    files_changed = pr_data.get("files", []) or []
    additions = pr_data.get("additions", 0) or 0
    deletions = pr_data.get("deletions", 0) or 0

    # Basic PR summary
    summary_lines = []
    summary_lines.append("PR Summary:")
    summary_lines.append(f"Title: {title if title else 'No title'}")
    summary_lines.append("")
    summary_lines.append("Description:")
    summary_lines.append(body if body else "No description provided.")
    summary_lines.append("")

    # Code Insights: functions/classes added
    functions, classes = extract_code_insights(files_changed)
    summary_lines.append("Code Insights:")
    if functions:
        for f in functions:
            summary_lines.append(f"• Function `{f}` added")
    if classes:
        for c in classes:
            summary_lines.append(f"• Class `{c}` added")
    if not functions and not classes:
        summary_lines.append("No significant new functions or classes detected.")
    summary_lines.append("")

    # Code Explanation (natural-language short explanations per function)
    if functions or classes:
        summary_lines.append("Code Explanation:")
        for f in functions:
            expl = explain_function_from_patch(f, files_changed)
            summary_lines.append(f"• `{f}`: {expl}")
        for c in classes:
            # short class heuristic
            words = c.replace("_", " ")
            summary_lines.append(f"• `{c}`: Defines the `{words}` class (see file diff for details).")
    else:
        summary_lines.append("Code Explanation:")
        summary_lines.append("No new functions/classes to explain.")
    summary_lines.append("")

    # Warnings
    warnings = detect_code_warnings(files_changed)
    summary_lines.append("Warnings:")
    if warnings:
        for w in warnings:
            summary_lines.append(f"- {w}")
    else:
        summary_lines.append("No potential issues detected.")
    summary_lines.append("")

    # Test coverage hint
    tests_found = detect_tests_present(files_changed)
    summary_lines.append("Tests Present:")
    summary_lines.append("Yes" if tests_found else "No — no tests found in this PR.")
    summary_lines.append("")

    # Risk score
    risk = compute_risk_score(files_changed, additions, deletions, warnings, tests_found)
    summary_lines.append("Risk Score:")
    summary_lines.append(f"{risk}/10 (0 = low risk, 10 = high risk)")
    summary_lines.append("")

    # Keep existing automated review/safety/overview handled by other modules (they'll be attached separately)
    final = "\n".join(summary_lines).strip()
    return final
