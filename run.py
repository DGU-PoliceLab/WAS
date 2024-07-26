from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
# import uvicorn
import logging
import time
from starlette.middleware.cors import CORSMiddleware
import base64
import redis.asyncio as aioredis
from db.controller import MysqlDB, RedisDB, RedisMQ
from services import cctv as Cctv
from services import event as Event
from services import location as Location
from services import rtsp as RTSP
from services import log as Log
from services import snap as Snap
from models.log import LogReadModel, LogCheckModel
from models.cctv import CctvCreateModel, CctvCheckModel, CctvUpdateModel, CctvDeleteModel
from models.location import LocationCreateModel, LocationUpdateModel, LocationDeleteModel
from models.event import EventCreateModel, EventReadModel, EventUpdateModel, EventDeleteModel
from models.message import MessageSendModel, MessageRecvModel
from models.rtsp import RtspSnapModel
from models.snap import SnapReadModel, SnapUpdateModel

app = FastAPI()
mysql = MysqlDB()
redis = RedisDB()
redis_client = aioredis.from_url("redis://localhost:50001")
mq = RedisMQ()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

origins = [
    "https://localhost",
    "https://localhost:5173",
    "http://127.0.0.1",  # 추가 가능한 도메인
    "http://127.0.0.1:5173",  # 추가 가능한 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/file/snap", StaticFiles(directory="static/snap"), name="snap")
app.mount("/file/clip", StaticFiles(directory="static/clip"), name="clip")

# Root Services
@app.get("/")
def read_root():
    return {"msg": "Server Is Working"}

# CCTV Services
@app.post('/cctv/create')
def create_cctv(option: CctvCreateModel):
    response = Cctv.create(option.name, option.url)
    return response

@app.post('/cctv/read')
def read_cctv():
    response = Cctv.read()
    return response

@app.post('/cctv/check')
def read_cctv(option: CctvCheckModel):
    response = Cctv.check(option.name)
    return response

@app.post('/cctv/update')
def update_cctv(option: CctvUpdateModel):
    response = Cctv.update(option.target, option.name, option.url)
    return response

@app.post('/cctv/delete')
def delete_cctv(option: CctvDeleteModel):
    response = Cctv.delete(option.target)
    return response

# Event Services
@app.post('/event/create')
def create_event(option: EventCreateModel):
    response = Event.create(option.e_type, option.name)
    return response

@app.post('/event/read')
def read_event(option: EventReadModel):
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
def read_location():
    response = Location.read()
    return response

@app.post('/location/read/cctv')
def read_location_cctv():
    response = Location.read_with_cctv()
    return response

@app.post('/location/update')
def update_location(option: LocationUpdateModel):
    response = Location.update(option.target, option.name, option.cctv)
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

@app.post('/log/read/limit')
def read_log(option: LogReadModel):
    response = Log.readLimit(option.datetime, option.locations, option.types)
    return response


@app.post('/log/check')
def read_log(option: LogCheckModel):
    response = Log.check(option.target)
    return response

# Message Services
@app.post('/message/send')
def message_send(option: MessageSendModel):
    response = mq.send(option.key, option.message)
    return response

@app.post('/message/recv')
def message_send(option: MessageRecvModel):
    response = mq.recv(option.key)
    return response

@app.post('/message/live')
def message_live():
    response = mq.live()
    return response

# RTSP Services
@app.get("/rtsp")
def stream_rtsp(url: str):
    url_bytes = url.encode('ascii')
    decoded = base64.b64decode(url_bytes)
    str_url = decoded.decode('UTF-8')
    return StreamingResponse(RTSP.getRtspStream(str_url), media_type="multipart/x-mixed-replace; boundary=PNPframe")

@app.post("/rtsp/snap")
def stream_rtsp(option: RtspSnapModel):
    response = RTSP.snapshot(option.location, option.url, option.target)
    return response

# Snap Services
@app.post("/snap/read")
def stream_rtsp(option: SnapReadModel):
    response = Snap.read(option.target)
    return response

@app.post("/snap/update")
def stream_rtsp(option: SnapUpdateModel):
    response = Snap.update(option.target, option.url, option.data)
    return response

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