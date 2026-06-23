from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
import uuid
from schemas.enums import ConfidenceLevel

class Confidence(BaseModel):
    level: ConfidenceLevel = Field(default=ConfidenceLevel.HIGH)
    score: float = Field(default=1.0, ge=0.0, le=1.0)
    reasoning: Optional[str] = None

class Provenance(BaseModel):
    source_document_id: str
    document_name: str
    page: Optional[int] = None
    bounding_box: Optional[List[float]] = None
    paragraph: Optional[str] = None
    extraction_model: str
    confidence: Confidence
    created_time: datetime = Field(default_factory=datetime.utcnow)
    updated_time: datetime = Field(default_factory=datetime.utcnow)

class Metadata(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = Field(default=1)
    tags: List[str] = Field(default_factory=list)
    custom_attributes: Dict[str, Any] = Field(default_factory=dict)

class Audit(BaseModel):
    created_by: str = Field(default="system")
    updated_by: str = Field(default="system")
    audit_log: List[str] = Field(default_factory=list)

class EntityBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provenance: List[Provenance] = Field(default_factory=list)
    metadata: Metadata = Field(default_factory=Metadata)
    audit: Audit = Field(default_factory=Audit)
