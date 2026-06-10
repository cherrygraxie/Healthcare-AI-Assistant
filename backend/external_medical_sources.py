import requests


def search_loinc(test_name):
    url = "https://clinicaltables.nlm.nih.gov/api/loinc_items/v3/search"

    params = {
        "terms": test_name,
        "maxList": 3
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        results = []

        if len(data) >= 4:
            codes = data[1]
            displays = data[3]

            for i in range(len(codes)):
                display_text = displays[i][0] if displays[i] else "Unknown"

                results.append({
                    "loinc_code": codes[i],
                    "name": display_text
                })

        return results

    except Exception:
        return []