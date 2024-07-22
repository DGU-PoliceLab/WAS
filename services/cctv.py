from datetime import datetime
from db.controller import MysqlDB

def create(name, url):
    try:
        db = MysqlDB()
        sql = "INSERT INTO cctv (name, url) VALUE (%s, %s)"
        db.cur.execute(sql, (name, url))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.cctv.create",e)
        return False

def read():
    try:
        db = MysqlDB()
        sql = "SELECT * FROM cctv"
        db.cur.execute(sql)
        response = db.cur.fetchall()
        return response
    except Exception as e:
        print("Error occured in services.cctv.read",e)

def update(target, name, url):
    try:
        db = MysqlDB()
        now = datetime.now()
        sql = "UPDATE cctv SET name = %s, url = %s, created_at = %s WHERE id = %s"
        db.cur.execute(sql, (name, url, now, target))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.cctv.update",e)
        return False

def delete(target):
    try:
        db = MysqlDB()
        sql = "DELETE FROM cctv WHERE id = %s"
        db.cur.execute(sql, (target))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.cctv.delete",e)
        return False