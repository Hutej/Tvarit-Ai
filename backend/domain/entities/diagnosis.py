from typing import Optional, List
from pydantic import BaseModel

class DiagnosisEntity(BaseModel):
    id: Optional[str] = None
