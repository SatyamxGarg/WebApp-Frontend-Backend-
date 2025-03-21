from typing import List, TypeVar
from pydantic import BaseModel, Field, EmailStr
from app.models.order import OrderStatus, PaymentStatus
from app.schemas.product import ProductResponse
from . import TimestampMixin
T = TypeVar('T')


# class OrderRequest(BaseModel):
#     email: EmailStr = Field(..., description="User's email address")
#     product_id :str = Field(...,description="Unique ID of product")
#     quantity: int = Field(..., description="Quantity of product")
    

class UserResponse(BaseModel):
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User Email")


class OrderResponse(TimestampMixin, BaseModel):
    id: str = Field(..., description="Unique identifier for order")
    user: UserResponse = Field(..., description="User's reference")
    product :List[ProductResponse] = Field(...,description="Product's reference")
    total_price: float = Field(..., description="Total Price of Order")
    status: OrderStatus = Field(..., description="Status of order")
    payment_status: PaymentStatus = Field(...,description="Status of payment")
    
    
class Config:
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b1e8e5b2cbbf9b8",
                "user": "user@example.com",
                "product": "101",
                "total_price": 1000.00,
                "status":"Pending",
                "payment_status":"Pending",
                "created_at": "2023-09-01T08:00:00",
                "updated_at": "2023-09-14T12:45:30"
            }
        }
