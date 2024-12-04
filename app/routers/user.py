import random
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import User, UserCreate, UserUpdate, LoginRequest, PROFILE_PICTURES
from db import SessionDep
from typing import List

router = APIRouter()

# 1. Crear un nuevo usuario
@router.post("/users", response_model=User, tags=["Users"], summary="Create a new user")
async def create_user(user_data: UserCreate, session: SessionDep):
    # Verificar que el correo no exista previamente
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Asignar una imagen aleatoria si no se proporciona
    image = user_data.image or random.choice(PROFILE_PICTURES)

    user = User(
        email=user_data.email,
        password=user_data.password,
        name=user_data.name,
        image=image
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# 2. Login de usuario
@router.post("/users/login", tags=["Users"], summary="User login")
async def login(request: LoginRequest, session: SessionDep):
    query = select(User).where(User.email == request.email)
    user_db = session.exec(query).first()

    if not user_db or user_db.password != request.password:  # Simple password comparison
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Al autenticar correctamente, se retorna el is_logged como True
    return {
        "id": user_db.id,
        "message": "Login successful",
        "is_logged": True  # Agregando is_logged a la respuesta
    }


# 3. Listar todos los usuarios
@router.get("/users", response_model=List[User], tags=["Users"], summary="List all users")
async def list_users(session: SessionDep):
    return session.exec(select(User)).all()


# 4. Obtener usuario por ID
@router.get("/users/{user_id}", response_model=User, tags=["Users"], summary="Get user by ID")
async def read_user(user_id: int, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
    return user_db


# 5. Actualizar usuario por ID
@router.patch("/users/{user_id}", response_model=User, tags=["Users"], summary="Update user by ID")
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


# 6. Eliminar un usuario por ID
@router.delete("/users/{user_id}", tags=["Users"], summary="Delete user")
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
