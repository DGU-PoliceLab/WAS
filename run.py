from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
# import uvicorn
import time
from starlette.middleware.cors import CORSMiddleware
import base64
import asyncio
import redis.asyncio as aioredis
from db.controller import MysqlDB, RedisDB, RedisMQ
from services import cctv as Cctv
from services import event as Event
from services import location as Location
from services import log as Log
from models.log import LogReadModel
from models.cctv import CctvCreateModel, CctvUpdateModel, CctvDeleteModel
from models.location import LocationCreateModel, LocationReadModel, LocationUpdateModel, LocationDeleteModel
from models.event import EventCreateModel, EventReadModel, EventUpdateModel, EventDeleteModel
from models.message import MessageSendModel, MessageRecvModel
from models.rtsp import RtspModel
from utils.stream import getRtspStream

app = FastAPI()
mysql = MysqlDB()
redis = RedisDB()
redis_client = aioredis.from_url("redis://localhost:50001")
mq = RedisMQ()

origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Service
@app.get("/")
def read_root():
    return {"msg": "Server Is Working"}

# CCTV Service
@app.post('/cctv/create')
def create_cctv(option: CctvCreateModel):
    response = Cctv.create(option.name, option.url)
    return response

@app.post('/cctv/read')
def read_cctv():
    response = Cctv.read()
    return response

@app.post('/cctv/update')
def update_cctv(option: CctvUpdateModel):
    response = Cctv.update(option.target, option.name, option.url)
    return response

@app.post('/cctv/delete')
def delete_cctv(option: CctvDeleteModel):
    print(option.target, type(option.target))
    response = Cctv.delete(option.target)
    return response

# Event Services
@app.post('/event/create')
def create_event(option: EventCreateModel):
    response = Event.create(option.e_type, option.name)
    return response

@app.post('/event/read')
def read_event(option: EventReadModel):
    print(option.target, type(option.target))
    response = Event.read(option.target)
    return response

@app.post('/event/update')
def update_event(option: EventUpdateModel):
    response = Event.update(option.target, option.e_type, option.name)
    return response

@app.post('/event/delete')
def delete_event(option: EventDeleteModel):
    response = Event.delete(option.target)
    return response

# Location Services
@app.post('/location/create')
def create_location(option: LocationCreateModel):
    response = Location.create(option.name, option.cctv)
    return response

@app.post('/location/read')
def read_location(option: LocationReadModel):
    print(option.target, type(option.target))
    response = Location.read(option.target)
    return response

@app.post('/location/update')
def update_location(option: LocationUpdateModel):
    response = Location.update(option.target, option.name, option.url)
    return response

@app.post('/location/delete')
def delete_location(option: LocationDeleteModel):
    response = Location.delete(option.target)
    return response

# Log Services
@app.post('/log/read')
def read_log(option: LogReadModel):
    response = Log.read(option.datetime, option.locations, option.types)
    return response

# Message Service
@app.post('/message/send')
def message_send(option:MessageSendModel):
    response = mq.send(option.key, option.message)
    return response

@app.post('/message/send')
def message_send(option:MessageRecvModel):
    response = mq.recv(option.key)
    return response

# RTSP Services
@app.get("/rtsp")
def stream_rtsp(url: str):
    url_bytes = url.encode('ascii')
    decoded = base64.b64decode(url_bytes)
    str_url = decoded.decode('UTF-8')
    print(str_url)
    return StreamingResponse(getRtspStream(str_url), media_type="multipart/x-mixed-replace; boundary=PNPframe")

# Message Services
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         # Redis에서 데이터 가져오는 예제 (실시간 데이터 구독)
#         pubsub = redis_client.pubsub()
#         await pubsub.subscribe("realtime_data_channel")

#         while True:
#             message = await pubsub.get_message(ignore_subscribe_messages=True)
#             if message:
#                 await websocket.send_text(message["data"].decode('utf-8'))
#             await asyncio.sleep(1)
#     except Exception as e:
#         print(f"Connection error: {e}")
#     finally:
#         await pubsub.unsubscribe("realtime_data_channel")
#         await websocket.close()