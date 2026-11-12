from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserResponse(UserCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    views: Optional[int] = 0

class PostResponse(PostCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserAnalytics(BaseModel):
    user_id: int
    user_name: str
    total_posts: int
    total_views: int