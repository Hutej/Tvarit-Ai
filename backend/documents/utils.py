import os
import hashlib
import uuid
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Tuple
from documents.exceptions import (
    InvalidExtensionException,
    InvalidMimeTypeException,
    FileTooLargeException,
    StorageException
)
from documents.constants import DocumentType

ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
UPLOAD_DIR = Path('media/documents')

def generate_safe_filename(original_filename: str) -> Tuple[str, str, str]:
    """
    Generate a secure UUID-based filename.
    Returns (safe_filename, original_name, extension).
    """
    ext = os.path.splitext(original_filename)[1].lower()
    safe_filename = f"{uuid.uuid4()}{ext}"
    return safe_filename, original_filename, ext

def generate_sha256(file_content: bytes) -> str:
    """Generate SHA256 checksum for file content."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_content)
    return sha256_hash.hexdigest()

def validate_extension(extension: str) -> None:
    """Validate file extension."""
    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidExtensionException(f"Extension {extension} is not allowed. Allowed: {ALLOWED_EXTENSIONS}")

def validate_mime_type(mime_type: str) -> None:
    """Validate MIME type."""
    # Basic check - in production you'd use python-magic
    allowed_mimes = [
        'application/pdf', 'image/png', 'image/jpeg', 
        'image/tiff', 'image/bmp'
    ]
    if mime_type not in allowed_mimes:
        raise InvalidMimeTypeException(f"MIME type {mime_type} is not allowed.")

def validate_file_size(size: int) -> None:
    """Validate file size."""
    if size > MAX_FILE_SIZE:
        raise FileTooLargeException(f"File size {size} exceeds maximum {MAX_FILE_SIZE} bytes.")

def ensure_directory_exists(path: Path) -> None:
    """Ensure storage directory exists."""
    path.mkdir(parents=True, exist_ok=True)

def store_file(file_content: bytes, filename: str) -> str:
    """Store file and return relative path."""
    try:
        # Organize by year/month/day
        today = datetime.now()
        date_path = Path(str(today.year)) / f"{today.month:02d}" / f"{today.day:02d}"
        full_dir = UPLOAD_DIR / date_path
        ensure_directory_exists(full_dir)
        
        file_path = full_dir / filename
        with open(file_path, 'wb') as f:
            f.write(file_content)
            
        return str(date_path / filename)
    except Exception as e:
        raise StorageException(f"Failed to store file: {str(e)}")

def classify_document(filename: str) -> DocumentType:
    """
    Basic keyword-based document classifier.
    To be replaced by AI later.
    """
    lower_name = filename.lower()
    if 'lab' in lower_name:
        return DocumentType.LAB_REPORT
    elif 'prescription' in lower_name or 'rx' in lower_name:
        return DocumentType.PRESCRIPTION
    elif 'discharge' in lower_name:
        return DocumentType.DISCHARGE_SUMMARY
    elif 'rad' in lower_name or 'mri' in lower_name or 'xray' in lower_name or 'ct' in lower_name:
        return DocumentType.RADIOLOGY_REPORT
    elif 'note' in lower_name or 'clinic' in lower_name:
        return DocumentType.CLINICAL_NOTE
    elif 'op_' in lower_name or 'operative' in lower_name:
        return DocumentType.OPERATIVE_NOTE
    elif 'path' in lower_name:
        return DocumentType.PATHOLOGY_REPORT
    elif 'referral' in lower_name:
        return DocumentType.REFERRAL
    elif 'insurance' in lower_name or 'form' in lower_name:
        return DocumentType.INSURANCE_FORM
    return DocumentType.UNKNOWN
