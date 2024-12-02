from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional, List

# Enum para el estado de los libros
class StatusEnum(str, Enum):
    ACTIVE = "favorite"
    INACTIVE = "no favorite"

# Modelo de la relación entre usuarios y libros
class UserBooks(SQLModel, table=True):
    id: int = Field(primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")
    status: StatusEnum = Field(default=StatusEnum.INACTIVE)


# Base de modelo para los libros (común entre la creación, actualización y el libro en sí)
class BookBase(SQLModel):
    title: str = Field(default=None)
    author: str = Field(default=None)
    year: Optional[int] = Field(default=None)  # Cambié 'str' por 'Optional[int]'
    category: str = Field(default=None)
    num_pages: Optional[int] = Field(default=None)  # Cambié 'int' por 'Optional[int]'
    image: Optional[str] = Field(default=None)
    synopsis: Optional[str] = Field(default=None)

# Modelo para crear un libro
class BookCreate(BookBase):
    pass

# Modelo para actualizar un libro
class BookUpdate(BookBase):
    pass

# Modelo para el libro
class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: list["User"] = Relationship(
        back_populates="books", link_model=UserBooks
    )




# Base de modelo para los usuarios (común entre la creación, actualización y el usuario en sí)
class UserBase(SQLModel):
    email: EmailStr = Field(default=None, unique=True)  # Usé 'EmailStr' de Pydantic para validación de email
    password: str = Field(default=None)

# Modelo para crear un usuario
class UserCreate(UserBase):
    name: str = Field(default=None)

# Modelo para actualizar un usuario
class UserUpdate(UserBase):
    pass

# Modelo para el usuario
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List[Book] = Relationship(
        back_populates="users", link_model=UserBooks
    )
    is_logged: bool = Field(default=False)



# Modelo para el login de un usuario
class LoginRequest(UserBase):
    pass
