from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
        from_attributes=True


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        from_attributes=True
        orm_mode = True
