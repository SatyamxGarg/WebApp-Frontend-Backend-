from app.models.review import Review
from app.schemas.review import ReviewResponse


def create_review_response(review: Review) -> ReviewResponse:
    return ReviewResponse(
        id = str(review.id),
        rating = review.rating,
        review_text = review.review_text,
        created_at = review.created_at,
        updated_at = review.updated_at
    )