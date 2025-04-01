from app.models.order import Order
from app.schemas.order import OrderResponse
from app.utils.models_2_schemas.user import create_user_response
from app.utils.models_2_schemas.product import create_product_response


def create_order_response(order: Order) -> OrderResponse:
    return OrderResponse(
         id=str(order.id),
         user = create_user_response(order.user),
         product = [create_product_response(item) for item in order.product],
         total_price = order.total_price,
         status = order.status,
         payment_status = order.payment_status,
         created_at = order.created_at,
         updated_at = order.updated_at
    )