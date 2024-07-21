from fastapi import FastAPI
from db.controller import MysqlDB, RedisDB, RedisMQ
from services import cctv as Cctv
from services import event as Event
from services import location as Location
from services import log as Log
from models.log import LogReadModel
from models.cctv import CctvCreateModel, CctvUpdateModel, CctvDeleteModel
from models.location import LocationCreateModel, LocationReadModel, LocationUpdateModel, LocationDeleteModel
from models.event import EventCreateModel, EventReadModel, EventUpdateModel, EventDeleteModel

app = FastAPI()
mysql = MysqlDB()
redis = RedisDB()
mq = RedisMQ()

# Root Service
@app.get("/")
def read_root():
    return {"msg": "Server Is Working"}

# CCTV Service
@app.post('/cctv/create')
def create_cctv(option: CctvCreateModel):
    name, url = option
    response = Cctv.create(mysql, name[1], url[1])
    return response

@app.post('/cctv/read')
def read_cctv():
    response = Cctv.read(mysql)
    return response

@app.post('/cctv/update')
def update_cctv(option: CctvUpdateModel):
    target, name, url = option
    response = Cctv.update(mysql, target[1], name[1], url[1])
    return response

@app.post('/cctv/delete')
def delete_cctv(option: CctvDeleteModel):
    target = option
    response = Cctv.delete(mysql, target[1])
    return response

# Event Services
@app.post('/event/create')
def create_event(option: EventCreateModel):
    e_type, name = option
    response = Event.create(mysql, e_type[1], name[1])
    return response

@app.post('/event/read')
def read_event(option: EventReadModel):
    target = option
    response = Event.read(mysql, target[1])
    return response

@app.post('/event/update')
def update_event(option: EventUpdateModel):
    target, name, url = option
    response = Event.update(mysql, target[1], name[1], url[1])
    return response

@app.post('/event/delete')
def delete_event(option: EventDeleteModel):
    target = option
    response = Event.delete(mysql, target[1])
    return response

# Location Services
@app.post('/location/create')
def create_location(option: LocationCreateModel):
    name, cctv = option
    response = Location.create(mysql, name[1], cctv[1])
    return response

@app.post('/location/read')
def read_location(option: LocationReadModel):
    target = option
    response = Location.read(mysql, target[1])
    return response

@app.post('/location/update')
def update_location(option: LocationUpdateModel):
    target, name, url = option
    response = Location.update(mysql, target[1], name[1], url[1])
    return response

@app.post('/location/delete')
def delete_location(option: LocationDeleteModel):
    target = option
    response = Location.delete(mysql, target[1])
    return response

# Log Services
@app.post('/log/read')
def read_log(option: LogReadModel):
    datetime, locations, types = option
    response = Log.read(mysql, datetime[1], locations[1], types[1])
    return response