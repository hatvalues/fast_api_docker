from typing import Union
from fastapi import FastAPI, Body, Depends

from app.auth_handler import signJWT, is_registered, hash_
from app.auth_handler import VolatileUserDB
from app.auth_bearer import JWTBearer

from app.auth_model import UserSchema, UserLoginSchema
from app.demo_model import Item
from app.blog_model import BlogPost

from fastapi import FastAPI

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users_container = VolatileUserDB.get_instance()

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> str:
    return "OK"

@app.get("/hello")
async def read_root() -> dict:
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None) -> dict:
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict:
    return {"item_id": item_id, "item_name": item.name, "price": item.price}

@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return { "data": posts }

@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

# Depends introduces a dependency injection.JWTBearer verifies the bearer token
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: BlogPost) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    # Hash a password for the first time, with a randomly-generated salt
    user.password = hash_(user.password)
    users_container.add_user(user)
    return signJWT(user.email)

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if is_registered(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

