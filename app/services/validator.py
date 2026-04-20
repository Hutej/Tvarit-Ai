def validate_input(data):
    errors = []

    clinical = data.get("clinical")

    if not clinical:
        errors.append({
            "field": "clinical",
            "message": "Clinical section is required"
        })
        return errors

    diagnosis = clinical.get("diagnosis_codes")
    notes = clinical.get("notes")

    if (not diagnosis or len(diagnosis) == 0) and (not notes or notes.strip() == ""):
        errors.append({
            "field": "clinical",
            "message": "Provide at least diagnosis_codes or clinical notes"
        })

    return errors