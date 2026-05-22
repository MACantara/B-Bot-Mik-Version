from pydantic import BaseModel
from typing import List, Literal


class CellState(BaseModel):
    type: Literal["EMPTY", "TREE", "ROCK", "HOUSE"]
    id: str


class BotState(BaseModel):
    x: int
    y: int
    direction: Literal["UP", "DOWN", "LEFT", "RIGHT"]
    inventory: dict


class SimulationState(BaseModel):
    grid: List[List[CellState]]
    bot: BotState
    population: int


class SaveStateCreate(BaseModel):
    grid_json: List[List[CellState]]
    wood_count: int
    stone_count: int
    population_count: int


class SaveStateResponse(BaseModel):
    id: int
    user_id: int
    grid_json: List[List[CellState]]
    wood_count: int
    stone_count: int
    population_count: int

    class Config:
        from_attributes = True
