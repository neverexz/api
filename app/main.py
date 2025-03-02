from turtle import st
from typing import Optional
from annotated_types import T
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
    
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = []

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            print(post)
            return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return -1
            
while True:
    try:
        connection_bd = psycopg2.connect(host='localhost', database='petik', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = connection_bd.cursor()
        print("database connected")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(3)
# что-то другое
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id:{id} not found")
        # also usable
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"response_detail": f"Post id:{id} not found"}
    return {f"post_{id}": post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id:{id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id:{id} not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}

# uvicorn app.main:app --reload
# run with this command app. - folder name
# main is the file name and :app is app = FastAPI()
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )