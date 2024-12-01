from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship, Session, select
from enum import Enum
from db import engine

class StatusEnum(str, Enum):
    ACTIVE = "favorite"
    INACTIVE = "no favorite"

class UserBooks(SQLModel, table=True):
    id: int = Field(primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)

class BookBase(SQLModel):
    title: str = Field(default=None)
    author: str = Field(default=None)
    year: str = Field(default=None)
    category: str = Field(default=None)
    num_pages: int = Field(default=None)
    image: str = Field(default=None)

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(
        back_populates="books", link_model=UserBooks
    )

class UserBase(SQLModel):
    email: str = Field(default=None)  # Sin usar EmailStr
    password: str | None = Field(default=None)

class UserCreate(UserBase):
    name: str = Field(default=None)

class UserUpdate(UserBase):
    pass

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    books: list[Book] = Relationship(
        back_populates="users", link_model=UserBooks
    )
    is_logged: bool = Field(default=False)

class LoginRequest(UserBase):
    pass
