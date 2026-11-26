from fastapi import FastAPI
from routers import books, authors

app = FastAPI(title="API REST - Biblioteca")

app.include_router(
    books.router,
    prefix = "/books",
    tags=["Libros"]
)

app.include_router(
    authors.router,
    prefix="/authors",
    tags=["Autores"]
)

# GET http://127.0.0.1:8000/
@app.get("/")
def welcome():
    return {"mensaje": "Bienvenido a la API de la Biblioteca"}