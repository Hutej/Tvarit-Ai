from typing import Optional, List, Any
from core.repositories import BaseRepository
from documents.models import Document
from django.utils import timezone

class DocumentRepository(BaseRepository[Document]):
    """
    Repository for handling Document model database operations.
    Strictly DB logic. No validation.
    """
    model = Document

    def get_by_checksum(self, checksum: str) -> Optional[Document]:
        return self.model.objects.filter(sha256_checksum=checksum, is_deleted=False).first()

    def get_active_by_id(self, doc_id: str) -> Optional[Document]:
        return self.model.objects.filter(id=doc_id, is_deleted=False).first()

    def list_active(self, offset: int = 0, limit: int = 100, **filters) -> tuple[List[Document], int]:
        queryset = self.model.objects.filter(is_deleted=False)
        
        # Apply filters
        if 'filename' in filters and filters['filename']:
            queryset = queryset.filter(original_filename__icontains=filters['filename'])
        if 'status' in filters and filters['status']:
            queryset = queryset.filter(status=filters['status'])
        if 'document_type' in filters and filters['document_type']:
            queryset = queryset.filter(document_type=filters['document_type'])
            
        total_count = queryset.count()
        return list(queryset[offset:offset+limit]), total_count

    def soft_delete(self, doc_id: str) -> bool:
        doc = self.get_active_by_id(doc_id)
        if doc:
            doc.is_deleted = True
            doc.deleted_at = timezone.now()
            doc.save()
            return True
        return False
        
    def update_metadata(self, doc_id: str, update_data: dict) -> Optional[Document]:
        doc = self.get_active_by_id(doc_id)
        if doc:
            for key, value in update_data.items():
                if hasattr(doc, key):
                    setattr(doc, key, value)
            doc.save()
            return doc
        return None
