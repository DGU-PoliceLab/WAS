from pydantic import BaseModel

class MessageModel(BaseModel):
    event: str
    location: str
    occurred_at: float
class MessageSendModel(BaseModel):
    key: str
    message: MessageModel

class MessageRecvModel(BaseModel):
    key: str