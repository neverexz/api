from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import uvicorn

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = []

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            print(post)
            return post

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    print(my_posts)
    return my_posts

@app.post("/posts")
async def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": my_posts}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"latest_post": post}

@app.get("/posts/{id}")
async def get_post(id: int):
    print(id)
    return {f"post_{id}": find_post(id)}
    

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )