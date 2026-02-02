from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: int
    access_tocken: str

class UserCreateSchema(BaseModel):
    username: str
    password: str