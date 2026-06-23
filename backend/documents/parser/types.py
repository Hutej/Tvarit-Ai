from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentMetadata(BaseModel):
    page_count: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    creation_date: Optional[datetime] = None
    producer: Optional[str] = None
    is_scanned: Optional[bool] = None
    language: Optional[str] = None
    document_type_hint: Optional[str] = None
    custom_attributes: Dict[str, Any] = Field(default_factory=dict)

class ParsedTable(BaseModel):
    page: int
    data: List[List[str]]
    title: Optional[str] = None

class ParsedImage(BaseModel):
    page: int
    storage_path: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ParserResult(BaseModel):
    raw_text: str
    tables: List[ParsedTable] = Field(default_factory=list)
    metadata: DocumentMetadata
    images: List[ParsedImage] = Field(default_factory=list)
    page_count: int = 0
    language: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
