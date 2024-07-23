from typing import List
from pydantic import BaseModel

class SnapModel(BaseModel):
    tid: int
    thumb: str
    bbox: List[int]
    heart: int
    breath: int
    temp: float
    emotion: int

class SnapReadModel(BaseModel):
    target: str

class SnapUpdateModel(BaseModel):
    target: str
    url: str
    data: List[SnapModel]