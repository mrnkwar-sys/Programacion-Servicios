from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class Product(BaseModel):
    id: int
    name: str
    #gt significa greater than
    price: float = Field(gt=0)

products_list = [
    Product(id=1, name="Teclado", price=25.50),
    Product(id=2, name="Ratón", price=15.99),
    Product(id=3, name="Monitor", price=189.90)
]

# Devuelve todos los productos.
@router.get("")
def products():
    return products_list

# Devuelve un producto por su ID.
@router.get("/{id}")
def get_product(id: int):
    for product in products_list:
        if product.id == id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado"
    )