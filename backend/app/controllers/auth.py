from fastapi import HTTPException, Depends, APIRouter, status
from mongoengine.errors import NotUniqueError
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, Dict, Any

from app.configs import settings
from app.schemas.auth import Token, UserLogin, UserSignUp, UpdateUser
from app.schemas import ResponseWrapper
from app.models.user import User
from app.utils.crypto import hash_password, verify_password
from app.dependencies import get_current_user

router = APIRouter()

SECRET_KEY = settings.JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_EXPIRE_TIME_MIN
HASH_ALGORITHM = "HS256"


# Helper function to create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=ResponseWrapper[Token])
async def signup(user_data: UserSignUp):
    hashed_password = hash_password(user_data.password)
    
    try:
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        user.save()

        access_token = create_access_token(data={"sub": user.email})
        return ResponseWrapper(status="SUCCESS", message="User registered successfully", data={"access_token": access_token, "token_type": "bearer"}, error=None)
    
    except NotUniqueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during registration")


@router.post("/login", response_model=ResponseWrapper[Token])
async def login(user_data: UserLogin):
    user: User = User.objects(email=user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    # Generate JWT token for the user
    access_token = create_access_token(data={"sub": user.email})
    return ResponseWrapper(status="SUCCESS", message="Login successful", data={"access_token": access_token, "token_type": "bearer"}, error=None)


@router.get("/users/me", response_model=ResponseWrapper[Dict[str, Any]])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return ResponseWrapper(
        status="SUCCESS",
        message="User details fetched successfully", 
        data={
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'created_at': current_user.created_at,
            'updated_at': current_user.updated_at
        }, 
        error=None
    )

@router.put("/update",response_model=ResponseWrapper[Dict[str,Any]])
async def update_user(updated_data: UpdateUser, current_user: User = Depends(get_current_user)):
        if updated_data.first_name:
            current_user.first_name = updated_data.first_name
        if updated_data.last_name:
            current_user.last_name = updated_data.last_name
        
        current_user.save()
        return ResponseWrapper(status="SUCCESS",message="Details Updated Successfully!",data={
            "email":current_user.email,
            "first_name":current_user.first_name,
            "last_name":current_user.last_name
        },error=None)
        