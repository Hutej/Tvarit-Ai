from abc import ABC, abstractmethod
from documents.models import Document
from documents.parser.types import ParserResult, DocumentMetadata

class DocumentParser(ABC):
    """
    Abstract base class for all document parsers.
    """
    
    @abstractmethod
    def supports(self, document: Document) -> bool:
        """
        Check if this parser can handle the given document.
        """
        pass

    @abstractmethod
    def parse(self, document: Document) -> ParserResult:
        """
        Parse the document and return a structured ParserResult.
        """
        pass

    @abstractmethod
    def validate(self, document: Document) -> bool:
        """
        Validate if the document is intact and readable by this parser.
        """
        pass

    @abstractmethod
    def get_metadata(self, document: Document) -> DocumentMetadata:
        """
        Extract only metadata from the document without full parsing.
        """
        pass
