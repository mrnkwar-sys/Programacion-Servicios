from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int = Field(ge=0, le=120)

users_list = [
    User(id=1, name="Paco", surname="Pérez", age=-5),
    User(id=2, name="María", surname="Martínez", age=20),
    User(id=3, name="Lucía", surname="Rodríguez", age=40)
]

#-----ENDPOINT PARA MOSTRAR LA LISTA DE USUARIOS-----
@app.get("/users")
def users():
    return users_list

#-----ENDPOINT PARA MOSTRAR USUARIO BUSCADO POR ID-----
@app.get("/users/{id}")
def get_user(id: int):
    for user in users_list:
        if user.id == id:
            return user

    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )

#-----ENDPOINT PARA MOSTRAR USUARIOS FILTRADOS POR ID-----
'''
Un parametro de consulta en una ruta es un par clave-valor indicado tras un signo '?'
Suelen servir para filtrar datos, por ejemplo, para buscar a todos los usuarios con age >= 25
Ejemplo: http://127.0.0.1:8000/users/?id=2
'''
#Como el id no esta en la ruta, pero si en la funcion, FastAPI deduce que debe buscarlo tras el ? en la URL
@app.get("/users/")
def get_user_query(id: int):
    for user in users_list:
        if user.id == id:
            return user

    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )

#-----ENDPOINT PARA MOSTRAR USUARIOS FILTRADOS POR NOMBRE Y EDAD-----
'''
Para incluir mas de un parametro de consulta en la URL se utiliza '&'
Ejemplo: http://127.0.0.1:8000/buscar?name=Paco&age=30
'''
#La funcion no busca un usuario de la lista, sino que toma los parametros pasados al URL
# y los devuelve estructurados dentro de un diccionario de JSON
@app.get("/buscar")
def search(name: str, age: int):
    return {
        "nombre_buscado": name,
        "edad_buscada": age
    }

#-----ENDPOINT PARA MOSTRAR USUARIOS FILTRADOS POR EDAD-----
#Ejemplo: http://127.0.0.1:8000/mayores?age=25
@app.get("/mayores")
def older_users(age: int):
    #Devuelve una lista con los usuarios cuya edad supere la edad pasada por parametro
    return [user for user in users_list if user.age>age]

# Hace lo mismo:
# @app.get("/mayores")
# def usuarios_mayores(edad: int):
#     resultado = []

#     for usuario in users_list:
#         if usuario.age > edad:
#             resultado.append(usuario)

#     return resultado