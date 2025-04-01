from pydantic import BaseModel, Field
from app.schemas.order import UserResponse
from app.schemas.product import ProductResponse
from . import TimestampMixin


class WishlistResponse(TimestampMixin, BaseModel):
    id: str = Field(..., description="Unique identifier for Wishlist")
    user : UserResponse = Field(..., description="Users' Reference")
    products: list[ProductResponse] = Field(..., description="List of Product's Response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b1e8e5b2cbbf9b8",
                "user": "user@example.com",
                "products": "60c72b2f9b1e8e5b2cbbf9b8",
                "created_at": "2023-09-01T08:00:00",
                "updated_at": "2023-09-14T12:45:30"
            }
        }
