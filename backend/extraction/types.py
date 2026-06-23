from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from schemas.knowledge_base import PatientKnowledgeBase
from documents.parser.types import ParserResult

class ExtractionStatistics(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    processing_time_ms: int = 0

class ExtractionWarning(BaseModel):
    code: str
    message: str

class ExtractionRequest(BaseModel):
    parser_result: ParserResult
    document_type_hint: Optional[str] = None
    custom_instructions: Optional[str] = None

class ExtractionResult(BaseModel):
    knowledge_base: PatientKnowledgeBase
    statistics: ExtractionStatistics = Field(default_factory=ExtractionStatistics)
    warnings: List[ExtractionWarning] = Field(default_factory=list)
