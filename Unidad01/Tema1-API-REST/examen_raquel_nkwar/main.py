from fastapi import FastAPI
from routers import players, teams

app = FastAPI(title="API de Jugadores y Equipos")

app.include_router(
    players.router,
    prefix = "/players",
    tags=["Players"]
)

app.include_router(
    teams.router,
    prefix="/teams",
    tags=["Teams"]
)

@app.get("/")
def welcome():
    return {"mensaje": "Bienvenido a la API de la Jugadores y Equipos"}