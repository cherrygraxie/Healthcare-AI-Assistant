from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.research_agent import research_agent
from agents.drug_agent import drug_agent
from agents.report_agent import report_agent
from agents.summary_agent import summary_agent
from agents.verification_agent import verification_agent
from health_check_agent import health_check_agent

class AgentState(TypedDict):
    question: str
    route: str
    research_result: str
    drug_result: str
    report_result: str
    health_result: str
    health_data: dict
    summary: str
    verification: str
    final_answer: str
    


def supervisor_agent(state):
    question = state["question"].lower()

    import re
    pattern = r"[A-Za-z0-9\s\-]+[:=]\s*[0-9.]+"

    if re.search(pattern, question):
        return {"route": "health"}

    health_keywords = [
    "esr",
    "sodium",
    "potassium",
    "chloride",
    "creatinine",
    "tsh",
    "t3",
    "t4",
    "vitamin",
    "calcium",
    "phosphorus",
    "albumin",
    "sgot",
    "sgpt",
    "ferritin",
    "hemoglobin",
    "hb",
    "wbc",
    "rbc",
    "hdl",
    "ldl",
    "hba1c",
    "glucose",
    "triglycerides",
    "cholesterol",
    "crp",
    "uric acid"
]
    
    for keyword in health_keywords:
        if keyword in question:
            return {"route": "health"}

    drug_keywords = [
        "medicine",
        "drug",
        "tablet",
        "capsule",
        "side effect",
        "side effects",
        "dose",
        "dosage",
        "interaction",
        "interactions",
        "prescription",
        "metformin",
        "ibuprofen",
        "paracetamol",
        "aspirin"
    ]

    report_keywords = [
        "report",
        "blood test",
        "lab result",
        "lab report",
        "scan",
        "xray",
        "x-ray",
        "mri",
        "ct scan",
        "medical report",
        "health report"
    ]

    research_keywords = [
    "research paper",
    "papers",
    "pubmed",
    "journal",
    "study",
    "literature",
    "article"
    ]

    for keyword in research_keywords:
        if keyword in question:
            return {"route": "report"}

    for keyword in drug_keywords:
        if keyword in question:
            return {"route": "drug"}

    for keyword in report_keywords:
        if keyword in question:
            return {"route": "report"}

    return {"route": "report"}


def router(state):
    return state["route"]


def final_agent(state):
    final_text = ""

    if state.get("research_result"):
        final_text += state["research_result"] + "\n\n"

    if state.get("drug_result"):
        final_text += state["drug_result"] + "\n\n"

    if state.get("health_result"):
        final_text += state["health_result"] + "\n\n"

    if state.get("report_result"):
        final_text += state["report_result"] + "\n\n"

    final_text += state.get("summary", "") + "\n\n"
    final_text += state.get("verification", "")

    return {"final_answer": final_text}


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("research", research_agent)
    graph.add_node("drug", drug_agent)
    graph.add_node("report", report_agent)
    graph.add_node("summary", summary_agent)
    graph.add_node("verification", verification_agent)
    graph.add_node("final", final_agent)
    graph.add_node("health", health_check_agent)

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        router,
        {
            "research": "research",
            "drug": "drug",
            "report": "report",
            "health": "health"
        }
    )

    graph.add_edge("research", "summary")
    graph.add_edge("drug", "summary")
    graph.add_edge("report", "summary")
    graph.add_edge("health", "summary")

    graph.add_edge("summary", "verification")
    graph.add_edge("verification", "final")
    graph.add_edge("final", END)

    return graph.compile()