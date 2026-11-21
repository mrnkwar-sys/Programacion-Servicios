#Comando de terminal para arrancar el servidor
#.\.venv\Scripts\fastapi.exe dev Tema1-API-REST/repaso_todo.py

#Importa FastAPI para poder crear la aplicacion web
from fastapi import FastAPI

#Variable que guarda la instancia de la aplicacion.
#Sobre ella se cofiguran las rutas
app = FastAPI()

#------PRIMER ENDPOINT------
'''
@app.get("/") es un decorador que le dice a FastAPI que la funcion que esta
justo debajo debe ejecutarse cuando alguien haga una peticion
HTTP de tipo GET a la ruta raiz ("/")
'''
@app.get("/")
def root():
    #Devuelve un diccionario que FastAPI convierte a JSON antes de enviarlo como respuesta al cliente/navegador
    return {"Hello": "World"}

#------SEGUNDO ENDPOINT------
#Otra ruta GET que incluye una variable dinamica entre llaves
@app.get("/saludo/{nombre}")
#Recibe como argumento el parametro de la URL
def saludar(nombre: str):
    #Devuelve el resultado en un diccionario que se pasara a JSON
    return {"saludo": "Hola " + nombre}
    #return {"saludo": f"Hola, {nombre}"} Otra forma de concatenar