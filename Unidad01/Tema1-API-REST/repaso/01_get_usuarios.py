from fastapi import FastAPI
#BaseModel sirve para crear modelos de datos validos y convertibles a JSON
from pydantic import BaseModel
#Field permite anadir reglas de validacion mas especificas
#from pydantic import BaseModel, Field

#Variable que guarda la instancia de la aplicacion.
#Sobre ella se cofiguran las rutas
app = FastAPI()

#Define la clase usuario
#User hereda de BaseModel, definiendo la estructura que debe tener cada usuario
class User(BaseModel):
    name: str
    surname: str
    age: int
    #Field permitiria restringir la edad para que sea >= 0 y <= 120
    #age: int = Field(ge=0, le=120)

#Lista de usuarios que simula la base de datos
user_list = [
    User(name="Paco", surname="Pérez", age=-5),
    User(name="María", surname="Martínez", age=20),
    User(name="Lucía", surname="Rodríguez", age=40)
]

#------ENDPOINT-----
@app.get("/users")
def user():
    #Gracias a BaseModel, FastAPI convierte automaticamente los objetos User en una lista de objetos JSON
    return user_list