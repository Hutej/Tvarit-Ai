from documents.models import Document
from documents.parser.base import DocumentParser
from documents.parser.registry import ParserRegistry
from documents.parser.exceptions import UnsupportedDocumentException

class ParserFactory:
    """
    Factory for selecting and instantiating the correct parser for a document.
    """
    
    @staticmethod
    def get_parser_for_document(document: Document) -> DocumentParser:
        """
        Iterates through registered parsers and returns the first one that supports the document.
        Instantiates and returns the parser object.
        """
        for parser_cls in ParserRegistry.get_all_parsers():
            parser_instance = parser_cls()
            if parser_instance.supports(document):
                return parser_instance
                
        raise UnsupportedDocumentException(
            f"No registered parser supports document: {document.original_filename} (MIME: {document.mime_type})"
        )
