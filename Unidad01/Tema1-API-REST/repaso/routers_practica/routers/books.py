from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

#Modelo con todos los campos menos el id
class BookCreate(BaseModel):
    title: str
    author: str
    pages: int = Field(gt=0)
    available: bool = True

#Modelo completo, con id incluido
class Book(BookCreate):
    id: int

#Modelo con todos los campos opcionales
class BookPatch(BaseModel):
    title: str | None = None
    author: str | None = None
    pages: int | None = Field(default=None, gt=0)
    available: bool | None = True

# -------------------------------------------
# LISTA QUE SIMULA UNA BASE DE DATOS
# -------------------------------------------
books_list = [
    Book(id=1, title="Estoy pensando en dejarlo", author="Ian Reid", pages=208, available=True),
    Book(id=2, title="El cuento de la criada", author="Margaret Atwood", pages=416, available=True),
    Book(id=3, title="Tenemos que hablar de Kevin", author="Lionel Shriver", pages=608, available=False),
]

#Funcion auxiliar para buscar un libro
def search_book(id: int):
    for book in books_list:
        if book.id == id:
            return book

    raise HTTPException(
        status_code = 404,
        detail = "Libro no encontrado"
    )

#Devuelve la lista completa de libros
@router.get("")
def books():
    return books_list

#Busca un libro recibiendo su id como parametro de consulta
@router.get("/")
def search_book_query(id: int):
    return search_book(id)

#Devuelve una lista con los libros disponibles
@router.get("/disponibles")
def available():
    return [book for book in books_list if book.available == True]

#Devuelve los libros que tengan mas paginas que el numero de paginas pasadas por parametro
#GET http://127.0.0.1:8000/books/extensos?pages=300
@router.get("/extensos")
def longer_books(pages: int):
    return [book for book in books_list if book.pages > pages]

#Busca y devuelve un libro por su parametro de ruta id
@router.get("/{id}")
def get_book(id: int):
    return search_book(id)

#Crea un nuevo libro y lo agrega a la lista
@router.post("", status_code=201, response_model=Book)
def create_book(book: BookCreate):
    next_id = max(
        (book.id for book in books_list),
        default = 0
    ) + 1

    new_book = Book(
        id = next_id,
        **book.model_dump()
    )

    books_list.append(new_book)

    return new_book

#Reemplaza todos los datos editables de un libro existente a partir de su id
@router.put("/{id}", reponse_model = Book)
def replace_book(id: int, data: BookCreate):
    for position, book in enumerate(books_list):
        if book.id == id:
            altered_book = Book(
                id = id,
                **data.model_dump()
            )

            books_list[position] = altered_book

            return altered_book

    raise HTTPException(
        status_code = 404,
        detail = "Libro no encontrado"
    )

#Actualiza parcialmente solo los campos enviados en la peticion
@router.patch("/{id}", response_model=Book)
def alter_book(id: int, data: BookPatch):
    for position, book in enumerate(books_list):
        if book.id == id:
            changes = data.model_dump(
                exclude_unset = True,
                exclude_none = True
            )

            updated_data = book.model_dump()

            updated_data.update(changes)

            updated_book = Book(**updated_data)

            books_list[position] = updated_book

            return updated_book

    raise HTTPException(
        status_code = 404,
        detail = "Libro no encontrado"
    )

#Elimina el libro correspondient al id de la lista y devuelve un diccionarion vacio
@router.delete("/{id}")
def delete_book(id: int):
    for position, book in enumerate(books_list):
        if book.id == id:
            books_list.pop(position)

            return {}

    raise HTTPException(
        status_code = 404,
        detail = "Libro no encontrado"
    )