from typing import Optional
from pydantic import BaseModel

class LocationCreateModel(BaseModel):
    name: str
    cctv: str

class LocationReadModel(BaseModel):
    target: Optional[str] = None
    
class LocationUpdateModel(BaseModel):
    target: int
    name: str
    url: str

class LocationDeleteModel(BaseModel):
    target: int