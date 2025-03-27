from typing import List
from fastapi import Depends, HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas import ResponseWrapper
from app.models.cart import Cart
from app.models.user import User
from app.dependencies.get_user import get_current_user
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderResponse, RequestOrderStatus, UserResponse
from app.schemas.product import OrderProductResponse, ProductResponse

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
        
        return ResponseWrapper(status="SUCCESS", message="Order Placed Successfully!",
                               data=OrderResponse(
                                id=str(order.id),
                                user = UserResponse(id=str(user.id), email=user.email),
                                product = [OrderProductResponse(id=str(item.id), product_name=item.product_name, product_id=item.product_id,
                                                           product_price=item.product_price, product_description=item.product_description,
                                                           created_at=item.created_at,updated_at=item.updated_at)
                                           for item in order.product],
                                total_price = order.total_price,
                                status = order.status,
                                payment_status = order.payment_status,
                                created_at = order.created_at,
                                updated_at = order.updated_at
                                ),error=None)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get all Orders
@router.get("/",response_model=ResponseWrapper[List[OrderResponse]])
async def get_all_orders(user: User = Depends(get_current_user)):
    try:
        orders: Order = Order.objects(user=user)
        
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orders not Found")
    
        order_list=[
            OrderResponse(
                id=str(order.id),
                user = UserResponse(id=str(user.id), email=user.email),
                product = [OrderProductResponse(id=str(item.id), product_name=item.product_name, product_id=item.product_id,
                                           product_price=item.product_price, product_description=item.product_description,
                                           created_at=item.created_at,updated_at=item.updated_at)
                                        for item in order.product],
                total_price = order.total_price,
                status = order.status,
                payment_status = order.payment_status,
                created_at = order.created_at,
                updated_at = order.updated_at
            )
            for order in orders
        ]
        
        return ResponseWrapper(status="SUCCESS",message="Orders fetched successfully",data=order_list,error=None)
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get Order by ID
@router.get("/{id}",response_model=ResponseWrapper[OrderResponse])
async def get_order(id: str, user: User = Depends(get_current_user)):
    try:
        order: Order = Order.objects(id=id, user=user).first()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
        
        return ResponseWrapper(status="SUCCESS",message="Order fetched successfully",
                               data=OrderResponse(
                                id=str(order.id),
                                user = UserResponse(id=str(user.id), email=user.email),
                                product = [OrderProductResponse(id=str(item.id), product_name=item.product_name, product_id=item.product_id,
                                                           product_price=item.product_price, product_description=item.product_description,
                                                           created_at=item.created_at,updated_at=item.updated_at)
                                           for item in order.product],
                                total_price = order.total_price,
                                status = order.status,
                                payment_status = order.payment_status,
                                created_at = order.created_at,
                                updated_at = order.updated_at
                                ),error=None)
        
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
        return ResponseWrapper(status="SUCCESS",message="Status Updated Successfully",
                               data=OrderResponse(
                                id=str(order.id),
                                user = UserResponse(id=str(user.id), email=user.email),
                                product = [OrderProductResponse(id=str(item.id), product_name=item.product_name, product_id=item.product_id,
                                                           product_price=item.product_price, product_description=item.product_description,
                                                           created_at=item.created_at,updated_at=item.updated_at)
                                           for item in order.product],
                                total_price = order.total_price,
                                status = order.status,
                                payment_status = order.payment_status,
                                created_at = order.created_at,
                                updated_at = order.updated_at
                                ),error=None)
        
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
        return ResponseWrapper(status="SUCCESS", message="Order Canceled Successfully",
                               data=OrderResponse(
                                id=str(order.id),
                                user = UserResponse(id=str(user.id), email=user.email),
                                product = [OrderProductResponse(id=str(item.id), product_name=item.product_name, product_id=item.product_id,
                                                           product_price=item.product_price, product_description=item.product_description,
                                                           created_at=item.created_at,updated_at=item.updated_at)
                                           for item in order.product],
                                total_price = order.total_price,
                                status = order.status,
                                payment_status = order.payment_status,
                                created_at = order.created_at,
                                updated_at = order.updated_at
                                ),error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))