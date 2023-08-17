from fastapi import FastAPI, Body, UploadFile, status, File, Depends, Form
from pydantic import BaseModel
from typing import Optional, Annotated
import psycopg2, shutil, io
from psycopg2.extras import RealDictCursor
from PIL import Image
import os, base64


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
    # image_path = os.path.join("upload", content.filename)
    # Image.open(image_path).save(image_path, quality=50)

    # file_location = f"./ss.png"
    # with open(os.path.join('upload', post.title), "wb+") as file_object:
    #     shutil.copyfileobj(content.file, file_object)  
    # print(img.read())
    fn, fext = os.path.splitext(content.filename)
    img = Image.open(content.file)
    img.thumbnail((200,200))
    img.save(f'upload/{fn}_thumb{fext}')

    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning * ",(post.title, psycopg2.Binary(content.file.read()), post.published))
    print(post.title, content.file, post.published) #like objects we can access..
    conn.commit()
    post = cursor.fetchone()
    return {"data": post}

@app.get("/retrive/{id}", status_code=status.HTTP_201_CREATED)
async def get_post(id: int):
        cursor.execute(f"select * from posts where posts.id = {id}")
        post = cursor.fetchone()
        data=post['content']
        image = Image.open(io.BytesIO(data))
        image.show('upload/ss.png')
        
        # with open(os.path.join('upload', post['title']),'wb') as file:
        #     file.write(base64.b64decode(data))
        return {"data": "go see"}




