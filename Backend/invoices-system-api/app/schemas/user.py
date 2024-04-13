from pydantic import BaseModel
from uuid import UUID

class BaseUser(BaseModel):
    username: str

class CreateUser(BaseUser):
    password: str

class LoginUser(BaseUser):
    password: str

class ResponseUser(BaseUser):
    id: UUID

class Token(BaseModel):
    access_token: str
    token_type: str