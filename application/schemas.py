from pydantic import BaseModel, Field 
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50, pattern=r"^[a-zA-Z ]+$")
    email: str 
    phone: str = Field(min_length=10, max_length=15, pattern=r"^[0-9]+$")
    status: str = "active"

class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50, pattern=r"^[a-zA-Z ]+$")
    email: str 
    phone: str = Field(min_length=10, max_length=15, pattern=r"^[0-9]+$")
    status: str = "active"

class UserResponse(BaseModel):
    name: str 
    email: str 
    phone: str
    status: str 

#basemodel is parent class for pydantic shemas. field is constraint. default status is set to active.
