from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schema for user signup
class UserSignUp(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password for account creation")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "first_name": "John",
                "last_name": "Doe"
            }
        }

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password for login")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }

# Schema for token response
class Token(BaseModel):
    access_token: str = Field(..., description="Access token for authenticated requests")
    token_type: str = Field(..., description="Type of token, typically 'Bearer'")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer"
            }
        }

# Schema for token data
class TokenData(BaseModel):
    username: Optional[str] = Field(None, description="Username or email associated with the token")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user@example.com"
            }
        }