#FastAPI es un framework para crear nuestras propias APIs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date

app = FastAPI()

#Crear un contacto sin id
class ContactCreate(BaseModel):
    name: str
    surname: str
    phoneNumber: int = Field(ge=0, le=999999999)
    birthday: date
    
#mode="before" indica que el validador se debe ejecutar antes de que Pydantic haga la conversion
@field_validator("birthday", mode="before")

#Se debe indicar que @field_validator es un classmethod
#Se puede omitir ya que se aplica automáticamente, pero la documentación recomienda escribirlo
@classmethod

#Es obligatorio escribir cls en la función por ser classmethod
#v es el valor que llega a birthday
def parse_birthday(cls, v):
    
    #Comprobamos si el valor es una cadena
    if isinstance(v, str):
        return datetime.strptime(v, "%d/%m/%Y").date()
    return v
    
#Contacto completo (con ID)
class Contact(ContactCreate):
    id: int

#Lista de contactos
contacts_list = [
    Contact(id=1, name="Paco", surname="Pérez", phoneNumber=619827019, birthday="14/09/1994"),
    Contact(id=2, name="María", surname="Martínez", phoneNumber=689028644, birthday="29/02/2006"),
    Contact(id=1, name="Lucía", surname="Rodríguez", phoneNumber=609220753, birthday="02/08/1984")
]

#Función auxiliar para buscar un contacto
def buscar_contacto(id: int):
    for contact in contacts_list:
        if contact.id == id:
            return contact
    
    #raise es la palabra clave utilizada para lanzar excepciones
    raise HTTPException(
        status_code=404,
        detail="Contacto no encontrado"
    )

#GET de todos los contactos de la lista
@app.get("/contacts")
def obtener_contactos():
    return contacts_list

#GET de un usuario dado su id
@app.get("/contacts/{id}")
def obtener_contacto(id: int):
    return buscar_contacto(id)

#GET usuario dado su nombre y numero
@app.get("/buscar")
def buscar(name: str, number: int):
    return {
        "nombre_buscado": name,
        "numero_buscado": number
    }
    
#POST nuevo contacto
@app.post("/contact", status_code=201, response_model=Contact)
def crear_contacto(contact: ContactCreate):
    
    #Cálculo del identificador
    next_id = max((c.id for c in contacts_list), default=0) + 1

    #Crear el nuevo usuario con su respectivo ID
    new_contact = Contact(
        id=next_id,
        name=contact.name,
        surname=contact.surname,
        birthday=contact.birthday
    )
    
    #Se añade a la lista de contactos
    contacts_list.append(new_contact)
    
    #Se devuelve el contacto creado
    return new_contact