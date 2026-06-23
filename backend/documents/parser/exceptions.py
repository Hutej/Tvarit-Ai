from core.exceptions import TvaritException

class ParserException(TvaritException):
    """Base exception for parser errors."""
    pass

class UnsupportedDocumentException(ParserException):
    def __init__(self, message: str = "Document type or format is not supported by any registered parser"):
        super().__init__(message, code="UNSUPPORTED_DOCUMENT", status_code=400)

class ParsingFailedException(ParserException):
    def __init__(self, message: str = "Failed to parse the document"):
        super().__init__(message, code="PARSING_FAILED", status_code=500)

class ParserRegistrationException(ParserException):
    def __init__(self, message: str = "Error registering parser"):
        super().__init__(message, code="PARSER_REGISTRATION_ERROR", status_code=500)
