from typing import Dict, Type, List, Optional
from extraction.base import MedicalExtractor
from documents.constants import DocumentType
from extraction.exceptions import ExtractorRegistrationException

class ExtractorRegistry:
    """
    Registry for managing specialized document extractors.
    """
    _extractors: Dict[str, Type[MedicalExtractor]] = {}

    @classmethod
    def register(cls, name: str, extractor_cls: Type[MedicalExtractor]) -> None:
        if name in cls._extractors:
            raise ExtractorRegistrationException(f"Extractor '{name}' is already registered.")
        if not issubclass(extractor_cls, MedicalExtractor):
            raise ExtractorRegistrationException(f"Class '{extractor_cls.__name__}' must inherit from MedicalExtractor.")
        cls._extractors[name] = extractor_cls

    @classmethod
    def unregister(cls, name: str) -> None:
        if name in cls._extractors:
            del cls._extractors[name]

    @classmethod
    def get(cls, name: str) -> Optional[Type[MedicalExtractor]]:
        return cls._extractors.get(name)

    @classmethod
    def list(cls) -> List[str]:
        return list(cls._extractors.keys())
        
    @classmethod
    def get_all_extractors(cls) -> List[Type[MedicalExtractor]]:
        return list(cls._extractors.values())

# Auto-register default extractors
try:
    from extraction.extractors.generic_extractor import GenericMedicalExtractor
    ExtractorRegistry.register('GenericMedicalExtractor', GenericMedicalExtractor)
except ImportError:
    pass
