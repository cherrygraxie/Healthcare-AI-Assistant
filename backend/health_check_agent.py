import re
from clinical_rules import validate_value
from external_medical_sources import search_loinc


def extract_gender(question):
    text = question.lower()

    if "female" in text or "woman" in text:
        return "female"

    if "male" in text or "man" in text:
        return "male"

    return "all"


def extract_test_values(question):
    pattern = r"([A-Za-z0-9%.\-\s]+)\s*[:=]\s*([0-9.]+)"
    matches = re.findall(pattern, question)

    tests = []

    ignore_keys = ["age", "gender", "sex"]

    for name, value in matches:
        clean_name = name.strip()

        if clean_name.lower() in ignore_keys:
            continue

        tests.append({
            "test": clean_name,
            "value": value
        })

    return tests


def health_check_agent(state):
    question = state["question"]

    gender = extract_gender(question)
    tests = extract_test_values(question)

    if not tests:
        return {
            "health_result": (
                "Health Check Agent completed.\n\n"
                "I could not detect test values from your message.\n\n"
                "Use this format:\n"
                "Gender: female, ESR: 28, Sodium: 150, Creatinine: 0.8"
            )
        }

    validated_results = []

    for item in tests:
        result = validate_value(
            item["test"],
            item["value"],
            gender
        )
        validated_results.append(result)

    normal = []
    abnormal = []
    unverified = []

    for result in validated_results:
        if result["status"] == "NORMAL":
            normal.append(result)
        elif result["status"] in ["LOW", "HIGH"]:
            abnormal.append(result)
        else:
            unverified.append(result)

    response = "Health Check Agent completed.\n\n"
    response += f"Gender used for reference range: {gender}\n\n"

    if abnormal:
        response += "Abnormal Results:\n"
        for item in abnormal:
            response += (
                f"- {item['test']}: {item['value']} {item['unit']}\n"
                f"  Reference Range: {item['range']}\n"
                f"  Status: {item['status']}\n"
            )
        response += "\n"

    if normal:
        response += "Normal Results:\n"
        for item in normal:
            response += (
                f"- {item['test']}: {item['value']} {item['unit']}\n"
                f"  Reference Range: {item['range']}\n"
                f"  Status: NORMAL\n"
            )
        response += "\n"

    if unverified:
        response += "Unverified Results:\n"

        for item in unverified:
            loinc_matches = search_loinc(item["test"])

            response += (
                f"- {item['test']}: {item['value']}\n"
                f"  Status: {item['status']}\n"
                f"  Reason: No local reference range available.\n"
            )

            if loinc_matches:
                response += "  Possible LOINC Matches:\n"
                for match in loinc_matches:
                    response += (
                        f"  - {match['name']} "
                        f"(LOINC: {match['loinc_code']})\n"
                    )
            else:
                response += "  Possible LOINC Matches: Not found.\n"

    response += "\n"

    response += (
        "Safety Note:\n"
        "This is a rule-based screening result, not a diagnosis. "
        "Reference ranges can vary by lab, age, method, and clinical condition. "
        "Please confirm with a qualified doctor."
    )


    return {
        "health_result": response,
        "health_data": {
            "abnormal": abnormal,
            "normal": normal,
            "unverified": unverified,
            "gender": gender
        }
    }