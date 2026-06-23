from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
import uuid
from enum import Enum
from schemas.knowledge_base import PatientKnowledgeBase
from schemas.patient import Patient
from schemas.administrative import InsuranceDetails, Provider

class AuthorizationPriority(str, Enum):
    STANDARD = "STANDARD"
    URGENT = "URGENT"
    STAT = "STAT"

class AuthorizationStatus(str, Enum):
    DRAFT = "DRAFT"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    PENDING_MORE_INFO = "PENDING_MORE_INFO"

class AuthorizationRequest(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    patient: Optional[Patient] = None
    requested_procedure_code: str
    requested_procedure_name: str
    insurance: Optional[InsuranceDetails] = None
    ordering_provider: Optional[Provider] = None
    supporting_documents: List[Any] = Field(default_factory=list)
    knowledge_base: PatientKnowledgeBase
    priority: AuthorizationPriority = AuthorizationPriority.STANDARD
    created_time: datetime = Field(default_factory=datetime.utcnow)
    status: AuthorizationStatus = AuthorizationStatus.DRAFT
