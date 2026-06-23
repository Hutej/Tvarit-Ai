from core.exceptions import TvaritException

class DocumentException(TvaritException):
    """Base exception for document operations."""
    pass

class InvalidExtensionException(DocumentException):
    def __init__(self, message: str = "Invalid file extension"):
        super().__init__(message, code="INVALID_EXTENSION", status_code=400)

class InvalidMimeTypeException(DocumentException):
    def __init__(self, message: str = "Invalid MIME type"):
        super().__init__(message, code="INVALID_MIME_TYPE", status_code=400)

class FileTooLargeException(DocumentException):
    def __init__(self, message: str = "File exceeds maximum allowed size"):
        super().__init__(message, code="FILE_TOO_LARGE", status_code=400)

class DuplicateDocumentException(DocumentException):
    def __init__(self, message: str = "Document with this checksum already exists"):
        super().__init__(message, code="DUPLICATE_DOCUMENT", status_code=409)

class DocumentNotFoundException(DocumentException):
    def __init__(self, message: str = "Document not found"):
        super().__init__(message, code="DOCUMENT_NOT_FOUND", status_code=404)

class StorageException(DocumentException):
    def __init__(self, message: str = "Failed to store document"):
        super().__init__(message, code="STORAGE_ERROR", status_code=500)
