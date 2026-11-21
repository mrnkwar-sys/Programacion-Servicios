from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

#Variable que guarda la instancia de la aplicacion.
#Sobre ella se cofiguran las rutas
app = FastAPI()

#Define la clase usuario
#User hereda de BaseModel, definiendo la estructura que debe tener cada usuario
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int = Field(ge=0, le=120)

#Lista de usuarios que simula la base de datos
users_list = [
    User(id=1, name="Paco", surname="Pérez", age=-5),
    User(id=2, name="María", surname="Martínez", age=20),
    User(id=3, name="Lucía", surname="Rodríguez", age=40)
]

#-----ENDPOINT PARA MOSTRAR LA LISTA DE USUARIOS-----
@app.get("/users")
def user():
    return users_list

#-----ENDPOINT PARA MOSTRAR USUARIO BUSCADO POR ID-----
#Ruta GET que incluye una variable dinamica entre llaves
@app.get("/user/{id}")
def get_user(id: int):
    #Recorre la lista de usuarios para encontrar a uno con el mismo id que el pasado como parametro
    for user in users_list:
        if user.id == id:
            return user
        
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )