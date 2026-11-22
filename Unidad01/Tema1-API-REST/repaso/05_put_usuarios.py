from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    surname: str
    age: int = Field(ge=0, le=120)

class User(UserCreate):
    id: int

users_list = [
    User(id=1, name="Paco", surname="Pérez", age=30),
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

# -------------------------------------------
# OPERACIONES GET
# -------------------------------------------
@app.get("/")
def users():
    return users_list

@app.get("/users/{id}")
def get_user(id: int):
    return search_user(id)

@app.get("/users/")
def get_user_query(id: int):
    return search_user(id)

@app.get("/buscar")
def search(name: str, age: int):
    return {
        "nombre_buscado": name,
        "edad_buscada": age
    }

@app.get("/mayores")
def older_users(age: int):
    return [user for user in users_list if user.age > age]

# -------------------------------------------
# OPERACIÓN POST
# -------------------------------------------
@app.post("/users", status_code = 201, response_model = User)
def create_user(user: UserCreate):
    next_id = max(
        (user.id for user in users_list),
        default=0
    ) + 1

    new_user = User(
        id = next_id,
        **user.model_dump()
    )

    users_list.append(new_user)

    return new_user

# -------------------------------------------
# OPERACIÓN PUT
# -------------------------------------------
#Modifica por completo la informaccion de un usuario
@app.put("/users", response_model = User)
def alter_user(id: int, data: UserCreate):
    #Recorremos la lista de usuarios hasta encontrar el id solicitado
    #Necesitaremos la posicion del usuario para poder sustituirlo mas adelante
    for position, user in enumerate(users_list):
        #Si el id coincide, creamos un nuevo usuario con la nueva informacion
        if user.id == id:
            altered_user = User(
                id = id,
                **data.model_dump()
            )

            #Sustituye el usuario que ocupada esa posicion con la nueva informacion
            users_list[position] = altered_user

            #Devuelve el usuario modificado
            return altered_user

    #Error si el usuario no existe
    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )