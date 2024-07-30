import os
import cv2
import pickle
from db.controller import RedisDB
from utils.snapshot import snapshot

class ObjectManager():

    def __init__(self):
        self.db = RedisDB()
        self.conn = self.db.conn
        self.conn.set("snap", self._to_byte({}))

    def _to_byte(self, data):
        byteData = pickle.dumps(data)
        return byteData
    
    def _to_data(self, byteData):
        data = pickle.loads(byteData)
        return data
    
    def read(self, target = None):
        try:
            byteData = self.conn.get("snap")
            objectData = self._to_data(byteData)
            if target is not None:
                if target in objectData:
                    return objectData[target]
                else:
                    return []
            else:
                return objectData
        except Exception as e:
            print("Error occurred in utils.objectManage.ObjectManager.read:", e)
            return False
        
    def update(self, target, data):
        try:
            objectData = self.read()
            objectData[target] = data
            byteData = self._to_byte(objectData)
            self.conn.set("snap", byteData)
            return True
        except Exception as e:
            print("Error occurred in utils.objectManage.ObjectManager.update:", e)
            return False
