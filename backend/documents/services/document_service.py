from typing import List, Optional, Tuple, Dict, Any
from core.services import BaseService
from documents.repositories.document_repository import DocumentRepository
from documents.models import Document
from documents.constants import DocumentStatus, ProcessingStage, DocumentType
from documents.utils import (
    validate_extension,
    validate_mime_type,
    validate_file_size,
    generate_safe_filename,
    generate_sha256,
    store_file,
    classify_document
)
from documents.exceptions import DuplicateDocumentException, DocumentNotFoundException
import mimetypes
import os

class DocumentService(BaseService):
    """
    Service layer for document-related business orchestration.
    """
    def __init__(self):
        super().__init__()
        self.repo = DocumentRepository()

    def process_upload(self, file_content: bytes, original_filename: str, content_type: str) -> Document:
        """
        Handles document validation, saving, and triggering extraction workflows.
        """
        size = len(file_content)
        
        # Validation
        ext = os.path.splitext(original_filename)[1].lower()
        validate_extension(ext)
        validate_mime_type(content_type)
        validate_file_size(size)

        # Checksum
        checksum = generate_sha256(file_content)
        if self.repo.get_by_checksum(checksum):
            raise DuplicateDocumentException()

        # Filename & Storage
        safe_filename, _, _ = generate_safe_filename(original_filename)
        storage_path = store_file(file_content, safe_filename)

        # Classification
        doc_type = classify_document(original_filename)

        # Create Model
        doc = self.repo.create(
            original_filename=original_filename,
            stored_filename=safe_filename,
            display_name=original_filename,
            extension=ext,
            mime_type=content_type,
            size=size,
            sha256_checksum=checksum,
            storage_path=storage_path,
            status=DocumentStatus.VALIDATED,
            processing_stage=ProcessingStage.CLASSIFICATION,
            document_type=doc_type
        )
        return doc

    def process_multiple_uploads(self, files: List[Tuple[bytes, str, str]]) -> List[Document]:
        """
        Process a list of (file_content, filename, content_type) tuples.
        """
        docs = []
        for content, name, ctype in files:
            try:
                doc = self.process_upload(content, name, ctype)
                docs.append(doc)
            except DuplicateDocumentException:
                # Skip duplicates in batch upload
                pass
        return docs

    def get_document(self, doc_id: str) -> Document:
        doc = self.repo.get_active_by_id(doc_id)
        if not doc:
            raise DocumentNotFoundException()
        return doc

    def list_documents(self, page: int = 1, limit: int = 20, filters: Dict[str, Any] = None) -> Tuple[List[Document], int]:
        filters = filters or {}
        offset = (page - 1) * limit
        return self.repo.list_active(offset=offset, limit=limit, **filters)

    def update_document_metadata(self, doc_id: str, data: Dict[str, Any]) -> Document:
        doc = self.repo.update_metadata(doc_id, data)
        if not doc:
            raise DocumentNotFoundException()
        return doc

    def delete_document(self, doc_id: str) -> bool:
        success = self.repo.soft_delete(doc_id)
        if not success:
            raise DocumentNotFoundException()
        return True
