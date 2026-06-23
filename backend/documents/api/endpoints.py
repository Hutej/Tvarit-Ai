from ninja_extra import api_controller, route
from ninja import UploadedFile, File, Query
from django.http import HttpResponse, FileResponse
from typing import List, Optional
import os

from core.responses import SuccessResponse, ErrorResponse
from documents.services.document_service import DocumentService
from documents.exceptions import DocumentException, DocumentNotFoundException
from documents.api.schemas import (
    UploadResponse,
    UploadMultipleResponse,
    DocumentDetails,
    UpdateDocumentRequest,
    DeleteResponse,
    ListDocumentsResponse,
    PaginationMeta
)

@api_controller('/documents', tags=['Documents'])
class DocumentController:
    
    def __init__(self):
        self.service = DocumentService()

    @route.post('/upload', response={200: UploadResponse, 400: ErrorResponse, 409: ErrorResponse, 500: ErrorResponse})
    def upload_document(self, file: UploadedFile = File(...)):
        """Upload a single medical document."""
        try:
            content = file.read()
            doc = self.service.process_upload(content, file.name, file.content_type)
            return 200, {"message": "Document uploaded successfully", "document": doc}
        except DocumentException as e:
            return e.status_code, {"error": e.code, "details": e.message}

    @route.post('/upload-multiple', response={200: UploadMultipleResponse, 400: ErrorResponse, 500: ErrorResponse})
    def upload_multiple_documents(self, files: List[UploadedFile] = File(...)):
        """Upload multiple medical documents."""
        try:
            file_data = [(f.read(), f.name, f.content_type) for f in files]
            docs = self.service.process_multiple_uploads(file_data)
            return 200, {"message": f"{len(docs)} documents uploaded successfully", "documents": docs}
        except DocumentException as e:
            return e.status_code, {"error": e.code, "details": e.message}

    @route.get('', response=ListDocumentsResponse)
    def list_documents(
        self,
        page: int = 1,
        limit: int = 20,
        filename: Optional[str] = None,
        status: Optional[str] = None,
        document_type: Optional[str] = None
    ):
        """List documents with pagination and filtering."""
        filters = {
            "filename": filename,
            "status": status,
            "document_type": document_type
        }
        docs, total = self.service.list_documents(page=page, limit=limit, filters=filters)
        return {
            "data": docs,
            "meta": PaginationMeta(total=total, page=page, limit=limit)
        }

    @route.get('/{id}', response={200: DocumentDetails, 404: ErrorResponse})
    def retrieve_document(self, id: str):
        """Retrieve full details of a specific document."""
        try:
            doc = self.service.get_document(id)
            return 200, doc
        except DocumentNotFoundException as e:
            return 404, {"error": e.code, "details": e.message}

    @route.patch('/{id}', response={200: DocumentDetails, 404: ErrorResponse})
    def update_document(self, id: str, payload: UpdateDocumentRequest):
        """Update metadata of a specific document."""
        try:
            doc = self.service.update_document_metadata(id, payload.dict(exclude_unset=True))
            return 200, doc
        except DocumentNotFoundException as e:
            return 404, {"error": e.code, "details": e.message}

    @route.delete('/{id}', response={200: DeleteResponse, 404: ErrorResponse})
    def delete_document(self, id: str):
        """Soft delete a specific document."""
        try:
            self.service.delete_document(id)
            return 200, {"message": "Document deleted successfully", "id": id}
        except DocumentNotFoundException as e:
            return 404, {"error": e.code, "details": e.message}

    @route.get('/download/{id}')
    def download_document(self, id: str):
        """Download the physical document file."""
        try:
            doc = self.service.get_document(id)
            if not os.path.exists(doc.storage_path):
                return HttpResponse(status=404, content="Physical file not found on disk")
            
            response = FileResponse(open(doc.storage_path, 'rb'), content_type=doc.mime_type)
            response['Content-Disposition'] = f'attachment; filename="{doc.original_filename}"'
            return response
        except DocumentNotFoundException:
            return HttpResponse(status=404, content="Document not found")

