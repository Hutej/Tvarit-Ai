from typing import TypeVar, Generic, Type
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class StructuredOutputGenerator(Generic[T]):
    def __init__(self, schema: Type[T]):
        self.schema = schema
