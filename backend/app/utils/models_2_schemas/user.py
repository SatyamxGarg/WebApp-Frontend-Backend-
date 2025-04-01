from app.models.user import User
from app.schemas.order import UserResponse


def create_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email
    )