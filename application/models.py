from pydantic import BaseModel


class Quote(BaseModel):
    id: str
    text: str

class User(BaseModel):
    name: str
    email: str 
    phone: str 
    status: str