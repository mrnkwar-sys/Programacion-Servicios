from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class Author(BaseModel):
    id: int
    name: str
    country: str

author_list = [
    Author(id=1, name="Ian Reid", country="Canada"),
    Author(id=2, name="Margaret Atwood", country="USA"),
    Author(id=3, name="Lionel Shriver", country="USA")
]

#Devuelve la lista con todos los autores
@router.get("")
def authors():
    return author_list

@router.get("/{id}")
def get_author(id: int):
    for author in author_list:
        if author.id == id:
            return author

    raise HTTPException(
        status_code = 404,
        detail = "Autor no encontrado"
    )