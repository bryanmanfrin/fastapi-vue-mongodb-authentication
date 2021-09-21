
from models.user_signup_model import UserInDB
from database import database


async def create_user(user: UserInDB):
    await database.users_collection.insert_one(user)


async def find_user(username: str):
    user = await database.users_collection.find_one({'username': username})
    return user
