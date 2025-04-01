from typing import List
from fastapi import HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas import ResponseWrapper
from app.schemas.category import SubcategoryRequest, SubcategoryResponse, UpdateSubcategory
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.utils.models_2_schemas.subcategory import create_subcategory_response

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
        return ResponseWrapper(status="SUCCESS", message="Subcategory Created Successfully", data=create_subcategory_response(subcategory),error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get All Subcategories from Category
@router.get("/{id}", response_model=ResponseWrapper[list[SubcategoryResponse]])
async def get_subcategories(id: str):
    try:
        category: Category = Category.objects(id=id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category Not Found")
        
        subcategories : List[Subcategory] = Subcategory.objects(category=category)
        if not subcategories:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are No Subcategories for this Category")
        
        return ResponseWrapper(status="SUCCESS",message="Subcategories Fetched Successfully",
                               data=[create_subcategory_response(subcategory)
                                     for subcategory in subcategories],
                               error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Get Subcategory by Name
@router.get("/name/{subcategory_name}", response_model=ResponseWrapper[SubcategoryResponse])
async def get_subcategory(subcategory_name: str):
    try:
        subcategory: Subcategory = Subcategory.objects(subcategory_name=subcategory_name).first()
        if not subcategory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory Not Found")
        
        return ResponseWrapper(status="SUCCESS", message="Subcategory Fetched Successfully",data=create_subcategory_response(subcategory),error=None)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Update Subcategory Description
@router.put("/{id}", response_model=ResponseWrapper[SubcategoryResponse])
async def update_subcatgeory(id: str, update_subcategory: UpdateSubcategory):
    try:
        subcategory: Subcategory = Subcategory.objects(id=id).first()
        if not subcategory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory Not Found")
        
        subcategory.subcategory_description = update_subcategory.subcategory_description
        subcategory.save()
        return ResponseWrapper(status="SUCCESS", message="Subcategory Updated Successfully", data=create_subcategory_response(subcategory), error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete Subcategory
@router.delete("/{id}", response_model=ResponseWrapper[None])
async def delete_subcategory(id: str):
    try:
        subcategory: Subcategory = Subcategory.objects(id=id).first()
        if not subcategory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory Not Found")
        
        subcategory.delete()
        return ResponseWrapper(status="SUCCESS", message="Subcategory Deleted Successfully", data=None, error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
