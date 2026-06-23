from typing import Optional, List
from pydantic import BaseModel

class AuthorizationEntity(BaseModel):
    id: Optional[str] = None
