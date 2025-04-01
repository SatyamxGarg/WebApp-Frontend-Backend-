from pydantic import BaseModel, Field, EmailStr
from app.schemas.product import ProductResponse
from app.schemas.order import UserResponse
from . import TimestampMixin


class CartRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    id :str = Field(...,description="Unique ID of product")
    quantity: int = Field(..., description="Quantity of product")
    
    
class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "product_id": "60c72b2f9b1e8e5b2cbbf9b8",
                "quantity": 10
            }
        }
        

class CartResponse(TimestampMixin, BaseModel):
    id: str = Field(..., description="Unique identifier for cart")
    user: UserResponse = Field(..., description="User's Reference")
    product: ProductResponse = Field(...,description="Product Reference")
    quantity: int = Field(..., description="Quantity of product")
    
    
class Config:
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b1e8e5b2cbbf9b8",
                "user": "user@example.com",
                "product": "60c72b1r9b1e8e5b2cbbf9b8",
                "quantity": 10,
                "created_at": "2023-09-01T08:00:00",
                "updated_at": "2023-09-14T12:45:30"
            }
        }
    
    
class CartUpdate(BaseModel):
    quantity: int = Field(..., description="Quantity of product")

    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 10,
            }
        }
