def summary_agent(state):

    content = ""

    if state.get("research_result"):
        content += state["research_result"]

    if state.get("drug_result"):
        content += state["drug_result"]

    if state.get("report_result"):
        content += state["report_result"]

    summary_text = (
        "Summary Agent completed.\n\n"
        "The system has processed the user query using the selected specialized agent. "
        "The response includes the most relevant information found from the available sources. "
        "For medical decisions, the user should verify the information with a qualified healthcare professional."
    )

    return {
        "summary": summary_text
    }