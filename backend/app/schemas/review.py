from pydantic import BaseModel, Field
from . import TimestampMixin


class ReviewRequest(BaseModel):
    rating: int = Field(..., description="Rating of Product")
    review_text : str = Field(None, description="Review of Product")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rating": 5,
                "review_text": "This is Product Review",
            }
        }

class ReviewResponse(TimestampMixin,BaseModel):
    id: str = Field(..., description="Unique identifier for Review")
    rating: int = Field(..., description="Rating of Product")
    review_text : str = Field(None, description="Review of Product")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b1e8e5b2cbbf9b8",
                "rating": 5,
                "review_text": "This is Product Review",
                "created_at": "2023-09-01T08:00:00",
                "updated_at": "2023-09-14T12:45:30"
            }
        }
