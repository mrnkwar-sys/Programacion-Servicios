from fastapi import FastAPI
from routers import contacts, tasks

#Creamos la aplicación principal.
app = FastAPI(title="Ejemplo 08 - Routers Contacts y Tasks")

#Incorporamos los routers a nuestra aplicación.
app.include_router(
    contacts.router,
    prefix="/contacts",
    tags=["Contactos"]
)

app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tareas"]
)

@app.get("/")
def inicio():
    return {"mensaje": "API REST con routers"}