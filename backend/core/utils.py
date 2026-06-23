import uuid
from typing import Any

def generate_uuid() -> str:
    """Generate a standard UUID string."""
    return str(uuid.uuid4())

def safe_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary."""
    return dictionary.get(key, default)
