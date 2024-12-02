from fastapi import FastAPI
from db import create_all_tables
from starlette.middleware.cors import CORSMiddleware

from .routers import user, book, vinculacion

app = FastAPI(lifespan=create_all_tables)
app.include_router(user.router)
app.include_router(book.router)
app.include_router(vinculacion.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)