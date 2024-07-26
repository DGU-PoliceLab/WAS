from typing import Optional
from pydantic import BaseModel

class LocationCreateModel(BaseModel):
    name: str
    cctv: int
    
class LocationCheckModel(BaseModel):
    name: str

class LocationUpdateModel(BaseModel):
    target: int
    name: str
    cctv: int

class LocationDeleteModel(BaseModel):
    target: int