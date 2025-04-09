from typing import List
from fastapi import HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas import ResponseWrapper
from app.schemas.category import CategoryRequest, CategoryResponse, UpdateCategory
from app.models.category import Category
from app.models_2_schemas.category import create_category_response

router = APIRouter()

# Create Category
@router.post("/", response_model=ResponseWrapper[CategoryResponse])
async def create_category(category_req: CategoryRequest):
    try:
        category: Category = Category.objects(category_id=category_req.category_id).first()
        if category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already Exists")
        
        category: Category = Category(
            category_id = category_req.category_id,
            category_name = category_req.category_name,
            category_description = category_req.category_description
        )
        category.save()
        return ResponseWrapper(status="SUCCESS",message="Category Created Successfully",data=create_category_response(category),error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get all Categories
@router.get("/", response_model=ResponseWrapper[List[CategoryResponse]])
async def get_categories():
    try:
        categories: List[Category] = Category.objects()
        if not categories:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categories Not Found")
        
        return ResponseWrapper(status="SUCCESS", message="Categories Fetched Successfully",
                               data=[
                                   create_category_response(category)
                                   for category in categories
                               ],error=None)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Get Category by Name
@router.get("/{category_name}", response_model=ResponseWrapper[CategoryResponse])
async def get_category(category_name :str):
    try:
        category: Category = Category.objects(category_name=category_name).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
        
        return ResponseWrapper(status="SUCCESS", message="Category Fetched Successfully",data=create_category_response(category),error=None)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update Category Description
@router.put("/{id}", response_model=ResponseWrapper[CategoryResponse])
async def update_category(id: str, update_category: UpdateCategory):
    try:
        category: Category = Category.objects(id=id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category Not Found")

        category.category_description = update_category.category_description
        category.save()
        return ResponseWrapper(status="SUCCESS", message="Category Updated Successfully",data=create_category_response(category),error=None)
      
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete Category
@router.delete("/{id}",response_model=ResponseWrapper[None])
async def delete_category(id: str):
    try:
        catgeory: Category = Category.objects(id=id).first()
        if not catgeory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
        
        catgeory.delete()
        return ResponseWrapper(status="SUCCESS", message="Category Deleted Successfully", data=None, error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
