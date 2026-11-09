from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, date

router = APIRouter()

class ContactCreate(BaseModel):
    id: int
    name: str
    birthdate: date

class Contact(ContactCreate):
    id: int
    
class ContactPatch(BaseModel):
    name: str | None = None
    birthdate: date | None = None
    
contacts_list = [
    Contact(id=1, name="Paco", birthdate="1994-09-14"),
    Contact(id=2, name="Ana", birthdate="1990-03-22"),
    Contact(id=3, name="Lucía", birthdate="1984-08-02")
]

def buscar_contacto(id: int):
    for contact in contacts_list:
        if contact.id == id:
            return contact

    raise HTTPException(
        status_code=404,
        detail="Contacto no encontrado"
    )

# Devuelve todos los contactos.
@router.get("")
def obtener_contactos():
    return contacts_list

# Busca un contacto mediante parámetro de consulta.
@router.get("/")
def obtener_contacto_query(id: int):
    return buscar_contacto(id)

# Recibe dos parámetros de consulta.
@router.get("/buscar")
def buscar(nombre: str, cumple: date):
    return {
        "nombre_buscado": nombre,
        "cumpleaños_buscado": cumple
    }

# Devuelve un contacto por su ID.
@router.get("/{id}")
def obtener_contacto(id: int):
    return buscar_contacto(id)

# Crea un contacto nuevo.
@router.post("", status_code=201, response_model=Contact)
def crear_contacto(contacto: ContactCreate):

    siguiente_id = max(
        (c.id for c in contacts_list),
        default=0
    ) + 1

    nuevo_contacto = Contact(
        id=siguiente_id,
        name=contacto.name,
        birthdate=contacto.birthdate
    )

    # Alternativa:
    # nuevo_contacto = Contact(
    #     id=siguiente_id,
    #     **contacto.model_dump()
    # )

    contacts_list.append(nuevo_contacto)

    return nuevo_contacto

# Sustituye todos los datos editables del contacto.
@router.put("/{id}", response_model=Contact)
def modificar_contacto(id: int, datos: ContactCreate):

    for posicion, contacto in enumerate(contacts_list):

        if contacto.id == id:

            contacto_modificado = Contact(
                id=id,
                name=datos.name,
                birthdate=datos.birthdate
            )

            # Alternativa:
            # contacto_modificado = Contact(
            #     id=id,
            #     **datos.model_dump()
            # )

            contacts_list[posicion] = contacto_modificado

            return contacto_modificado

    raise HTTPException(
        status_code=404,
        detail="Contacto no encontrado"
    )
    
# Modifica solamente los atributos enviados.
@router.patch("/{id}", response_model=Contact)
def modificar_contacto_parcial(id: int, datos: ContactPatch):

    for posicion, contacto in enumerate(contacts_list):

        if contacto.id == id:

            cambios = datos.model_dump(
                exclude_unset=True,
                exclude_none=True
            )

            datos_actualizados = contacto.model_dump()

            datos_actualizados.update(cambios)

            contacto_modificado = Contact(
                **datos_actualizados
            )

            contacts_list[posicion] = contacto_modificado

            return contacto_modificado

    raise HTTPException(
        status_code=404,
        detail="Contacto no encontrado"
    )

# Elimina un contacto por su ID.
@router.delete("/{id}")
def eliminar_contacto(id: int):

    for contacto in contacts_list:

        if contacto.id == id:

            # Eliminamos directamente el objeto.
            contacts_list.remove(contacto)

            return {}

    raise HTTPException(
        status_code=404,
        detail="Contacto no encontrado"
    )