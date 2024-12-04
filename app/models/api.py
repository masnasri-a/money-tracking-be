from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')

class APIResponse(GenericModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None

class ErrorResponse(BaseModel):
    detail: str

