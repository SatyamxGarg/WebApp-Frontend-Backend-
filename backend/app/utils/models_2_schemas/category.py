from app.models.category import Category
from app.schemas.category import CategoryResponse


def create_category_response(category: Category) -> CategoryResponse:
    return CategoryResponse(
         id=str(category.id),
         category_id=category.category_id,
         category_name=category.category_name,
         category_description=category.category_description,
         created_at=category.created_at,
         updated_at=category.updated_at
    )