from fastapi import FastAPI
from routers import products, users

#Le podemos indicar el titulo del doc mediante la propiedad title
app = FastAPI(title="Repaso Routers")

app.include_router(
    users.router,
    #Agrega automaticamente el /users delante de todas las rutas definidas en el archivo
    prefix = "/users",
    #Agrupa visualmente todos los endpoints del archivo bajo una seccion etiquetada como Usuarios
    tags = ["Usuarios"]
)

app.include_router(
    products.router,
    prefix = "/products",
    tags = ["Productos"]
)

#Endpoint general directamente en la aplicacion principal para comprobar que el servidor esta activo
@app.get("/")
def beginning():
    return {"mensaje": "API Rest con routers"}