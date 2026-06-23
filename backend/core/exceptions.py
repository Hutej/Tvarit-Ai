class TvaritException(Exception):
    """Base exception for all custom Tvarit AI exceptions."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)

class ResourceNotFoundException(TvaritException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="NOT_FOUND", status_code=404)

class ValidationException(TvaritException):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, code="VALIDATION_ERROR", status_code=400)

class AIProcessingException(TvaritException):
    def __init__(self, message: str = "AI processing failed"):
        super().__init__(message, code="AI_ERROR", status_code=502)
