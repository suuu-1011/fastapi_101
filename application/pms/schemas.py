from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import Literal
from pydantic import StrictStr


# User Schemas

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str
    phone: StrictStr = Field(min_length=10, max_length=15)
    status: str = "active"

class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str
    phone: str = Field(min_length=10, max_length=15)
    status: str = "active"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    status: str
    created_at: datetime
    role: str

    class Config:
        orm_mode = True


# Task Schemas

class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    status: Literal["pending", "in progress", "done"] = "pending"
    user_id: int



class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    user_id: int
    work_notes: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = None
    status: Optional[Literal["pending", "in progress", "done"]] = None
    user_id: Optional[int] = None


class UserWithTasks(UserResponse):
    tasks: list[TaskResponse] = []

# Authentication Schemas

class AuthRegister(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: str = Field(
        min_length=5,
        max_length=100,
        regex=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )
    phone: StrictStr = Field(min_length=10, max_length=15)
    password: StrictStr = Field(min_length=8, max_length=128)


class AuthLogin(BaseModel):
    email: str
    password: StrictStr


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthUserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: Literal["teacher", "student"]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class RefreshTokenRequest(BaseModel):
    refresh_token: StrictStr

class StudentTaskUpdate(BaseModel):
    status: Optional[Literal["pending", "in progress", "done"]] = None
    work_notes: Optional[str] = None