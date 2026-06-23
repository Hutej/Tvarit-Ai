from typing import Optional, List
from pydantic import BaseModel

class InsuranceEntity(BaseModel):
    id: Optional[str] = None
