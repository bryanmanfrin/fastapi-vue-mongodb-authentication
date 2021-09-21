from models.user_signup_model import User
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


from routers import todos
from routers import auth

app = FastAPI()
origins = ['http://localhost:8080']


class MyModel(BaseModel):
    title: str
    body: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router)
app.include_router(auth.router)


# if __name__ == '__main__':
#   uvicorn.run(app)
