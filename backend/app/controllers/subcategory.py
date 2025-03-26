from typing import List
from fastapi import HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas import ResponseWrapper
from app.schemas.category import CategoryResponse, SubcategoryRequest, SubcategoryResponse
from app.models.category import Category
from app.models.subcategory import Subcategory

router = APIRouter()

# Create Subcategory
@router.post("/", response_model=ResponseWrapper[SubcategoryResponse])
async def create_subcatgeory(subcategory_req: SubcategoryRequest):
    try:
        subcategory: Subcategory = Subcategory.objects(subcategory_id=subcategory_req.subcategory_id).first()
        if subcategory:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subcategory Already Exists")
        
        category: Category = Category.objects(id=subcategory_req.category).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category Not Found")
        
        subcategory: Subcategory = Subcategory(
            subcategory_id = subcategory_req.subcategory_id,
            subcategory_name = subcategory_req.subcategory_name,
            subcategory_description = subcategory_req.subcategory_description,
            category = subcategory_req.category
        )
        subcategory.save()
        return ResponseWrapper(status="SUCCESS", message="Subcategory Created Successfully",
                               data=SubcategoryResponse(
                                   id = str(subcategory.id),
                                   subcategory_id= subcategory.subcategory_id,
                                   subcategory_name = subcategory.subcategory_name,
                                   subcategory_description = subcategory.subcategory_description,
                                   category = CategoryResponse(
                                       id = str(subcategory.category.id),
                                       category_id = subcategory.category.category_id,
                                       category_name = subcategory.category.category_name,
                                       category_description = subcategory.category.category_description,
                                       created_at = subcategory.category.created_at,
                                       updated_at = subcategory.category.updated_at
                                       ),
                                   created_at = subcategory.created_at,
                                   updated_at = subcategory.updated_at                                   
                               ),error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get All Subcategories from Category
@router.get("/{id}", response_model=ResponseWrapper[list[SubcategoryResponse]])
async def get_subcategory(id: str):
    try:
        category: Category = Category.objects(id=id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
        
        subcategories : Subcategory = Subcategory.objects(category=category)
        if not subcategories:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are No Subcategories for this Category")
        
        return ResponseWrapper(status="SUCCESS",message="Subcategories Fetched Successfully",
                               data=(SubcategoryResponse(
                                   id = str(subcategory.id),
                                   subcategory_id= subcategory.subcategory_id,
                                   subcategory_name = subcategory.subcategory_name,
                                   subcategory_description = subcategory.subcategory_description,
                                   category = CategoryResponse(
                                       id = str(subcategory.category.id),
                                       category_id = subcategory.category.category_id,
                                       category_name = subcategory.category.category_name,
                                       category_description = subcategory.category.category_description,
                                       created_at = subcategory.category.created_at,
                                       updated_at = subcategory.category.updated_at
                                       ),
                                   created_at = subcategory.created_at,
                                   updated_at = subcategory.updated_at
                                ) for subcategory in subcategories), error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))