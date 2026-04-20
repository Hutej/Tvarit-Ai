import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from app.services.validator import validate_input
from app.services.normalizer import normalize_input
from app.services.clinical_extractor import extract_from_notes

from app.config.clinical_patterns import CONDITION_PATTERNS

logger = logging.getLogger(__name__)


def _debug_log(debug: bool, message: str, details: Optional[Any] = None) -> None:
    if not debug:
        return

    if details is None:
        logger.debug(message)
        return

    logger.debug("%s | %s", message, details)


def _dedupe_codes(codes: Iterable[Any]) -> List[str]:
    deduped: List[str] = []
    seen = set()

    for code in codes:
        if code is None or isinstance(code, bool):
            continue

        if not isinstance(code, str):
            code = str(code)

        normalized_code = code.strip().upper()
        if not normalized_code or normalized_code in seen:
            continue

        seen.add(normalized_code)
        deduped.append(normalized_code)

    return deduped


def _as_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def _parse_error_messages(errors: Any) -> List[str]:
    if errors is None:
        return []

    if isinstance(errors, str):
        message = errors.strip()
        return [message] if message else []

    if isinstance(errors, dict):
        field = errors.get("field")
        message = errors.get("message")

        if isinstance(message, str) and message.strip():
            if isinstance(field, str) and field.strip():
                return [f"{field.strip()}: {message.strip()}"]
            return [message.strip()]

        return [str(errors)]

    if isinstance(errors, (list, tuple, set)):
        messages: List[str] = []
        for item in errors:
            messages.extend(_parse_error_messages(item))
        return messages

    return [str(errors)]


def _build_error_response(errors: Any) -> Dict[str, Any]:
    messages = _parse_error_messages(errors)
    if not messages:
        messages = ["Unknown pipeline error"]

    return {
        "status": "error",
        "data": None,
        "errors": messages,
    }


def _merge_diagnosis_codes(structured_codes: Any, inferred_codes: Any) -> List[str]:
    combined: List[str] = []
    seen = set()

    for source in [structured_codes, inferred_codes]:
        normalized_source = _dedupe_codes(source if isinstance(source, (list, tuple, set)) else [])
        for code in normalized_source:
            if code in seen:
                continue
            seen.add(code)
            combined.append(code)

    return combined


def enrich_codes(codes: Any) -> List[Dict[str, str]]:
    normalized_codes = _dedupe_codes(codes if isinstance(codes, (list, tuple, set)) else [])
    enriched: List[Dict[str, str]] = []

    for code in normalized_codes:
        pattern = CONDITION_PATTERNS.get(code)
        description = None

        if isinstance(pattern, dict):
            description = pattern.get("description")

        if not isinstance(description, str) or not description.strip():
            description = "Unknown"

        enriched.append(
            {
                "code": code,
                "description": description.strip(),
            }
        )

    return enriched


def run_pipeline(input_data: dict, debug: bool = False) -> Dict[str, Any]:
    try:
        if not isinstance(input_data, dict):
            return _build_error_response("Input payload must be a JSON object")

        # 1. Validate
        errors = validate_input(input_data)
        if errors:
            return _build_error_response(errors)

        # 2. Normalize
        normalized = normalize_input(input_data)

        # 3. Extract
        clinical = _as_dict(normalized.get("clinical"))
        notes = clinical.get("notes")
        structured_codes = _as_list(clinical.get("diagnosis_codes"))

        extracted = extract_from_notes(notes, structured_codes=structured_codes)
        extracted_data = _as_dict(extracted)

        extracted_structured = _as_list(extracted_data.get("structured_codes"))
        extracted_inferred = _as_list(extracted_data.get("inferred_codes"))
        combined_codes = _merge_diagnosis_codes(extracted_structured, extracted_inferred)
        enriched_codes = enrich_codes(combined_codes)

        confidence = extracted_data.get("confidence")
        if not isinstance(confidence, dict):
            confidence = {}

        # 4. Build NIF
        patient = _as_dict(normalized.get("patient"))

        nif = {
            "request_id": str(uuid.uuid4()),
            "patient": {
                "age": patient.get("age"),
                "gender": patient.get("gender"),
            },
            "clinical": {
                "diagnosis_codes": enriched_codes,
                "procedure_codes": _as_list(clinical.get("procedure_codes")),
                "notes": notes if isinstance(notes, str) else None,
                "extracted": {
                    "structured_codes": _dedupe_codes(extracted_structured),
                    "inferred_codes": _dedupe_codes(extracted_inferred),
                    "confidence": confidence,
                },
            },
            "documents": _as_list(normalized.get("documents")),
            "payer": _as_dict(normalized.get("payer")),
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "api",
                "version": "v1",
            },
        }

        return {
            "status": "success",
            "data": nif,
            "errors": None,
        }
    except Exception as exc:
        _debug_log(debug, "Input pipeline failed", details=str(exc))
        if debug:
            return _build_error_response(["Internal pipeline error", str(exc)])
        return _build_error_response("Internal pipeline error")