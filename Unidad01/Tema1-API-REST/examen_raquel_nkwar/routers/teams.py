from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class TeamCreate(BaseModel):
    name: str
    city: str
    
class Team(TeamCreate):
    id: int

teams_list = [
    Team(id=1, name="Lions", city="Seville"),
    Team(id=2, name="Eagles", city="Madrid"),
    Team(id=3, name="Wolves", city="Valencia")
]

@router.get("")
def teams():
    return teams_list;

@router.post("", status_code=201, response_model=Team)
def create_team(team: TeamCreate):
    next_id = max(
        (team.id for team in teams_list),
        default=0
    ) + 1
    
    new_team = Team(
        id = next_id,
        **team.model_dump()
    )
    
    teams_list.append(new_team)
    
    return new_team