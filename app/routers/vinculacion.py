from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import Session, select
from models import UserBooks, StatusEnum, Book, User
from db import SessionDep
from typing import Optional

router = APIRouter()

# 3. Consultar libros asociados a un usuario por estado
@router.get("/user/{user_id}/books/", tags=["Vinculation"])
async def read_book_to_user(
    user_id: int,
    session: SessionDep,
    book_status: StatusEnum = Query()
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

# 5. Asociar un libro a un usuario
@router.post("/user/{user_id}/books/{book_id}", tags=["Vinculation"])
async def subscribe_book_to_user(
    user_id: int,
    book_id: int,
    session: SessionDep,
    book_status: StatusEnum = Query()
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