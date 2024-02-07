from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserInDB(UserCreate):
    id: int

    class Config:
        orm_mode = True
