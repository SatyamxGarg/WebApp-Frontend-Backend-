from app.models.subcategory import Subcategory
from app.schemas.category import SubcategoryResponse
from app.utils.models_2_schemas.category import create_category_response


def create_subcategory_response(subcategory: Subcategory) -> SubcategoryResponse:
    return SubcategoryResponse(
         id = str(subcategory.id),
         subcategory_id= subcategory.subcategory_id,
         subcategory_name = subcategory.subcategory_name,
         subcategory_description = subcategory.subcategory_description,
         category = create_category_response(subcategory.category),
         created_at = subcategory.created_at,
         updated_at = subcategory.updated_at   
    )