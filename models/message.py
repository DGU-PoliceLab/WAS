from pydantic import BaseModel

class MessageSendModel(BaseModel):
    key: str
    message: dict

class MessageRecvModel(BaseModel):
    key: str