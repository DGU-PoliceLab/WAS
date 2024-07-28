from typing import Optional, List
from pydantic import BaseModel

class LogReadModel(BaseModel):
    datetime: Optional[List[str]] = []
    locations: Optional[List[str]] = []
    types: Optional[List[str]] = []


class LogCheckModel(BaseModel):
    target: int