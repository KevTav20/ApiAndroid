from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from db import SessionDep
from models import (
    User, UserCreate, UserUpdate, UserBooks, Book, StatusEnum, LoginRequest
)

router = APIRouter()

@router.post("/login", tags=["auth"], summary="User login")
async def login(request: LoginRequest, session: SessionDep):
    query = select(User).where(User.email == request.email)
    user_db = session.exec(query).first()

    if not user_db or user_db.password != request.password:  # Simple password comparison
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    user_db.is_logged = True
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return {
        "id": user_db.id,
        "is_logged": user_db.is_logged,
        "message": "Login successful"
    }

@router.get("/users", response_model=list[User], tags=["users"], summary="List all users")
async def list_users(session: SessionDep):
    return session.exec(select(User)).all()

@router.get("/users/{user_id}", response_model=User, tags=["users"], summary="Get user by ID")
async def read_user(user_id: int, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    return user_db

@router.get("/users/{user_id}/books", tags=["users"], summary="Get user's books by status")
async def read_books_to_user(
    user_id: int,
    session: SessionDep,
    book_status: StatusEnum = Query(..., description="Filter books by status")
):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )

    query = (
        select(UserBooks)
        .where(UserBooks.user_id == user_id)
        .where(UserBooks.status == book_status)
    )
    books = session.exec(query).all()
    return books

@router.post("/users/create", response_model=User, tags=["users"], summary="Create a new user")
async def create_user(user_data: UserCreate, session: SessionDep):
    user = User(**user_data.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/users/{user_id}/books/{book_id}", tags=["users"], summary="Associate book with user")
async def subscribe_book_to_user(
    user_id: int,
    book_id: int,
    session: SessionDep,
    book_status: StatusEnum = Query(..., description="Book status")
):
    user_db = session.get(User, user_id)
    book_db = session.get(Book, book_id)

    if not user_db or not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user or book doesn't exist"
        )

    user_book_db = UserBooks(
        book_id=book_db.id,
        user_id=user_db.id,
        status=book_status
    )

    session.add(user_book_db)
    session.commit()
    session.refresh(user_book_db)
    return user_book_db

@router.patch("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK, tags=["users"], summary="Update user by ID")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: SessionDep
):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )

    user_data_dict = user_data.dict(exclude_unset=True)
    for key, value in user_data_dict.items():
        setattr(user_db, key, value)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.delete("/users/{user_id}", tags=["users"], summary="Delete user")
async def delete_user(user_id: int, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )

    session.delete(user_db)
    session.commit()
    return {"detail": "User deleted successfully"}
