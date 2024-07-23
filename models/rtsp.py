from typing import List
from pydantic import BaseModel

class BBox(BaseModel):
    tid: int
    bbox: List[int]

class RtspSnapModel(BaseModel):
    location: int
    url: str
    target: List[BBox]