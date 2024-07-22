from typing import Optional
from pydantic import BaseModel

class RtspModel(BaseModel):
    url: Optional[str] = 0