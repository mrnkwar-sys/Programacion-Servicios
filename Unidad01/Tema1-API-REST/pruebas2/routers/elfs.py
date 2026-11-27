from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from routers.presents import Present, presents_list

router = APIRouter()


class Elf(BaseModel):
    id: int
    name: str
    turn: str
    manufactured_toys: int = Field(ge=0)


class PresentNestedCreate(BaseModel):
    name: str
    destinatary: str
    weight: float = Field(gt=0)
    wrapped: bool


elfs_list = [
    Elf(id=1, name="Name1", turn="morning", manufactured_toys=10),
    Elf(id=2, name="Name2", turn="afternoon", manufactured_toys=65),
    Elf(id=3, name="Name3", turn="night", manufactured_toys=40),
]


def search_elf(id: int):
    for elf in elfs_list:
        if elf.id == id:
            return elf

    raise HTTPException(status_code=404, detail="Elf not found")


@router.get("")
def get_elfs():
    return elfs_list


@router.get("/notable")
def notable_elfs(min: int):
    return [elf for elf in elfs_list if elf.manufactured_toys > min]


@router.get("/by-turn")
def get_elfs_by_turn(turn: str):
    return [elf for elf in elfs_list if elf.turn == turn]


@router.get("/{id}")
def get_elf_by_id(id: int):
    return search_elf(id)


# -------------------------------------------
# PETICIONES ANIDADAS (REGALOS DE UN ELFO)
# -------------------------------------------


@router.get("/{id}/presents", response_model=list[Present])
def get_presents_by_elf(id: int):
    search_elf(id)
    return [present for present in presents_list if present.elf_id == id]


@router.post("/{id}/presents", status_code=201, response_model=Present)
def create_present_for_elf(id: int, present: PresentNestedCreate):
    search_elf(id)

    next_id = max((present.id for present in presents_list), default=0) + 1

    new_present = Present(
        id=next_id,
        name=present.name,
        destinatary=present.destinatary,
        weight=present.weight,
        wrapped=present.wrapped,
        elf_id=id,
    )

    presents_list.append(new_present)
    return new_present
