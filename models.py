from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional, List
import random

PROFILE_PICTURES = [
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQdf7rYhCFkpfEMCS3_YjH5smapUlcVezp9WpXU54rrz4bhStYQAc6BZHHyD4XJ_xo4iIuGRfS5PtvGYiz__nCey5YbD8V2Nzxy1x3Z6Xh-d5NHHatPDbz3URCzbLplNPw6A79CJzkNvgJJkLzB1KRmJm.png?r=6d1",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQcxP3g8WyiGzAxSt8qSTmLyVGZkIlRMQqTTn5w_IN8M5tUJmFqX1z0-Rl-Yf7aazK0AxZ1B52mvdrkzvOpEqaMuPeDkSHLyE2bTFV7KZlu6XVgSy5yKunHkGUqW5JMNmcac-IIo9xlP36mdYv2RKdwRY.png?r=ac6",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQV8jWMWTVyLm4FyQLgCDuPzQFoELAKCHZ_mm74uZX4kcsdoz82ly0BiCPwuqo4Zm57xVJIkNOzbNWFxTiNDcx73eMAGXcJMNYAhFikCjmER-DZ6Yd1DSKh_W07ZzFCytbJeekDTKIy90BV2e-q3Zm0lN.png?r=be9",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQSGbTxO2EJTp1HS1RXKWvQWkeSJQ8PpLwv6wWF-Vtv_R4skE3WRdf4DSE3ykyeHogjK_cLfIpvS1GUJZMR04ZhQDvTXcHMWci4H9sLzmTS-dxmjbqsL-IO_svJBz7VJtG5qFL2SCG12HUnLqdpNPKfIM.png?r=d98",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQUBycgDBQwiaHZ_LqPCwqfLSTVyOneoakDiPM5lPJ2mY2tvkXEN17ADbsKKWXSJTXcYk3B9wmI7xzUzB0FYyhELBJi2jEAoMvplJ40mqTf62Q36abJyCRmjgMHN4NdV3iu6RqWx6CxQ8eXfFbJZPxOCc.png?r=620",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQXi9TU8-sfAu3qnQmaoHlrievPw38-OZzL4roFczJPJ6nAzOUB0CmLQ54FqE6aK_277YwbpcpxpWQiS2fEMWEJ0DnVLBPegC3gK_k_SHjQ-Sk5RTMeNJR3iWYmDQZDV0SpgtWjS4APt68N7cJkyydq4q.png?r=b68",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQXx_6DocAYc0fYquDuv4m3fSfTLYouG8YRSLOrBrX3L-Pog4eCHIXfc6PHf7C-jOVCCTRB1XdAaQX0hpfu3nDSXHeX6G_vu7rQv325JL_OZiPEJQ9tjEPRslTLjlleDC2MTyFQG1uHkcmUJcyIB_f6uT.png?r=21f",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQePwS-NMhMsYw0QyOTIrImOQo5sqzXPwTldo7dbLfm5yWo1uqstas7w-CfnQppDdu394ZwCq0Ut7trDpXSRUWXGg67mSbEakqR5WFvv4pmWsblFGYOn1eY75dWL7ReOP7vmTbk9lGltfnDzTJibzuyxe.png?r=568",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQe6It_8trjkSKsijp8Jzz5fYvFhEo8JB4UIjgGCIHfCrHs6v5kBYNDIofPCeNqHss1Bn_YnJ-zFo4ZLBR8gz71A-ren1omQIXgXm2F2eFPQDWHIaacE9hOhCMynA4ecip98ZbmwJmpNKL0shsCjS5fIB.png?r=30a",
    "https://dnm.nflximg.net/api/v6/2DuQlx0fM4wd1nzqm5BFBi6ILa8/AAAAQeIGj2jVceUK5bQJPhi_Sz75cxQtxeswgkaSC3BcbAhKOiQAc-kgZwQJqFZ2SC_LPAapbBCkCA5aUl5KtgGTWGtC2BSGNZM6JmYhkn3E8jffX8sAqA3BXJrllLJLNSPRLQVhl0UqA90DF9Xn9vBx708L.png?r=1e4",
]


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
    book: "Book" = Relationship(back_populates="user_books")


# Base de modelo para los libros (común entre la creación, actualización y el libro en sí)
class BookBase(SQLModel):
    title: str = Field(default=None)
    author: str = Field(default=None)
    year: Optional[int] = Field(default=None)
    category: str = Field(default=None)
    num_pages: Optional[int] = Field(default=None)
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
    user_books: list[UserBooks] = Relationship(back_populates="book")




# Base de modelo para los usuarios (común entre la creación, actualización y el usuario en sí)
class UserBase(SQLModel):
    email: EmailStr = Field(default=None, unique=True)
    password: str = Field(default=None)
    image: Optional[str] = Field(default_factory=lambda: random.choice(PROFILE_PICTURES))
    name: str = Field(default=None)

# Modelo para crear un usuario
class UserCreate(UserBase):
    pass

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
