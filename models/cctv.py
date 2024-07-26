from pydantic import BaseModel

class CctvCreateModel(BaseModel):
    name: str
    url: str
class CctvCheckModel(BaseModel):
    name: str

class CctvUpdateModel(BaseModel):
    target: int
    name: str
    url: str

class CctvDeleteModel(BaseModel):
    target: int