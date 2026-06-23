import os
from typing import Tuple
from extraction.base import MedicalExtractor
from documents.constants import DocumentType
from documents.parser.types import ParserResult
from schemas.knowledge_base import PatientKnowledgeBase
from agents.prompts.loader import PromptLoader
from agents.prompts.builder import PromptBuilder

class GenericMedicalExtractor(MedicalExtractor):
    """
    Generic extraction model capable of extracting structured medical information
    from ANY parsed medical document.
    """
    def __init__(self):
        super().__init__()
        self.prompt_loader = PromptLoader()

    def supports(self, document_type: DocumentType) -> bool:
        # Supports everything as a fallback extractor
        return True

    def build_prompt(self, parser_result: ParserResult) -> Tuple[str, str]:
        # Load the prompt template from agents/prompts/generic/
        template = self.prompt_loader.load_template(category="generic", template_name="default")
        template.output_schema = PatientKnowledgeBase
        
        # Determine document type hint
        doc_type_hint = parser_result.metadata.document_type_hint or "UNKNOWN"
        doc_type = DocumentType(doc_type_hint) if doc_type_hint in [dt.value for dt in DocumentType] else DocumentType.UNKNOWN
        
        # Build prompt package
        prompt_package = PromptBuilder.build(
            template=template,
            parser_result=parser_result,
            document_type=doc_type
        )
        
        return prompt_package.system_prompt, prompt_package.user_prompt

    def validate(self, output: PatientKnowledgeBase) -> bool:
        # Pydantic v2 automatically validates during instantiation inside AIClient
        if not isinstance(output, PatientKnowledgeBase):
            return False
        return True
