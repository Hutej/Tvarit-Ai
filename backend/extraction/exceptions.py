from core.exceptions import TvaritException

class ExtractionException(TvaritException):
    """Base exception for extraction operations."""
    pass

class ExtractorRegistrationException(ExtractionException):
    def __init__(self, message: str = "Error registering extractor"):
        super().__init__(message, code="EXTRACTOR_REGISTRATION_ERROR", status_code=500)

class UnsupportedExtractionDocumentException(ExtractionException):
    def __init__(self, message: str = "Document type is not supported by any registered extractor"):
        super().__init__(message, code="UNSUPPORTED_EXTRACTION_DOCUMENT", status_code=400)

class ProviderCommunicationException(ExtractionException):
    def __init__(self, message: str = "Failed to communicate with AI provider"):
        super().__init__(message, code="PROVIDER_COMMUNICATION_ERROR", status_code=502)

class ExtractionValidationException(ExtractionException):
    def __init__(self, message: str = "Extracted data failed validation"):
        super().__init__(message, code="EXTRACTION_VALIDATION_ERROR", status_code=422)
