from app.models.product import Product
from app.schemas.product import ProductResponse
from app.utils.models_2_schemas.subcategory import create_subcategory_response


def create_product_response(product: Product) -> ProductResponse:
    return ProductResponse(
            id=str(product.id),
            product_name=product.product_name,
            product_id=product.product_id,
            product_description = product.product_description,
            product_price=product.product_price,
            product_stock = product.product_stock,
            product_rating = product.product_rating,
            subcategory = create_subcategory_response(product.subcategory),
            created_at=product.created_at,
            updated_at=product.updated_at
    )