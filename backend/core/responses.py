from ninja import Schema
from typing import Generic, TypeVar, Optional, Any
from pydantic import Field

T = TypeVar('T')

class SuccessResponse(Schema, Generic[T]):
    message: str = "Success"
    data: Optional[T] = None

class ErrorResponse(Schema):
    error: str
    details: Optional[Any] = None
