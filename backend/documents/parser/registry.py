from typing import Dict, Type, List, Optional
from documents.parser.base import DocumentParser
from documents.parser.exceptions import ParserRegistrationException

class ParserRegistry:
    """
    Registry for managing document parsers.
    """
    _parsers: Dict[str, Type[DocumentParser]] = {}

    @classmethod
    def register(cls, name: str, parser_cls: Type[DocumentParser]) -> None:
        if name in cls._parsers:
            raise ParserRegistrationException(f"Parser '{name}' is already registered.")
        if not issubclass(parser_cls, DocumentParser):
            raise ParserRegistrationException(f"Class '{parser_cls.__name__}' must inherit from DocumentParser.")
        cls._parsers[name] = parser_cls

    @classmethod
    def unregister(cls, name: str) -> None:
        if name in cls._parsers:
            del cls._parsers[name]

    @classmethod
    def get(cls, name: str) -> Optional[Type[DocumentParser]]:
        return cls._parsers.get(name)

    @classmethod
    def list(cls) -> List[str]:
        return list(cls._parsers.keys())
        
    @classmethod
    def get_all_parsers(cls) -> List[Type[DocumentParser]]:
        return list(cls._parsers.values())

# Auto-register default parsers
try:
    from documents.parser.pdf.pdf_parser import PDFParser
    ParserRegistry.register('PDFParser', PDFParser)
except ImportError:
    pass
