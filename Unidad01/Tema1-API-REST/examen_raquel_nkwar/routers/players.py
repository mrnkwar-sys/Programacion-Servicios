from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class PlayerCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    goals: int = Field(gt=0)
    
class Player(PlayerCreate):
    id: int

class PlayerPatch(BaseModel):
    id: int | None = None
    name: str | None = None
    age: int | None = Field(default=None, gt=0)
    goals: int | None = Field(default=None, gt=0)
    
players_list = [
    Player(id=1, name="Hugo", age=23, goals=12),
    Player(id=2, name="Alex", age=20, goals=4),
    Player(id=3, name="Leo", age=27, goals=15),
    Player(id=4, name="Noah", age=19, goals=1),
    Player(id=5, name="Marc", age=25, goals=8)
]

@router.get("")
def players():
    return players_list;

@router.get("/above-average")
def above_average():
    total_goals = 0
    players_above_average = []
    
    for player in players_list:
        total_goals += player.goals
    
    average_goals = total_goals / len(players_list)
        
    for player in players_list:
        if player.goals > average_goals:
            players_above_average.append(player.name)
            
    return players_above_average

@router.get("/{id}")
def get_player(id: int):
    for player in players_list:
        if player.id == id:
            return player
        
    raise HTTPException(
        status_code=404,
        detail="Player not found"
    )
    
@router.post("", status_code=201, response_model=Player)
def create_player(player: PlayerCreate):
    next_id = max(
        (player.id for player in players_list),
        default=0
    ) + 1
    
    new_player = Player(
        id = next_id,
        **player.model_dump()
    )
    
    players_list.append(new_player)
    
    return new_player

@router.put("/{id}")
def replace_player(id: int, data: PlayerCreate):
    for position, player in enumerate(players_list):
        if player.id == id:
            altered_player = Player(
                id=id,
                **data.model_dump()
            )
            
            players_list[position] = altered_player
            
            return altered_player
    
    raise HTTPException(
        status_code=404,
        detail="Player not found"
    )
    
@router.patch("/{id}")
def alter_player(id: int, data: PlayerPatch):
    for position, player in enumerate(players_list):
        if player.id == id:
            changes = data.model_dump(
                exclude_unset=True,
                exclude_none=True
            )
            
            updated_data = player.model_dump()
            
            updated_data.update(changes)
            
            updated_player = Player(**updated_data)
            
            players_list[position] = updated_player
            
            return updated_player
    
    raise HTTPException(
        status_code=404,
        detail="Player not found"
    ) 
            
@router.delete("/{id}")
def delete_player(id: int):
    for player in players_list: 
        if player.id == id:
            players_list.remove(player)
            
            return {}  
        
    raise HTTPException(
        status_code=404,
        detail="Player not found"
    )          