from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import func
from sqlmodel import select
from models import Book, BookCreate, BookUpdate
from db import SessionDep
from typing import List

router = APIRouter()

# 8. Obtener todas las categorías de libros
@router.get("/books/categories", response_model=List[str], tags=["Books"], summary="Get all unique book categories")
async def get_all_categories(session: SessionDep):
    # Realiza una consulta para obtener todas las categorías únicas
    query = select(Book.category).distinct()
    result = session.execute(query).scalars().all()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found"
        )

    return result

# 1. Crear un nuevo libro
@router.post("/books", response_model=Book, tags=["Books"], summary="Create a new book")
async def create_book(book_data: BookCreate, session: SessionDep):
    book = Book(**book_data.dict())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


# 2. Listar libros por categoría
@router.get("/books/category/{book_category}", response_model=List[Book], tags=["Books"],
            summary="Get books by category")
async def read_books_by_category(book_category: str, session: SessionDep):
    query = select(Book).where(Book.category == book_category)
    books = session.exec(query).all()

    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No books found in category '{book_category}'"
        )
    return books


# 3. Buscar libros por nombre (insensible a mayúsculas/minúsculas)
@router.get("/books/search/{book_name}", response_model=List[Book], tags=["Books"], summary="Search books by name")
async def search_books_by_name(session: SessionDep, book_name: str):
    # Usar func.lower para ignorar mayúsculas y minúsculas
    query = select(Book).where(func.lower(Book.title) == func.lower(book_name))
    books = session.exec(query).all()

    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No books found with the name '{book_name}'"
        )
    return books


# 4. Listar todos los libros con paginación
@router.get("/books/list", response_model=List[Book], tags=["Books"], summary="List all books")
async def list_books(
        session: SessionDep,
        skip: int = Query(0, description="Records to skip"),
        limit: int = Query(10, description="Number of records to return")
):
    query = select(Book).offset(skip).limit(limit)
    books = session.exec(query).all()
    return books


# 5. Obtener libro por ID
@router.get("/books/{id}", response_model=Book, tags=["Books"], summary="Get book by ID")
async def read_book(id: int, session: SessionDep):
    book_db = session.get(Book, id)
    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book doesn't exist"
        )
    return book_db


# 6. Actualizar un libro por ID
@router.patch("/books/{book_id}", response_model=Book, tags=["Books"], summary="Update book by ID")
async def update_book(book_id: int, book_data: BookUpdate, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book doesn't exist"
        )

    book_data_dict = book_data.dict(exclude_unset=True)
    for key, value in book_data_dict.items():
        setattr(book_db, key, value)

    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    return book_db


# 7. Eliminar un libro por ID
@router.delete("/books/{book_id}", tags=["Books"], summary="Delete book")
async def delete_book(book_id: int, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book doesn't exist"
        )
    session.delete(book_db)
    session.commit()
    return {"detail": "Book deleted successfully"}





