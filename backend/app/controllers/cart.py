from typing import List
from fastapi import Depends, HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas.cart import CartRequest, CartResponse, CartUpdate
from app.schemas import ResponseWrapper
from app.models.cart import Cart
from app.models.user import User
from app.models.product import Product
from app.dependencies.get_user import get_current_user

router = APIRouter()

# Add Item to Cart
@router.post("/",response_model=ResponseWrapper[CartResponse])
async def add_to_cart(cart_request: CartRequest):
    try:
        user: User = User.objects(email=cart_request.email).first()
        product: Product = Product.objects(id=cart_request.id).first()
        
        if not user or not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or Product not found")
        
        cart_item: Cart = Cart.objects(user=user, product=product).first()
        if cart_item:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item is already in Cart")
       
        cart: Cart = Cart(
            user = user,
            product = product,
            quantity = cart_request.quantity
        )
        cart.save()
        
        return ResponseWrapper(status="SUCCESS",message="Item is added to cart",
                               data=CartResponse(
                                   id=str(cart.id),
                                   email=str(user.email),
                                   product_id = str(product.id),
                                   quantity = cart.quantity,    
                                   created_at=str(cart.created_at),
                                   updated_at=str(cart.updated_at)
                                ),error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get Cart Item
@router.get("/",response_model=ResponseWrapper[List[CartResponse]])
async def get_cart_item(user: User = Depends(get_current_user)):
    try:
        cart_items: List[Cart] = Cart.objects(user=user)
        cart_list = [
            CartResponse(
                id=str(cart_item.id),
                email=str(user.email),
                product_id=str(cart_item.product.id),
                quantity=cart_item.quantity,
                created_at=str(cart_item.created_at),
                updated_at=str(cart_item.updated_at)
            )
            for cart_item in cart_items
        ]
        
        return ResponseWrapper(status="SUCCESS", message="Cart Items Fetched Successfully",data=cart_list,error=None)
        
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurs while fetching cart items")
 

# Update Cart Item Quantity
@router.put("/{id}",response_model=ResponseWrapper[CartResponse])
async def update_cart_item_quantity(id: str, cart_update: CartUpdate, user = Depends(get_current_user)):
    try:
        cart_item: Cart = Cart.objects(user=user, id=id).first()
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Item not found")

        cart_item.quantity = cart_update.quantity
        cart_item.save()
        
        return ResponseWrapper(status="SUCCESS",message="Cart Item updated successfully",
                               data=CartResponse(
                                   id=str(cart_item.id),
                                   email=str(cart_item.user.email),
                                   product_id = str(cart_item.product.id),
                                   quantity = cart_item.quantity,
                                   created_at=str(cart_item.created_at),
                                   updated_at=str(cart_item.updated_at)
                                ),error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Remove Cart Item
@router.delete("/{id}",response_model=ResponseWrapper[None])
async def remove_cart_item(id: str, user = Depends(get_current_user)):
    try:
        cart_item: Cart = Cart.objects(user=user, id=id).first()
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Item not found")
        
        cart_item.delete()
        return ResponseWrapper(status="SUCCESS", message="Cart Item Removed Successfully",data=None,error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))