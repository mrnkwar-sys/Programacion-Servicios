from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Modelo para crear o sustituir usuarios.
class UserCreate(BaseModel):
    name: str
    surname: str
    age: int = Field(ge=0, le=120)

#Modelo del usuario completo, incluido su id
class User(UserCreate):
    id: int

#Modelo para modificaciones parciales (PATCH)
#Todos los atributos son opcionales para que el usuario pueda elegir que datos cambiar y cuales no
#Si no se envian, valdran None por defecto
class UserPatch(BaseModel):
    name: str | None = None
    surname: str | None = None
    age: int | None = Field(default = None, ge=0, le=120)

# -------------------------------------------
# LISTA QUE SIMULA UNA BASE DE DATOS
# -------------------------------------------

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
# Crea un usuario nuevo.
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
@app.put("/users", response_model = User)
def alter_user(id: int, data: UserCreate):
    for position, user in enumerate(users_list):
        if user.id == id:
            altered_user = User(
                id = id,
                **data.model_dump()
            )

            users_list[position] = altered_user

            return altered_user

    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )

# -------------------------------------------
# OPERACIÓN PATCH
# -------------------------------------------
# Modifica solamente los atributos enviados.
@app.patch("/users/{id}", response_model = User)
def alter_user_slightly(id: int, data: UserCreate):
    for position, user in users_list:
        if user.id == id:
            changes = data.model_dump(
                exclude_unset = True,
                exclude_none = True
            )

            data_updated = user.model_dump()

            data_updated.update(changes)

            user_updated = User(**data_updated)

            users_list[position] = user_updated

            return user_updated

    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )

# -------------------------------------------
# OPERACIÓN DELETE - NUEVA
# -------------------------------------------
# Elimina un usuario existente mediante su ID.
@app.delete("/users/{id}")
def delete_user(id: int):
    for position, user in enumerate(users_list):
        if user.id == id:
            #.pop() permite eliminar un par clave-valor de un diccionario al pasarle la clave
            users_list.pop(position)

            #Devuelve un diccionario vacio
            return {}

    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )