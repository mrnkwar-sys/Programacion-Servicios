from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class PresentCreate(BaseModel):
    name: str
    destinatary: str
    weight: float = Field(gt=0)
    wrapped: bool
    elf_id: int


class Present(PresentCreate):
    id: int


class PresentPatch(BaseModel):
    name: str | None = None
    destinatary: str | None = None
    weight: float | None = Field(default=None, gt=0)
    wrapped: bool | None = None
    elf_id: int | None = None


presents_list = [
    Present(
        id=1, name="Name1", destinatary="Dest1", weight=1.0, wrapped=True, elf_id=1
    ),
    Present(
        id=2, name="Name2", destinatary="Dest2", weight=2.5, wrapped=False, elf_id=2
    ),
    Present(
        id=3, name="Name3", destinatary="Dest3", weight=3.0, wrapped=True, elf_id=1
    ),
]


def search_present(id: int):
    for present in presents_list:
        if present.id == id:
            return present

    raise HTTPException(status_code=404, detail="Present not found")


@router.get("")
def get_presents():
    return presents_list


@router.get("/buscar")
def wrapped_presents(wrapped: bool):
    return [present for present in presents_list if present.wrapped == wrapped]


@router.get("/{id}")
def get_present_by_id(id: int):
    return search_present(id)


@router.post("", status_code=201, response_model=Present)
def create_present(present: PresentCreate):
    next_id = max((present.id for present in presents_list), default=0) + 1

    new_present = Present(
        id=next_id,
        name=present.name,
        destinatary=present.destinatary,
        weight=present.weight,
        wrapped=present.wrapped,
        elf_id=present.elf_id,
    )

    presents_list.append(new_present)
    return new_present


@router.put("/{id}", response_model=Present)
def modify_present(id: int, data: PresentCreate):
    for position, present in enumerate(presents_list):
        if present.id == id:
            modified_present = Present(
                id=id,
                name=data.name,
                destinatary=data.destinatary,
                weight=data.weight,
                wrapped=data.wrapped,
                elf_id=data.elf_id,
            )
            presents_list[position] = modified_present
            return modified_present

    raise HTTPException(status_code=404, detail="Present not found")


@router.patch("/{id}", response_model=Present)
def patch_present(id: int, data: PresentPatch):
    for position, present in enumerate(presents_list):
        if present.id == id:
            changes = data.model_dump(
                exclude_unset=True,
                exclude_none=True,
            )
            data_updated = present.model_dump()
            data_updated.update(changes)
            present_patched = Present(**data_updated)
            presents_list[position] = present_patched
            return present_patched

    raise HTTPException(status_code=404, detail="Present not found")


@router.delete("/{id}")
def delete_present(id: int):
    for present in presents_list:
        if present.id == id:
            presents_list.remove(present)
            return {}

    raise HTTPException(status_code=404, detail="Present not found")
