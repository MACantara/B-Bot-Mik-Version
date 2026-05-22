from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import supabase
from app.core.security import decode_token
from app.schemas.simulation import SimulationState, SaveStateCreate, SaveStateResponse, CellState, BotState
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    return user_id


@router.get("/state", response_model=SimulationState)
def get_simulation_state():
    """Returns the demo 10x10 grid configuration"""
    # Create a demo 10x10 grid with some trees, rocks, and empty spaces
    demo_grid: List[List[CellState]] = []
    for y in range(10):
        row: List[CellState] = []
        for x in range(10):
            if (x, y) in [(2, 3), (5, 7), (8, 2), (1, 8), (6, 4)]:
                cell = CellState(type="TREE", id=f"{x}-{y}")
            elif (x, y) in [(3, 1), (7, 5), (4, 8), (9, 3), (2, 6)]:
                cell = CellState(type="ROCK", id=f"{x}-{y}")
            else:
                cell = CellState(type="EMPTY", id=f"{x}-{y}")
            row.append(cell)
        demo_grid.append(row)
    
    bot_state = BotState(
        x=0,
        y=0,
        direction="RIGHT",
        inventory={"wood": 0, "stone": 0}
    )
    
    return SimulationState(
        grid=demo_grid,
        bot=bot_state,
        population=0
    )


@router.post("/save", response_model=SaveStateResponse)
def save_simulation_state(
    save_data: SaveStateCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Persists the player's layout progress and resource tallies"""
    # Check if user already has a save state
    response = supabase.table("save_states").select("*").eq("user_id", user_id).execute()
    
    save_state_data = {
        "user_id": user_id,
        "grid_json": save_data.grid_json,
        "wood_count": save_data.wood_count,
        "stone_count": save_data.stone_count,
        "population_count": save_data.population_count
    }
    
    if response.data:
        # Update existing save
        result = supabase.table("save_states").update(save_state_data).eq("id", response.data[0]["id"]).execute()
        return result.data[0]
    else:
        # Create new save
        result = supabase.table("save_states").insert(save_state_data).execute()
        return result.data[0]


@router.get("/save", response_model=SaveStateResponse)
def get_simulation_state(
    user_id: str = Depends(get_current_user_id)
):
    """Retrieves the user's saved simulation state"""
    response = supabase.table("save_states").select("*").eq("user_id", user_id).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No save state found for this user"
        )
    return response.data[0]
