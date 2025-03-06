from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import uvicorn
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import model
from database import *
from database import *


model.Base.metadata.create_all(bind=engine)
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

            
while True:
    try:
        connection_bd = psycopg2.connect(host='localhost', database='petik', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = connection_bd.cursor()
        print("database connected")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(3)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(model.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(f"""insert into posts (title, content, published) values ({post.title}, {post.content}, {post.published})""")
    # небезопасно, возможны SQL-инъекции
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # my_posts = cursor.fetchone()
    # connection_bd.commit()
    new_post = model.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/latest")
async def get_latest_post():
    cursor.execute("""SELECT * FROM posts order by created_at limit 1""")
    post = cursor.fetchone()
    return {"latest_post": post}

@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
                                                          # ожидает кортеж!
    cursor.execute("""select * from posts where id=%s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id:{id} not found")
    return {"data": post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""delete from posts where id=%s returning *""", (id,))
    delete_post = cursor.fetchone()
    if not delete_post:
        print(delete_post)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id:{id} not found")
    connection_bd.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning *""", (post.title, post.content, post.published, id))
    update_post = cursor.fetchone()
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id:{id} not found")
    connection_bd.commit()
    return {'data': update_post}

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