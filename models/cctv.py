from pydantic import BaseModel

class CctvCreateModel(BaseModel):
    name: str
    url: str

    class Config:
        json_schema_extra = {
            "name": "테스트",
            "url": "rtsp://"
        }

class CctvCheckModel(BaseModel):
    name: str
    class Config:
        json_schema_extra = {
            "name": "테스트",
        }

class CctvUpdateModel(BaseModel):
    target: int
    name: str
    url: str

    class Config:
        json_schema_extra = {
            "target": 1,
            "name": "테스트",
            "url": "rtsp://"
        }

class CctvDeleteModel(BaseModel):
    target: int

    class Config:
        json_schema_extra = {
            "target": 1,
        }