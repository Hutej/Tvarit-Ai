from pydantic import BaseModel, Field
from typing import Dict, Any, Type, Optional, List

class PromptMetadata(BaseModel):
    version: str = "1.0"
    author: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class PromptVariable(BaseModel):
    name: str
    description: Optional[str] = None
    is_required: bool = True
    default_value: Optional[str] = None

class PromptContext(BaseModel):
    document_type: str
    variables: Dict[str, Any] = Field(default_factory=dict)
    raw_text: Optional[str] = None

class PromptPackage(BaseModel):
    system_prompt: str
    user_prompt: str
    response_schema: Optional[Type[BaseModel]] = None
    metadata: PromptMetadata = Field(default_factory=PromptMetadata)
