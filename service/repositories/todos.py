from models.todo_model import Todo

async def fetch_one(todo_collection, title: str):
    document = await todo_collection.find_one({"title": title})
    return document

async def fetch_all_todos(todo_collection):
    todos = []
    cursor = todo_collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo_collection, todo: Todo):
    document = todo
    result = await todo_collection.insert_one(document)
    return document

async def update_todo(todo_collection, title, desc):
    await todo_collection.update_one({"title": title}, {"$set": {
        "description": desc
    }})
    document = await todo_collection.find_one({"title": title})
    return document

async def delete_one(todo_collection, title):
    await todo_collection.delete_one({"title": title})
    return True