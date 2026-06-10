from rag import ask_document


def report_agent(state):
    question = state["question"]

    try:
        answer = ask_document(question, "")

        return {
            "report_result": (
                "Medical Report Agent completed.\n\n"
                f"Query: {question}\n\n"
                "Report Analysis:\n"
                f"{answer}\n\n"
                "Important Warning:\n"
                "This report analysis is for educational understanding only. "
                "Please consult a qualified doctor for diagnosis, treatment, or medical decisions."
            )
        }

    except Exception:
        return {
            "report_result": (
                "Medical Report Agent completed.\n\n"
                "No uploaded medical report was found or the report could not be analyzed.\n\n"
                "Please upload a medical report PDF first using the upload feature, then ask your question again."
            )
        }