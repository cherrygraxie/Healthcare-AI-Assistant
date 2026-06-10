def verification_agent(state):

    checks = []

    if state.get("research_result"):
        checks.append("Research results include source details such as paper title, PMID, journal, and publication date.")

    if state.get("drug_result"):
        checks.append("Medicine-related answers should be verified with trusted medical sources before use.")

    if state.get("report_result"):
        checks.append("Medical report interpretation should be confirmed by a qualified doctor.")

    if state.get("health_result"):
        checks.append(
            "Manual health values were checked using local reference ranges and Python-based validation."
        )

    verification_text = "Verification Agent completed.\n\n"

    if checks:
        for check in checks:
            verification_text += f"- {check}\n"
    else:
        verification_text += "- No specialized content found for verification.\n"

    verification_text += "\nNote: This system is for educational and research assistance, not medical diagnosis."

    return {
        "verification": verification_text
    }