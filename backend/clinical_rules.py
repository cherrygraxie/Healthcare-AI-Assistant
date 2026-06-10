REFERENCE_RANGES = {
    "esr": {
        "female": {"low": 0, "high": 20, "unit": "mm/hr"},
        "male": {"low": 0, "high": 15, "unit": "mm/hr"}
    },
    "sodium": {
        "all": {"low": 136, "high": 146, "unit": "mEq/L"}
    },
    "potassium": {
        "all": {"low": 3.5, "high": 5.1, "unit": "mEq/L"}
    },
    "chloride": {
        "all": {"low": 101, "high": 109, "unit": "mEq/L"}
    },
    "creatinine": {
        "female": {"low": 0.51, "high": 0.95, "unit": "mg/dL"},
        "male": {"low": 0.67, "high": 1.17, "unit": "mg/dL"}
    },
    "tsh": {
        "all": {"low": 0.35, "high": 5.50, "unit": "uIU/mL"}
    },
    "t3": {
        "all": {"low": 0.60, "high": 1.81, "unit": "ng/mL"}
    },
    "t4": {
        "all": {"low": 5.01, "high": 12.45, "unit": "ug/dL"}
    },
    "vitamin b12": {
        "all": {"low": 211, "high": 911, "unit": "pg/mL"}
    },
    "vitamin d3": {
        "all": {"low": 75, "high": 250, "unit": "nmol/L"}
    },
    "phosphorus": {
        "all": {"low": 2.40, "high": 4.40, "unit": "mg/dL"}
    },
    "calcium": {
        "all": {"low": 8.80, "high": 10.60, "unit": "mg/dL"}
    },
    "albumin": {
        "all": {"low": 3.50, "high": 5.20, "unit": "g/dL"}
    },
    "platelet": {
        "all": {"low": 150, "high": 450, "unit": "thou/mm3"}
    },
    "serum iron": {
        "all": {"low": 50, "high": 170, "unit": "ug/dL"}
    },
    "tibc": {
        "all": {"low": 250, "high": 425, "unit": "ug/dL"}
    },
    "transferrin saturation": {
        "all": {"low": 15, "high": 50, "unit": "%"}
    },
    "amylase": {
        "all": {"low": 28, "high": 100, "unit": "U/L"}
    },
    "sgot": {
        "all": {"low": 0, "high": 35, "unit": "U/L"}
    },
    "sgpt": {
        "all": {"low": 0, "high": 35, "unit": "U/L"}
    },
    "ferritin": {
        "female": {"low": 12, "high": 150, "unit": "ng/mL"},
        "male": {"low": 24, "high": 336, "unit": "ng/mL"}
    },
    "hemoglobin": {
        "female": {"low": 12.0, "high": 15.5, "unit": "g/dL"},
        "male": {"low": 13.5, "high": 17.5, "unit": "g/dL"}
    },
    "wbc": {
        "all": {"low": 4.0, "high": 10.0, "unit": "thou/mm3"}
    },
    "rbc": {
        "female": {"low": 3.8, "high": 5.2, "unit": "million/mm3"},
        "male": {"low": 4.5, "high": 5.9, "unit": "million/mm3"}
    },
    "fasting glucose": {
        "all": {"low": 70, "high": 100, "unit": "mg/dL"}
    },
    "hba1c": {
        "all": {"low": 0, "high": 5.6, "unit": "%"}
    },
    "ldl": {
        "all": {"low": 0, "high": 100, "unit": "mg/dL"}
    },
    "hdl": {
        "female": {"low": 50, "high": 100, "unit": "mg/dL"},
        "male": {"low": 40, "high": 100, "unit": "mg/dL"}
    },
    "triglycerides": {
        "all": {"low": 0, "high": 150, "unit": "mg/dL"}
    },
    "crp": {
        "all": {"low": 0, "high": 3, "unit": "mg/L"}
    },
    "hs-crp": {
        "all": {"low": 0, "high": 3, "unit": "mg/L"}
    },
    "uric acid": {
        "female": {"low": 2.6, "high": 6.0, "unit": "mg/dL"},
        "male": {"low": 3.5, "high": 7.2, "unit": "mg/dL"}
    },
    "total protein": {
        "all": {"low": 6.4, "high": 8.3, "unit": "g/dL"}
    },
    "bilirubin": {
        "all": {"low": 0.3, "high": 1.2, "unit": "mg/dL"}
    },
    "alkaline phosphatase": {
        "all": {"low": 30, "high": 120, "unit": "U/L"}
    }
}


ALIASES = {
    "platelet count": "platelet",
    "platelets": "platelet",
    "erythrocyte sedimentation rate": "esr",
    "serum amylase": "amylase",
    "s albumin": "albumin",
    "s. albumin": "albumin",
    "ast": "sgot",
    "alt": "sgpt",
    "% transferrin sat": "transferrin saturation",
    "% transferrin saturation": "transferrin saturation",
        "hb": "hemoglobin",
    "white blood cells": "wbc",
    "leucocyte": "wbc",
    "leukocyte": "wbc",
    "red blood cells": "rbc",
    "glucose fasting": "fasting glucose",
    "fbs": "fasting glucose",
    "glycated hemoglobin": "hba1c",
    "total cholesterol": "cholesterol",
    "ldl cholesterol": "ldl",
    "hdl cholesterol": "hdl",
    "hs crp": "hs-crp",
    "high sensitivity crp": "hs-crp",
    "c reactive protein": "crp",
    "total bilirubin": "bilirubin",
    "alk phosphatase": "alkaline phosphatase",
    "alk. phosphatase": "alkaline phosphatase"
}


def normalize_test_name(test_name):
    key = test_name.lower().strip()
    key = key.replace(":", "")
    return ALIASES.get(key, key)


def get_reference_range(test_name, gender="all"):
    key = normalize_test_name(test_name)

    if key not in REFERENCE_RANGES:
        return None

    ranges = REFERENCE_RANGES[key]
    gender = gender.lower().strip()

    if gender in ranges:
        return ranges[gender]

    if "all" in ranges:
        return ranges["all"]

    return None


def validate_value(test_name, value, gender="all"):
    ref = get_reference_range(test_name, gender)

    if ref is None:
        return {
            "test": test_name,
            "value": value,
            "unit": "",
            "range": "Not available",
            "status": "UNVERIFIED"
        }

    try:
        numeric_value = float(value)
    except ValueError:
        return {
            "test": test_name,
            "value": value,
            "unit": ref["unit"],
            "range": f"{ref['low']} - {ref['high']}",
            "status": "INVALID_VALUE"
        }

    if numeric_value < ref["low"]:
        status = "LOW"
    elif numeric_value > ref["high"]:
        status = "HIGH"
    else:
        status = "NORMAL"

    return {
        "test": test_name,
        "value": numeric_value,
        "unit": ref["unit"],
        "range": f"{ref['low']} - {ref['high']}",
        "status": status
    }