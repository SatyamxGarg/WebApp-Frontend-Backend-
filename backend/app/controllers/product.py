from typing import List
from fastapi import HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas.product import ProductRequest, ProductResponse, UpdateProduct
from app.schemas import ResponseWrapper
from app.models.product import Product
from app.models.subcategory import Subcategory
from app.schemas.category import CategoryResponse, SubcategoryResponse

router = APIRouter()

# Add Product
@router.post("/",response_model=ResponseWrapper[ProductResponse])
async def add_product(product: ProductRequest):
    try:
        existing_product: Product = Product.objects(product_id=product.product_id).first()
        if existing_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID already exists")
        
        subcategory: Subcategory = Subcategory.objects(id=product.subcategory).first()
        if not subcategory:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subcategory not Found")
            
        product: Product = Product(
            product_name = product.product_name,
            product_id = product.product_id,
            product_description = product.product_description,
            product_price = product.product_price,
            product_stock = product.product_stock,
            subcategory = product.subcategory
        )
        product.save()
        return ResponseWrapper(status="SUCCESS",message="Product Added Successfully",
        data=ProductResponse(
            id=str(product.id),
            product_name=product.product_name,
            product_id=product.product_id,
            product_description = product.product_description,
            product_price=product.product_price,
            product_stock = product.product_stock,
            product_rating = product.product_rating,
            subcategory = SubcategoryResponse(
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
            ),
            created_at=product.created_at,
            updated_at=product.updated_at
        ),error=None)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get all Products
@router.get("/",response_model=ResponseWrapper[List[ProductResponse]])
async def get_products():
    try:
        products: Product = Product.objects()
        product_list = [
            ProductResponse(
            id=str(product.id),
            product_name=product.product_name,
            product_id=product.product_id,
            product_description = product.product_description,
            product_price=product.product_price,
            product_stock = product.product_stock,
            product_rating = product.product_rating,
            subcategory = SubcategoryResponse(
                id = str(product.subcategory.id),
                subcategory_id= product.subcategory.subcategory_id,
                subcategory_name = product.subcategory.subcategory_name,
                subcategory_description = product.subcategory.subcategory_description,
                category = CategoryResponse(
                    id = str(product.subcategory.category.id),
                    category_id = product.subcategory.category.category_id,
                    category_name = product.subcategory.category.category_name,
                    category_description = product.subcategory.category.category_description,
                    created_at = product.subcategory.category.created_at,
                    updated_at = product.subcategory.category.updated_at
                ),
                created_at = product.subcategory.created_at,
                updated_at = product.subcategory.updated_at 
            ),
            created_at=product.created_at,
            updated_at=product.updated_at
            )
            for product in products
        ]
        return ResponseWrapper(status="SUCCESS",message="Products Fetched Successfully!",data=product_list,error=None)
    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurs while fetching products")
    

# Get Product by ID
@router.get("/{id}",response_model=ResponseWrapper[ProductResponse])
async def get_product(id: str):
    try:
        product: Product = Product.objects(id=id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this ID not exists!")
        
        return ResponseWrapper(status="SUCCESS",message="Product Fetched Successfully!",
        data=ProductResponse(
            id=str(product.id),
            product_name=product.product_name,
            product_id=product.product_id,
            product_description = product.product_description,
            product_price=product.product_price,
            product_stock = product.product_stock,
            product_rating = product.product_rating,
            subcategory = SubcategoryResponse(
                id = str(product.subcategory.id),
                subcategory_id= product.subcategory.subcategory_id,
                subcategory_name = product.subcategory.subcategory_name,
                subcategory_description = product.subcategory.subcategory_description,
                category = CategoryResponse(
                    id = str(product.subcategory.category.id),
                    category_id = product.subcategory.category.category_id,
                    category_name = product.subcategory.category.category_name,
                    category_description = product.subcategory.category.category_description,
                    created_at = product.subcategory.category.created_at,
                    updated_at = product.subcategory.category.updated_at
                ),
                created_at = product.subcategory.created_at,
                updated_at = product.subcategory.updated_at 
            ),
            created_at=product.created_at,
            updated_at=product.updated_at
        ),error=None)      
   
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update Product by ID
@router.put("/{id}",response_model=ResponseWrapper[ProductResponse])
async def update_product(id: str, product_req: UpdateProduct):
    try:
        product: Product = Product.objects(id=id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with this ID not exists!")
        
        if product_req.product_name:
            product.product_name = product_req.product_name
        
        if product_req.product_price:
            product.product_price = product_req.product_price
            
        if product_req.product_description:
            product.product_description = product_req.product_description
        
        if product_req.product_stock:
            product.product_stock = product_req.product_stock
        
        product.save()
        
        return ResponseWrapper(status="SUCCESS",message="Product Updated Successfully!",
        data=ProductResponse(
            id=str(product.id),
            product_name=product.product_name,
            product_id=product.product_id,
            product_description = product.product_description,
            product_price=product.product_price,
            product_stock = product.product_stock,
            product_rating = product.product_rating,
            subcategory = SubcategoryResponse(
                id = str(product.subcategory.id),
                subcategory_id= product.subcategory.subcategory_id,
                subcategory_name = product.subcategory.subcategory_name,
                subcategory_description = product.subcategory.subcategory_description,
                category = CategoryResponse(
                    id = str(product.subcategory.category.id),
                    category_id = product.subcategory.category.category_id,
                    category_name = product.subcategory.category.category_name,
                    category_description = product.subcategory.category.category_description,
                    created_at = product.subcategory.category.created_at,
                    updated_at = product.subcategory.category.updated_at
                ),
                created_at = product.subcategory.created_at,
                updated_at = product.subcategory.updated_at 
            ),
            created_at=product.created_at,
            updated_at=product.updated_at
        ),error=None)      
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Delete Product
@router.delete("/{id}",response_model=ResponseWrapper[None])
async def delete_product(id: str):
    try:
        product: Product = Product.objects(id=id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        product.delete()
        
        return ResponseWrapper(status="SUCCESS",message="Product Deleted Successfully",data=None,error=None)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))