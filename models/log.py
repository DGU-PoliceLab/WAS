from typing import Optional
from pydantic import BaseModel

class LogReadModel(BaseModel):
    datetime: Optional[list] = []
    locations: Optional[list] = []
    types: Optional[list] = []