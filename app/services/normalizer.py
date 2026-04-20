from typing import Any, Dict, List, Optional


def _as_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _dedupe_keep_order(values: List[str]) -> List[str]:
    deduped: List[str] = []
    seen = set()

    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)

    return deduped


def _normalize_age(value: Any) -> Optional[int]:
    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value if value >= 0 else None

    if isinstance(value, float):
        if value.is_integer() and value >= 0:
            return int(value)
        return None

    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)

    return None


def normalize_gender(gender: Any) -> Optional[str]:
    if not isinstance(gender, str):
        return None

    value = gender.strip().lower()
    if not value:
        return None

    if value in ["m", "male"]:
        return "male"
    if value in ["f", "female"]:
        return "female"

    return "other"


def _normalize_code_list(value: Any) -> List[str]:
    if isinstance(value, str):
        raw_values = [value]
    elif isinstance(value, (list, tuple, set)):
        raw_values = list(value)
    else:
        raw_values = []

    cleaned: List[str] = []

    for item in raw_values:
        if item is None or isinstance(item, bool):
            continue

        if isinstance(item, dict):
            item = item.get("code")

        if not isinstance(item, str):
            item = str(item)

        code = item.strip().upper()
        if code:
            cleaned.append(code)

    return _dedupe_keep_order(cleaned)


def _normalize_notes(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None

    text = value.strip()
    return text if text else None


def _normalize_documents(value: Any) -> List[Dict[str, Any]]:
    documents = _as_list(value)
    normalized_documents: List[Dict[str, Any]] = []

    for document in documents:
        if not isinstance(document, dict):
            continue

        doc_type = document.get("type")
        content = document.get("content")

        normalized_documents.append(
            {
                "type": doc_type.strip() if isinstance(doc_type, str) else "",
                "content": content.strip() if isinstance(content, str) else None,
            }
        )

    return normalized_documents


def normalize_input(data: Any) -> Dict[str, Any]:
    input_data = _as_dict(data)

    patient_raw = _as_dict(input_data.get("patient"))
    clinical_raw = _as_dict(input_data.get("clinical"))

    patient = {
        "age": _normalize_age(patient_raw.get("age")),
        "gender": normalize_gender(patient_raw.get("gender")),
    }

    clinical = {
        "diagnosis_codes": _normalize_code_list(clinical_raw.get("diagnosis_codes")),
        "procedure_codes": _normalize_code_list(clinical_raw.get("procedure_codes")),
        "notes": _normalize_notes(clinical_raw.get("notes")),
    }

    normalized = dict(input_data)
    normalized["patient"] = patient
    normalized["clinical"] = clinical
    normalized["documents"] = _normalize_documents(input_data.get("documents"))
    normalized["payer"] = _as_dict(input_data.get("payer"))

    return normalized