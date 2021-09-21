from models.todo_model import Todo
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://localhost:28000'
)  # connexion between database.py and mongodb

database = client.TodoList  # TodoList = db name

todo_collection = database.todo  # todo = collection name
users_collection = database.users  # users = collection name


def get_database():
    return client.TodoList


def get_todos():
    return database.todo


def get_users():
    return database.users
