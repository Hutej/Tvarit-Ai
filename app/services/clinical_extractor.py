import re
from typing import Any, Dict, List

from app.config.clinical_patterns import CONDITION_PATTERNS


NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def _normalize_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""

    lowered = value.lower().strip()
    if not lowered:
        return ""

    return " ".join(NON_ALNUM_RE.sub(" ", lowered).split())


def _normalize_code_list(value: Any) -> List[str]:
    if isinstance(value, str):
        raw_values = [value]
    elif isinstance(value, (list, tuple, set)):
        raw_values = list(value)
    else:
        raw_values = []

    normalized: List[str] = []
    seen = set()

    for item in raw_values:
        if item is None or isinstance(item, bool):
            continue

        if isinstance(item, dict):
            item = item.get("code")

        if item is None:
            continue

        if not isinstance(item, str):
            item = str(item)

        code = item.strip().upper()
        if not code or code in seen:
            continue

        seen.add(code)
        normalized.append(code)

    return normalized


def _keyword_matches(normalized_notes: str, keyword: Any) -> bool:
    keyword_normalized = _normalize_text(keyword)
    if not keyword_normalized:
        return False

    # Space padding keeps matching aligned to token boundaries in normalized text.
    return f" {keyword_normalized} " in f" {normalized_notes} "


def _safe_weight(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def extract_from_notes(notes: Any, structured_codes: Any = None) -> Dict[str, Any]:
    normalized_notes = _normalize_text(notes)
    structured = _normalize_code_list(structured_codes)
    structured_set = set(structured)

    inferred_codes: List[str] = []
    confidence: Dict[str, float] = {}

    for code, pattern_data in CONDITION_PATTERNS.items():
        if not isinstance(pattern_data, dict):
            continue

        normalized_code = str(code).strip().upper()
        if not normalized_code or normalized_code in structured_set:
            continue

        keywords = pattern_data.get("keywords")
        if not isinstance(keywords, list) or not normalized_notes:
            continue

        if any(_keyword_matches(normalized_notes, keyword) for keyword in keywords):
            inferred_codes.append(normalized_code)
            confidence[normalized_code] = _safe_weight(pattern_data.get("weight"))

    return {
        "structured_codes": structured,
        "inferred_codes": inferred_codes,
        "confidence": confidence,
    }