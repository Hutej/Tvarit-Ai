from ninja_extra import api_controller, route
from core.responses import ErrorResponse
from extraction.services.extraction_service import ExtractionService
from extraction.types import ExtractionResult
from extraction.exceptions import (
    ExtractionException, 
    UnsupportedExtractionDocumentException, 
    ProviderCommunicationException, 
    ExtractionValidationException
)
from documents.exceptions import DocumentNotFoundException
from documents.parser.exceptions import ParserException

@api_controller('/extraction', tags=['Extraction'])
class ExtractionController:
    
    def __init__(self):
        self.service = ExtractionService()

    @route.post('/{document_id}', response={200: ExtractionResult, 404: ErrorResponse, 400: ErrorResponse, 422: ErrorResponse, 502: ErrorResponse, 500: ErrorResponse})
    def extract_document(self, document_id: str):
        """
        Run end-to-end extraction pipeline on a document.
        """
        try:
            result = self.service.extract_document(document_id)
            return 200, result
        except DocumentNotFoundException as e:
            return 404, {"error": e.code, "details": e.message}
        except UnsupportedExtractionDocumentException as e:
            return 400, {"error": e.code, "details": e.message}
        except ExtractionValidationException as e:
            return 422, {"error": e.code, "details": e.message}
        except ProviderCommunicationException as e:
            return 502, {"error": e.code, "details": e.message}
        except ParserException as e:
            return 400, {"error": e.code, "details": e.message}
        except ExtractionException as e:
            return 500, {"error": e.code, "details": e.message}
        except Exception as e:
            return 500, {"error": "INTERNAL_SERVER_ERROR", "details": str(e)}
