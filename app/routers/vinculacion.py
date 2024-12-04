from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select
from models import UserBooks, StatusEnum, Book, User
from db import SessionDep
from typing import Optional
router = APIRouter()

# 3. Consultar libros asociados a un usuario por estado
@router.get("/user/{user_id}/books", response_model=list[Book], tags=["Vinculation"], summary="Get books by user")
async def get_books_by_user(
    user_id: int,
    session: SessionDep,
    status: Optional[StatusEnum] = Query(None, description="Filter by book status")
):
    # Verificar si el usuario existe
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )

    # Construir la consulta para libros asociados al usuario
    query = (
        select(UserBooks)
        .where(UserBooks.user_id == user_id)
        .options(joinedload(UserBooks.book))  # Cargar libros relacionados
    )

    # Aplicar filtro por estado si se proporciona
    if status:
        query = query.where(UserBooks.status == status)

    user_books = session.exec(query).all()

    # Formatear respuesta
    books = [
        {
            "id": ub.book.id,
            "title": ub.book.title,
            "author": ub.book.author,
            "year": ub.book.year,
            "category": ub.book.category,
            "num_pages": ub.book.num_pages,
            "image": ub.book.image,
            "synopsis": ub.book.synopsis,
            "status": ub.status,
        }
        for ub in user_books
    ]

    return books


@router.get("/users/{user_id}/books/{book_id}/exists", tags=["Vinculation"])
async def is_book_linked_to_user(
        user_id: int,
        book_id: int,
        session: SessionDep
):
    # Verificar si el usuario existe
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )

    # Consultar si el libro está vinculado al usuario
    query = select(UserBooks).where(
        UserBooks.user_id == user_id,
        UserBooks.book_id == book_id
    )
    user_book = session.exec(query).first()

    # Devolver el resultado
    return {"exists": bool(user_book)}

@router.get("/users/{user_id}/books/", tags=["Vinculation"])
async def read_book_to_user(
    user_id: int,
    session: SessionDep,
    book_status: Optional[StatusEnum] = Query(None)
):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    query = select(UserBooks).where(UserBooks.user_id == user_id)
    if book_status:
        query = query.where(UserBooks.status == book_status)

    user_books = session.exec(query).all()
    return user_books

@router.post("/user/{user_id}/books/{book_id}/link", tags=["Vinculation"], summary="Link a book to a user")
async def link_book_to_user(
    user_id: int,
    book_id: int,
    session: SessionDep,
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
    )

    session.add(user_book_db)
    session.commit()
    session.refresh(user_book_db)
    return user_book_db

@router.patch("/user/{user_id}/books/{book_id}/favorite", tags=["Vinculation"])
async def mark_book_as_favorite(
    user_id: int,
    book_id: int,
    session: SessionDep
):
    user_book_db = session.exec(
        select(UserBooks).where(
            UserBooks.user_id == user_id,
            UserBooks.book_id == book_id
        )
    ).first()

    if not user_book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user-book relationship doesn't exist"
        )

    if user_book_db.status == StatusEnum.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The book is already marked as favorite"
        )

    user_book_db.status = StatusEnum.ACTIVE
    session.add(user_book_db)
    session.commit()
    session.refresh(user_book_db)
    return user_book_db
