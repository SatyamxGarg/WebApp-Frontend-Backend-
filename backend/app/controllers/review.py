from fastapi import Depends, HTTPException, APIRouter, status
from mongoengine import ValidationError
from app.schemas import ResponseWrapper
from app.models.user import User
from app.dependencies.get_user import get_current_user
from app.schemas.review import ReviewRequest, ReviewResponse
from app.models.product import Product
from app.models.review import Review
from app.utils.models_2_schemas.review import create_review_response

router = APIRouter()


# Create Review
@router.post("/{id}",response_model=ResponseWrapper[ReviewResponse])
async def add_review(id: str, review_req: ReviewRequest, user: User = Depends(get_current_user)):
    try:
        product: Product = Product.objects(id=id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        existing_review: Review = Review.objects(user=user, product=product).first()
        if existing_review:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already reviewed the Product")
        
        review: Review = Review(
            user = user,
            product = product,
            rating = review_req.rating,
            review_text = review_req.review_text
        )
        review.save()
        calculate_avg_rating(product)
        
        return ResponseWrapper(status="SUCCESS", message="Product Successfully Reviewed", data=create_review_response(review), error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get all Reviews for Product
@router.get("/{id}",response_model=ResponseWrapper[list[ReviewResponse]])
async def get_reviews(id: str):
    try:
        product: Product = Product.objects(id=id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not Found")

        reviews: list[Review] = Review.objects(product=product).order_by('-created_at')
        
        return ResponseWrapper(status="SUCCESS", message="Reviews fetched successfully",
                               data=[create_review_response(review)
                                    for review in reviews],
                                error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Update review by ID
@router.put("/{id}",response_model=ResponseWrapper[ReviewResponse])
async def update_review(id: str, review_req: ReviewRequest, user:User = Depends(get_current_user)):
    try:
        review: Review = Review.objects(id=id, user=user).first()
        
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not Found")
        
        review.rating =  review_req.rating
        review.review_text = review_req.review_text
        review.save()
        
        return ResponseWrapper(status="SUCCESS", message="Review updated Successfully", data=create_review_response(review),error=None)
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Delete Review by ID
@router.delete("/{id}", response_model=ResponseWrapper[None])
async def delete_review(id: str, user: User = Depends(get_current_user)):
    try:
        review: Review = Review.objects(id=id, user=user).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not Found")
        
        review.delete()
        return ResponseWrapper(status="SUCCESS", message="Review Deleted Successfully", data=None, error=None)
        
    except ValidationError as e:
        raise  HTTPException(status_code=400, detail=str(e))


# Function to calcualte product's average rating
def calculate_avg_rating(product: Product):
    try:
        reviews: Review = Review.objects(product=product)
        
        if reviews:
            avg_rating = sum( review.rating for review in reviews)/ len(reviews)
            product.product_rating = round(avg_rating,1)
        
        else:
            product.product_rating = 0.0
        product.save()
        
    except ValidationError as e:
        raise  HTTPException(status_code=400, detail=str(e))