from typing import Optional
from pydantic import BaseModel

class EventCreateModel(BaseModel):
    e_type: str
    name: str

class EventReadModel(BaseModel):
    target: Optional[str] = None
    
class EventUpdateModel(BaseModel):
    target: int
    e_type: str
    name: str

class EventDeleteModel(BaseModel):
    target: int