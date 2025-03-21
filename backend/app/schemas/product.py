from typing import Optional
from pydantic import BaseModel, Field
from . import TimestampMixin


class ProductRequest(BaseModel):
    product_name: str = Field(..., description="Name of product")
    product_id :str = Field(...,description="Unique ID of product")
    product_price: float = Field(..., description="Price of product")
    product_description: str = Field(...,description="Description of product")
    product_stock: int = Field(...,description="Available Stock of product")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_name": "example_product",
                "product_id": "101",
                "product_price": 500.00,
                "product_description": "This is the product description",
                "product_stock": 10
            }
        }

class ProductResponse(TimestampMixin, BaseModel):
    id: str = Field(..., description="Unique identifier for product")
    product_name: str = Field(..., description="Name of product")
    product_id: str = Field(..., description="Unique ID of product")
    product_price: float = Field(..., description="Price of product")
    product_description: str = Field(...,description="Description of product")
    product_stock: int = Field(...,description="Available Stock of product")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b1e8e5b2cbbf9b8",
                "product_name": "example_product",
                "product_id": "101",
                "product_price": 500.00,
                "product_description": "This is the product description",
                "product_stock": 10,
                "created_at": "2023-09-01T08:00:00",
                "updated_at": "2023-09-14T12:45:30"
            }
        }

class UpdateProduct(BaseModel):
    product_name: Optional[str] = Field(None, description="Name of product")
    product_price: Optional[float] = Field(None, description="Price of product")
    product_description: Optional[str] = Field(None, description="Description of product")
    product_stock: Optional[int] = Field(None, description="Available Stock of product")

    class Config:
        json_schema_extra = {
            "example": {
                "product_name": "example_product",
                "product_price": 500.00,
                "product_description": "This is the product description",
                "product_stock": 10,
            }
        }
