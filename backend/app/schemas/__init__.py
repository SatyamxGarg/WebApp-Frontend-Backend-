from datetime import datetime
import uuid
from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Literal, Any, Optional

T = TypeVar('T')

class ResponseWrapper(BaseModel, Generic[T]):
    status: Literal['ERROR', 'WARN', 'SUCCESS'] = Field(..., description="Status of the response")
    message: str = Field(..., description="Descriptive message about the response")
    data: Optional[T] = Field(None, description="Response payload containing requested data")
    error: Optional[Any] = Field(None, description="Error details if the status is 'ERROR'")
    execution_id: str = Field(default_factory=lambda: uuid.uuid4().hex, description="Unique ID for tracking the execution")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "SUCCESS",
                "message": "Request processed successfully",
                "data": {"example_field": "example_value"},  # Replace with relevant example data for T
                "error": None,
                "execution_id": "9f1b6e5d8a7c4b6f8d93e2a1f3a1a9e7"
            }
        }

class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None