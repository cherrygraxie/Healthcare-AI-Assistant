import requests


def search_rxnorm(medicine_name):
    url = "https://rxnav.nlm.nih.gov/REST/drugs.json"

    params = {
        "name": medicine_name
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        concepts = data.get("drugGroup", {}).get("conceptGroup", [])

        results = []

        for group in concepts:
            for concept in group.get("conceptProperties", []):
                results.append({
                    "name": concept.get("name", "Unknown"),
                    "rxcui": concept.get("rxcui", "N/A"),
                    "synonym": concept.get("synonym", "N/A")
                })

        return results[:5]

    except Exception as e:
        return []


def extract_medicine_name(question):
    remove_words = [
        "check", "this", "medicine", "drug", "tablet",
        "capsule", "details", "about", "tell", "me",
        "information", "for", "of", "the"
    ]

    words = question.lower().replace("?", "").split()

    medicine_words = [
        word for word in words
        if word not in remove_words
    ]

    return " ".join(medicine_words).strip()


def drug_agent(state):
    question = state["question"]

    medicine_name = extract_medicine_name(question)

    if not medicine_name:
        return {
            "drug_result": (
                "Drug Agent completed.\n\n"
                "Please provide a medicine name.\n\n"
                "Example: Check medicine metformin"
            )
        }

    results = search_rxnorm(medicine_name)

    if results:

        medicine_text = ""

        for index, medicine in enumerate(results, start=1):
            medicine_text += (
                f"{index}. {medicine['name']}\n"
                f"   RxCUI: {medicine['rxcui']}\n"
            )
        

        response = (
            "Drug Agent completed.\n\n"
            f"Medicine searched: {medicine_name}\n\n"
            "Best Matching Medicine Records:\n"
            f"{medicine_text}\n"
            "Safety Note:\n"
            "This result identifies possible medicine records. "
            "It does not provide dosage instructions, diagnosis, or treatment advice. "
            "Please confirm usage, dosage, side effects, and interactions with a qualified doctor or pharmacist."
        )

    else:
        response = (
            "Drug Agent completed.\n\n"
            f"Medicine searched: {medicine_name}\n\n"
            "No matching medicine record was found from RxNorm.\n\n"
            "Safety Note:\n"
            "Please check the spelling or consult a qualified doctor or pharmacist."
        )

    return {
        "drug_result": response
    }