from typing import Optional, List
from pydantic import BaseModel

class ProcedureEntity(BaseModel):
    id: Optional[str] = None
