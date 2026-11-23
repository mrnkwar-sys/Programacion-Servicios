from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# -------------------------------------------
# MODELOS DE DATOS
# -------------------------------------------
class UserCreate(BaseModel):
    name: str
    surname: str
    age: int = Field(ge=0, le=120)

class User(UserCreate):
    id: int

class UserPatch(BaseModel):
    name: str | None = None
    surname: str | None = None
    age: int | None = Field(default=None, ge=0, le=0)

# -------------------------------------------
# LISTA QUE SIMULA UNA BASE DE DATOS
# -------------------------------------------
users_list = [
    User(id=1, name="Paco", surname="Pérez", age=30),
    User(id=2, name="María", surname="Martínez", age=20),
    User(id=3, name="Lucía", surname="Rodríguez", age=40)
]

# -------------------------------------------
# FUNCIÓN AUXILIAR
# -------------------------------------------
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
# Devuelve todos los usuarios.
@router.get("")
def users():
    return users_list

# Busca un usuario mediante parámetro de consulta.
@router.get("/")
def get_user_query(id: int):
    return search_user(id)

# Recibe dos parámetros de consulta.
@router.get("/buscar")
def search(name: str, age: int):
    return {
        "nombre_buscado": name,
        "edad_buscada": age
    }

# Devuelve usuarios mayores que la edad indicada.
@router.get("/mayores")
def older_users(age: int):
    return [user for user in users_list if user.age > age]

# Devuelve un usuario por su ID.
@router.get("/{id}")
def get_user(id: int):
    return search_user(id)

# -------------------------------------------
# OPERACIÓN POST
# -------------------------------------------
# Crea un usuario nuevo.
@router.post("", status_code=201, response_model=User)
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
# Sustituye todos los datos editables del usuario.
@router.put("/{id}", response_model=User)
def alter_user(id: int, data: UserCreate):
    for position, user in enumerate(users_list):
        if user.id == id:
            user_altered = User(
                id = id,
                **data.model_dump()
            )

        users_list[position] = user_altered

        return user_altered

    raise HTTPException(
        status_code = 404,
        detail = "Usuario no encontrado"
    )

# -------------------------------------------
# OPERACIÓN PATCH
# -------------------------------------------
# Modifica solamente los atributos enviados.
@router.patch("/{id}", response_model = User)
def alter_user_slightly(id: int, data: UserPatch):
    for position, user in users_list:
        if user.id == id:
            changes = data.model_dump(
                exclude_unset = True,
                exclude_none = True
            )

            updated_data = user.model_dump()

            updated_data.update(changes)

            updated_user = User(
                id = id,
                **updated_data
            )

            users_list[position] = updated_user

            return updated_user
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# -------------------------------------------
# OPERACIÓN DELETE
# -------------------------------------------
# Elimina un usuario por su ID.
@router.delete("/{id}")
def delete_user(id: int):
    for position, user in enumerate(users_list):
        if user.id == id:
            users_list.pop(position)

            return {}

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )