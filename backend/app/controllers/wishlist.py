from fastapi import Depends, HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas import ResponseWrapper
from app.models.user import User
from app.dependencies.get_user import get_current_user
from app.models.product import Product
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistResponse
from app.schemas.order import UserResponse
from app.schemas.product import OrderProductResponse

router = APIRouter()


# Add Product to Wishlist
@router.post("/{id}", response_model=ResponseWrapper[WishlistResponse])
async def add_to_wishlist(id: str, user: User = Depends(get_current_user)):
    try:
        product: Product = Product.objects(id=id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not Found")
        
        wishlist: Wishlist = Wishlist.objects(user=user).first()
        
        if not wishlist:
            wishlist : Wishlist = Wishlist(
                user = user,
                products = [product]
            )
            wishlist.save()
            return ResponseWrapper(status="SUCCESS", message="Item added to Wishlist",
                                   data = WishlistResponse(
                                       id = str(wishlist.id),
                                       user = UserResponse(id=str(user.id), email=user.email),
                                       products = [OrderProductResponse(
                                           id = str(product.id),
                                           product_name = product.product_name,
                                           product_id = product.product_id,
                                           product_description = product.product_description,
                                           product_price = product.product_price,
                                           created_at = product.created_at,
                                           updated_at = product.updated_at
                                        )],
                                        created_at = wishlist.created_at,
                                        updated_at = wishlist.updated_at                                       
                                       ), error=None)

        if product in wishlist.products:
            raise HTTPException(status_code=400, detail="Product already in wishlist")
        
        wishlist.products.append(product)
        wishlist.save()
        return ResponseWrapper(status="SUCCESS", message="Item added to Wishlist Successfully",
                               data = WishlistResponse(
                                   id = str(wishlist.id),
                                   user = UserResponse(id=str(user.id), email=user.email),
                                   products = [
                                       OrderProductResponse(
                                           id=str(product.id),
                                           product_name=product.product_name,
                                           product_id=product.product_id,
                                           product_description=product.product_description,
                                           product_price=product.product_price,
                                           created_at=product.created_at,
                                           updated_at=product.updated_at
                                        )
                                        for product in wishlist.products
                                    ],
                                   created_at = wishlist.created_at,
                                   updated_at = wishlist.updated_at                                   
                                ),error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Get Users's Wishlist 
@router.get("/",response_model=ResponseWrapper[WishlistResponse])
async def get_wishlist_items(user: User = Depends(get_current_user)):
    try:
        wishlist: Wishlist = Wishlist.objects(user=user).first()
        if not wishlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist Not Exists")
        
        return ResponseWrapper(status="SUCCESS",message="Wishlist Fetched Successfully",
                               data= WishlistResponse(
                                   id = str(wishlist.id),
                                   user = UserResponse(id=str(user.id), email=user.email),
                                   products = [
                                       OrderProductResponse(
                                           id=str(product.id),
                                           product_name=product.product_name,
                                           product_id=product.product_id,
                                           product_description=product.product_description,
                                           product_price=product.product_price,
                                           created_at=product.created_at,
                                           updated_at=product.updated_at
                                        )
                                        for product in wishlist.products
                                    ],
                                   created_at = wishlist.created_at,
                                   updated_at = wishlist.updated_at                                   
                                ),
                                error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Remove item from Wishlist
@router.delete("/{id}", response_model=ResponseWrapper[None])
async def remove_wishlist_item(id: str, user: User = Depends(get_current_user)):
    try:
        wishlist: Wishlist = Wishlist.objects(user=user).first()
        if not wishlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not Exists")
        
        product: Product = Product.objects(id=id).first()
        
        if product not in wishlist.products:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not in Wishlist")
        
        wishlist.products.remove(product)
        wishlist.save()
        return ResponseWrapper(status="SUCCESS",message="Item Removed from Wishlist Successfully",data=None,error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
