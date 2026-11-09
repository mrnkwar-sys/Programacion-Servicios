from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import date

router = APIRouter()

class Task(BaseModel):
    id: int
    title: str
    begin_date: date | None = None
    end_date: date | None = None

# Lista de tareas   
tasks_list = [
    Task(id=1, title="Tarea 1", begin_date="2026-11-01", end_date="2026-11-10"),
    Task(id=2, title="Tarea 2", begin_date="2026-11-05", end_date="2026-11-15"),
    Task(id=3, title="Tarea 3", begin_date="2026-11-10", end_date="2026-11-20")
]

# Devuelve todas las tareas.
@router.get("")
def obtener_tareas():
    return tasks_list

#Devuelve una tarea por su ID.
@router.get("/{id}")
def obtener_tarea(id: int):

    for tarea in tasks_list:
        if tarea.id == id:
            return tarea

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )