from documents.constants import DocumentType
from extraction.base import MedicalExtractor
from extraction.registry import ExtractorRegistry
from extraction.exceptions import UnsupportedExtractionDocumentException

class ExtractorFactory:
    """
    Factory for selecting and instantiating the correct extractor for a document type.
    """
    
    @staticmethod
    def get_extractor_for_type(document_type: DocumentType) -> MedicalExtractor:
        """
        Iterates through registered extractors and returns the first one that supports the document type.
        """
        for extractor_cls in ExtractorRegistry.get_all_extractors():
            extractor_instance = extractor_cls()
            if extractor_instance.supports(document_type):
                return extractor_instance
                
        raise UnsupportedExtractionDocumentException(
            f"No registered extractor supports document type: {document_type}"
        )
