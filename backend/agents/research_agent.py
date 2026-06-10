from research_search import research_chat


def research_agent(state):
    question = state["question"]

    result = research_chat(question)

    local_papers = result.get("local_papers", [])
    pubmed_papers = result.get("pubmed_papers", [])

    local_text = ""
    if local_papers:
        for paper in local_papers[:3]:
            clean_name = paper.replace("./knowledge_base/research_papers\\", "")
            clean_name = clean_name.replace("./knowledge_base/research_papers/", "")
            local_text += f"- {clean_name}\n"
    else:
        local_text = "No local papers found.\n"

    pubmed_text = ""
    if pubmed_papers:
        for paper in pubmed_papers[:3]:
            pubmed_text += (
                f"- {paper.get('title', 'No title')}\n"
                f"  PMID: {paper.get('pmid', 'N/A')}\n"
                f"  Journal: {paper.get('journal', 'N/A')}\n"
                f"  Published: {paper.get('pub_date', 'N/A')}\n\n"
            )
    else:
        pubmed_text = "No PubMed papers found.\n"

    return {
        "research_result": (
            "Research Agent completed.\n\n"
            f"Query: {question}\n\n"
            "Top Local Research Papers:\n"
            f"{local_text}\n"
            "Top PubMed Research Papers:\n"
            f"{pubmed_text}"
        )
    }