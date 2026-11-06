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

    class Config:
        orm_mode = True


# Task Schemas

class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    status: Literal["pending", "in progeress", "done"] = "pending"
    user_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = None
    status: Optional[Literal["pending", "in progeress", "done"]] = None


class UserWithTasks(UserResponse):
    tasks: list[TaskResponse] = []