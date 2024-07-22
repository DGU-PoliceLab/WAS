import pymysql
import redis
import json
import time
from threading import Thread
from datetime import datetime
from db.config import config_redis, config_mysql
from utils.time import timestamp


class MysqlDB():

    def __init__(self):
        self.config = config_mysql()
        self.conn = None
        self.connect()
    
    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.config['host'],
                port=int(self.config['port']),
                user=self.config['user'],
                password=self.config['password'],
                db=self.config['db'],
                charset=self.config['charset'],
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Error occured in db.controller.connect",e)

    def disconnect(self):
        try:
            if self.conn != None:
                self.conn.close()
            else:
                print("Warning: The database is not yet connected. Please use MysqlDB.connect() to connect.")    
        except Exception as e:
            print("Error occured in db.controller.disconnect",e)

    def insert(self, table, columns = [], values = []):
        try:
            _columns = ", ".join(columns)
            _values = []
            for v in values:
                if type(v) == str:
                    _values.append(f"'{v}'")
                else:
                    _values.append(str(v))
            _values = ", ".join(_values)
            if _columns == "":
                sql = f"INSERT INTO {table} VALUES ({_values});"
            else:
                sql = f"INSERT INTO {table} ({_columns}) VALUE ({_values});"
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("Error occured in db.controller.insert",e)

    def select(self, table, targets = None, options = None):
        try:
            if targets:
                _targets = ', '.join(targets)
            else:
                _targets = "*"
            if options:
                sql = f"SELECT {_targets} FROM {table} WHERE {options};"
            else:
                sql = f"SELECT {_targets} FROM {table};"
            self.cur.execute(sql)
            response = self.cur.fetchall()
            return response
        except Exception as e:
            print("Error occured in db.controller.insert",e)

class RedisDB():

    def __init__(self):
        self.config = config_redis()
        self.conn = None
        self.connect()
    
    def connect(self):
        try:
            self.conn = redis.Redis(
                host=self.config['host'],
                port=int(self.config['port']),
                db=self.config['db'],
            )
        except Exception as e:
            print("Error occured in db.controller.connect",e)

class RedisMQ():

    def __init__(self):
        self.config = config_redis()
        self.conn = None
        self.mysql = None
        self.connect()
    
    def connect(self):
        try:
            self.conn = redis.Redis(
                host=self.config['host'],
                port=int(self.config['port']),
                db=self.config['db'],
            )
            self.mysql = MysqlDB()
            cleaner_thread = Thread(target=self._cleaner, args=(self.conn,))
            cleaner_thread.start()
        except Exception as e:
            print("Error occured in db.controller.connect",e)

    def _save(self, message):
        try:
            if isinstance(message['occurred_at'], datetime):
                occured_at = message['occurred_at']
            else:
                occured_at = datetime.fromtimestamp(message['occurred_at'])
            pre = json.loads(self.conn.get('realtime'))
            if pre == "":
                cur = str(message)
            else:
                cur = pre + ", " + str(message)
            cur = json.dumps(cur)
            self.conn.set('realtime', cur)
            sql = "INSERT INTO log (type, location, occurred_at) VALUE (%s, %s ,%s)"
            self.mysql.cur.execute(sql, (message['event'], message['location'],occured_at))
            self.mysql.conn.commit()
            return True
        except Exception as e:
            print("Error occured in db.controller._save",e)
            return False

    def send(self, key, message):
        try:
            self._save(message)
            try:
                message['occurred_at'] = timestamp(message['occurred_at'])
            except:
                pass
            _message = json.dumps(message)
            self.conn.lpush(key, _message)
            return True
        except Exception as e:
            print("Error occured in db.controller.send",e)
            return False
        
    def _cleaner(self, conn):
         while True:
            cur = json.dumps("")
            conn.set('realtime', cur)
            time.sleep(1)

    def recv(self, key):
        try:
            queue, message = self.conn.brpop(key)
            _message = json.loads(message)
            return _message
        except Exception as e:
            print("Error occured in db.controller.recv",e)
            return False

    def is_empty(self, key):
        try:
            length = self.conn.lrange(key, 0, -1)
            if length == 0:
                return True
            else:
                return False
        except Exception as e:
            print("Error occured in db.controller.is_empty",e)