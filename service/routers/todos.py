from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from models.todo_model import Todo
from typing import List
from repositories import todos as todos_repo
from database import database

router = APIRouter(
    prefix = '/todos',
    tags = ['Todos'],
)

@router.get("/")
async def index(todos = Depends(database.get_todos)): 
    response = await todos_repo.fetch_all_todos(todos)
    return response

@router.get("/{title}", response_model=Todo)
async def get_todo_by_id(title, todos = Depends(database.get_todos)):
    response = await todos_repo.fetch_one(todos, title)
    if response:
        return response
    raise HTTPException(404, f"There is no TODO with that title {title}")

@router.post("/", response_model=Todo)
async def post_todo(todo: Todo, todos = Depends(database.get_todos)):
    response = await todos_repo.create_todo(todos, todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@router.put("/{id}")
async def put_todo(title, desc, todos = Depends(database.get_todos)):
    response = await todos_repo.update_todo(todos, title, desc)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@router.delete("/{title}")
async def delete_todo(title, todos = Depends(database.get_todos)):
    response = await todos_repo.delete_one(todos, title)
    if response:
        return "successfully deleted todo"
    raise HTTPException(404, "Title not found") 