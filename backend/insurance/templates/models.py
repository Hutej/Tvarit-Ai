from pydantic import BaseModel, Field
from typing import List, Optional

class ProcedureTemplate(BaseModel):
    procedure_code: str
    procedure_name: str
    aliases: List[str] = Field(default_factory=list)
    
    required_diagnoses: List[str] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    required_clinical_findings: List[str] = Field(default_factory=list)
    required_lab_results: List[str] = Field(default_factory=list)
    required_imaging: List[str] = Field(default_factory=list)
    required_medications: List[str] = Field(default_factory=list)
    required_conservative_treatment: List[str] = Field(default_factory=list)
    required_provider_types: List[str] = Field(default_factory=list)
    
    minimum_age: Optional[int] = None
    maximum_age: Optional[int] = None
    gender_restrictions: Optional[str] = None
    required_duration_months: Optional[int] = None
    custom_notes: Optional[str] = None
    priority: int = 1
