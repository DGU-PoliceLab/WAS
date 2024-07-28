from typing import Optional
from pydantic import BaseModel

class EventCreateModel(BaseModel):
    e_type: str
    name: str

    class Config:
        json_schema_extra = {
            "e_type": "event type id",
            "name": "이벤트 유형 이름",
        }

class EventReadModel(BaseModel):
    target: Optional[str] = None

    class Config:
        json_schema_extra = {
            "target": None,
        }
    
class EventUpdateModel(BaseModel):
    target: int
    e_type: str
    name: str

class EventDeleteModel(BaseModel):
    target: int