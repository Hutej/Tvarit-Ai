from ninja import Schema
from pydantic import Field
from datetime import datetime
from typing import Optional, List
import uuid

class DocumentSummary(Schema):
    id: uuid.UUID
    original_filename: str
    display_name: str
    extension: str
    size: int
    status: str
    document_type: str
    upload_timestamp: datetime

class DocumentDetails(DocumentSummary):
    mime_type: str
    sha256_checksum: str
    processing_stage: str
    page_count: Optional[int] = None
    is_scanned: Optional[bool] = None
    patient_id: Optional[str] = None
    authorization_case_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UploadResponse(Schema):
    message: str
    document: DocumentSummary

class UploadMultipleResponse(Schema):
    message: str
    documents: List[DocumentSummary]

class UpdateDocumentRequest(Schema):
    display_name: Optional[str] = None
    document_type: Optional[str] = None
    patient_id: Optional[str] = None
    authorization_case_id: Optional[str] = None

class DeleteResponse(Schema):
    message: str
    id: uuid.UUID

class PaginationMeta(Schema):
    total: int
    page: int
    limit: int

class ListDocumentsResponse(Schema):
    data: List[DocumentSummary]
    meta: PaginationMeta
