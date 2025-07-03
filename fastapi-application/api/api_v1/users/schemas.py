from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Схема пользователей"""

    id: int
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
