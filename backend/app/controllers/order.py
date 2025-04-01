from typing import List
from fastapi import Depends, HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas import ResponseWrapper
from app.models.cart import Cart
from app.models.user import User
from app.dependencies.get_user import get_current_user
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderResponse, RequestOrderStatus
from app.utils.models_2_schemas.order import create_order_response

router = APIRouter()

# Create an Order
@router.post("/",response_model=ResponseWrapper[OrderResponse])
async def create_order(user: User = Depends(get_current_user)):
    try:
        cart_items: Cart = Cart.objects(user=user)
        if not cart_items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")
            
        total_price = sum(item.product.product_price * item.quantity for item in cart_items)

        order: Order = Order(
            user = user,
            product = [item.product for item in cart_items],
            total_price = total_price,
        )
        order.save()
        Cart.objects(user=user).delete()
        
        return ResponseWrapper(status="SUCCESS", message="Order Placed Successfully!",data=create_order_response(order),error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get all Orders
@router.get("/",response_model=ResponseWrapper[List[OrderResponse]])
async def get_all_orders(user: User = Depends(get_current_user)):
    try:
        orders: Order = Order.objects(user=user)
        
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orders not Found")
        
        return ResponseWrapper(status="SUCCESS",message="Orders fetched successfully",
                               data=[create_order_response(order)
                                     for order in orders],
                               error=None)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get Order by ID
@router.get("/{id}",response_model=ResponseWrapper[OrderResponse])
async def get_order(id: str, user: User = Depends(get_current_user)):
    try:
        order: Order = Order.objects(id=id, user=user).first()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
        
        return ResponseWrapper(status="SUCCESS",message="Order fetched successfully",data=create_order_response(order),error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Update Order Status
@router.put("/{id}",response_model=ResponseWrapper[OrderResponse])
async def update_order_status(id: str, order_status: RequestOrderStatus, user :User=(Depends(get_current_user))):
    try:
        order: Order = Order.objects(id=id, user=user).first()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not Found")
        
        if order_status.status:
            order.status = order_status.status
             
        order.save()
        return ResponseWrapper(status="SUCCESS",message="Status Updated Successfully",data=create_order_response(order),error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Cancel Order by ID
@router.put("/cancel/{id}",response_model=ResponseWrapper[OrderResponse])
async def cancel_order(id: str, user: User=Depends(get_current_user)):
    try:
        order: Order = Order.objects(id=id,user=user).first()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not Found")

        if str(order.status.value) in ["shipped", "delivered"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot cancel a shipped / delivered order")
        
        order.status=OrderStatus.CANCELED
        order.save()
        return ResponseWrapper(status="SUCCESS", message="Order Canceled Successfully",data=create_order_response(order),error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))