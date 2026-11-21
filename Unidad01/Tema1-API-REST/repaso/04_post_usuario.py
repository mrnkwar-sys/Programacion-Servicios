from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

#Modelo para crear usuario sin id
class UserCreate(BaseModel):
    name: str
    surname: str
    age: int = Field(ge=0, le=120)

#Modelo para crear usuario completo (hereda de UserCreate, por lo que ya tiene los demas atributos)
class User(UserCreate):
    id: int

users_list = [
    User(id=1, name="Paco", surname="Pérez", age=-5),
    User(id=2, name="María", surname="Martínez", age=20),
    User(id=3, name="Lucía", surname="Rodríguez", age=40)
]

#Funcion auxiliar para buscar un usuario por su id
def search_user(id: int):
    for user in users_list:
        if user.id == id:
            return user
    
    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )

#-----ENDPOINT PARA MOSTRAR LA LISTA DE USUARIOS-----
@app.get("/users")
def users():
    return users_list

#-----ENDPOINT PARA MOSTRAR USUARIO BUSCADO POR ID-----
@app.get("/users/{id}")
def get_user(id: int):
    return search_user(id)

#-----ENDPOINT PARA MOSTRAR USUARIOS FILTRADOS POR ID-----
@app.get("/users/")
def get_user_query(id: int):
    return search_user(id)

#-----ENDPOINT PARA MOSTRAR USUARIOS FILTRADOS POR NOMBRE Y EDAD-----
@app.get("/buscar")
def search(name: str, age: int):
    return {
        "nombre_buscado": name,
        "edad_buscada": age
    }

#-----ENDPOINT PARA MOSTRAR USUARIOS FILTRADOS POR EDAD-----
@app.get("/mayores")
def older_users(age: int):
    return [user for user in users_list if user.age > age]

@app.post("/users", status_code = 201, response_model = User)
#El cliente envia en la peticion el nombre, apellido y edad del usuario (modelo UserCreate)
def create_user(user: UserCreate):
    # Calculamos el siguiente id
    #Busca y devuelve el id mas alto de todos los ids devueltos en el for
    next_id = max(
        #Guarda unicamente los ids de los usuarios de la lista
        (u.id for u in users_list),
        #Medida de seguridad para que, si la lista esta vacia, se asuma que el valor maximo es 0
        default=0
    #Le suma 1 al resultado de max()
    ) + 1

    #Se crea al nuevo usuario con los datos del usuario pasado por parametro
    new_user = User (
        id = next_id,
        name = user.name,
        surname = user.surname,
        age = user.age
    )

    #De otra forma:
    # new_user = User(
    #   id = next_id,
    '''
    model_dump es un metodo de BaseModel que convierte un objeto en un diccionario estandar de Python
    Los dos astericos indican a Python que "abra" el diccionario y pase cada pareja clave-valor como si fueran argumentos
    '''
    #   **user.model_dump()
    # )

    #Se anade el usuario a la lista ("base de datos")
    users_list.append(new_user)

    #Devuelve el usuario creado
    return new_user