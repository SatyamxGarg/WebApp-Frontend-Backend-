from pydantic import BaseModel, Field
from . import TimestampMixin
    

class CategoryRequest(BaseModel):
    category_id: str = Field(..., description="Unique Category ID")
    category_name :str = Field(...,description="Unique Category Name")
    category_description: str = Field(..., description="Category Description")

    class Config:
        json_schema_extra = {
            "example": {
                "category_id": "furniture",
                "category_name": "Furniture",
                "category_description": "All types of furniture"
            }
        }


class CategoryResponse(TimestampMixin, BaseModel):
    id: str = Field(..., description="Unique identifier for Category")
    category_id: str = Field(..., description="Unique Category ID")
    category_name :str = Field(...,description="Unique Category Name")
    category_description: str = Field(..., description="Category Description")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b1e8e5b2cbbf9b8",
                "category_id": "furniture",
                "category_name": "Furniture",
                "category_description": "All types of furniture",
                "created_at": "2023-09-01T08:00:00",
                "updated_at": "2023-09-14T12:45:30"
            }
        }


class UpdateCategory(BaseModel):
    category_description: str = Field(..., description="Category Description")
    

class SubcategoryRequest(BaseModel):
    subcategory_id: str = Field(..., description="Unique Subcategory ID")
    subcategory_name :str = Field(...,description="Unique Subcategory Name")
    subcategory_description: str = Field(..., description="Subcategory Description")
    category: str = Field(..., description="Category Reference")

    class Config:
        json_schema_extra = {
            "example": {
                "subcategory_id": "chairs",
                "subcategory_name": "Chairs",
                "subcategory_description": "Office and Home Chairs",
                "category": "60c72b2f9b1e8e5b2cbbf9b8"
            }
        }
        

class SubcategoryResponse(TimestampMixin, BaseModel):
    id: str = Field(..., description="Unique identifier for Subcategory")
    subcategory_id: str = Field(..., description="Unique Subcategory ID")
    subcategory_name :str = Field(...,description="Unique Subcategory Name")
    subcategory_description: str = Field(..., description="Subcategory Description")
    category: CategoryResponse = Field(..., description="Category Reference")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b1e8e5b2cbbf9b8",
                "subcategory_id": "chairs",
                "subcategory_name": "Chairs",
                "subcategory_description": "Office and Home Chairs",
                "category": "category",
                "created_at": "2023-09-01T08:00:00",
                "updated_at": "2023-09-14T12:45:30"
            }
        }
        

class UpdateSubcategory(BaseModel):
    subcategory_description: str = Field(..., description="Subcategory Description")