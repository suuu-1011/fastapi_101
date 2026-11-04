from fastapi import FastAPI, status,  HTTPException

from .db import read_data, save_data
from .models import Quote, User


app = FastAPI()


QUOTES_DB = read_data()
USER_DB = read_data("users.json")


@app.get("/")
def home():
    return "Welcome to the Quotes Library!"


@app.get("/quotes")
async def list_quotes():
    return QUOTES_DB


@app.get("/quotes/{item_id}")
async def quote_detail(item_id: str):
    detail = {
        "quote_id": item_id,
        "quote": QUOTES_DB[item_id]
    }
    return detail


@app.post("/quotes", status_code=status.HTTP_201_CREATED)
async def create_quote(item: Quote):
    QUOTES_DB[item.id] = item.text
    save_data(QUOTES_DB)
    return {"message": f"Quote '{item.id}' was created!"}

# GET all users
@app.get("/users")
async def get_users():
    return USER_DB


# GET user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    if user_id not in USER_DB:
        raise HTTPException(status_code=404, detail="User not found")

    return USER_DB[user_id]


# POST create user
@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_user(user_id: str, user: User):
    USER_DB[user_id] = user.dict()
    save_data(USER_DB, "users.json")
    return {"message": "User created successfully"}


# PUT update user
@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    if user_id not in USER_DB:
        raise HTTPException(status_code=404, detail="User not found")

    USER_DB[user_id] = user.dict()
    save_data(USER_DB, "users.json")
    return {"message": "User updated successfully"}


# DELETE user
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    if user_id not in USER_DB:
        raise HTTPException(status_code=404, detail="User not found")

    del USER_DB[user_id]
    save_data(USER_DB, "users.json")
    return {"message": "User deleted successfully"}


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}