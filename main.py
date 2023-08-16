from fastapi import FastAPI, Body, UploadFile, status, File, Depends, Form
from pydantic import BaseModel
from typing import Optional, Annotated
import psycopg2, shutil, io
from psycopg2.extras import RealDictCursor
from PIL import Image


app = FastAPI()

class Post(BaseModel):
    title: str
    published: bool = True


try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('database connected')
except Exception as error:
    print('connecting to database failed')



@app.get("/")
async def root():
    return {"message": "It is working"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM POSTS""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post = Depends(), content: UploadFile = File(...)):
    file_location = f"./ss.png"
    img= open(file_location, "rb")# as file_object
    # img1=shutil.copyfileobj(content.file, img)  
    print(img.read())

    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning * ",(post.title, psycopg2.Binary(img.read()), post.published))
    print(post.title, content.file, post.published) #like objects we can access..
    conn.commit()
    post = cursor.fetchone()
    return {"data": post}

@app.get("/retrive/{id}", status_code=status.HTTP_201_CREATED)
async def get_post(id: int):
        cursor.execute(f"select * from posts where posts.id = {id}")
        post = cursor.fetchone()
        # print(post['content'])
        image_data = post['content']
        print(image_data)
        image = Image.open(io.BytesIO(image_data))
        image.show()
        return {"data": post, "image":image.show()}




