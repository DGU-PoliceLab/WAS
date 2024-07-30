from typing import List
from pydantic import BaseModel

class SnapModel(BaseModel):
    tid: int
    thumb: str
    heart: int
    breath: int
    temp: float
    emotion: int

class SnapReadModel(BaseModel):
    target: str

class SnapUpdateModel(BaseModel):
    target: str
    data: List[SnapModel]