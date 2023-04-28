import time
import bcrypt
from typing import Dict
from app.auth_model import UserLoginSchema

import jwt
from decouple import config

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")

# just for demo, reset the user list each time, implement as a Singleton
class VolatileUserDB():
    
    __instance = None

    def __init__(self):
        if VolatileUserDB.__instance is not None:
            raise Exception("""Attempt to create a VolatileUserDB instance when VolatileUserDB already exists.
            Use VolatileUserDB.get_instance() to get or create the singleton.
            """)
        else:
            VolatileUserDB.__instance = self
            self._users = []
    
    @staticmethod
    def get_instance():
        if VolatileUserDB.__instance is None:
            VolatileUserDB()
        return VolatileUserDB.__instance

    @property
    def users(self) -> str:
        return self._users
    
    @users.setter
    def users(self, users):
        self._users = users

    def add_user(self, user):
        self._users += [user]


def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_email: str) -> Dict[str, str]:
    payload = {
        "user_email": user_email,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else {}
    except:
        return {}

def hash_(password):
    return bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())

def verify_(presented_password, hashed_password):
    return bcrypt.checkpw(presented_password, hashed_password)

def is_registered(data: UserLoginSchema):
    user_container = VolatileUserDB.get_instance()
    return any(verify_(bytes(data.password, "utf-8"), user.password) for user in user_container.users)