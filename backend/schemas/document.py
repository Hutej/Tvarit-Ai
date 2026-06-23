from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.base import EntityBase
from schemas.enums import DocumentType

class DocumentReference(EntityBase):
    filename: str
    document_type: DocumentType
    url: Optional[str] = None
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None
    hash: Optional[str] = None
