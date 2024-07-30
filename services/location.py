from db.controller import MysqlDB

def create(name, cctv):
    try:
        db = MysqlDB()
        if cctv >= 0:
            sql = "INSERT INTO location (name, cctv) VALUE (%s, %s)"
            db.cur.execute(sql, (name, cctv))
        else:
            sql = "INSERT INTO location (name) VALUE (%s)"
            db.cur.execute(sql, (name))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.location.create",e)
        return False

def read():
    try:
        db = MysqlDB()
        sql = "SELECT l.id as location_id, l.name as location_name, cctv as cctv_id, c.name as cctv_name, url, created_at, thermal_ip, thermal_port, rader_ip, rader_port FROM location as l LEFT JOIN cctv as c ON l.cctv = c.id"
        db.cur.execute(sql)
        response = db.cur.fetchall()
        return response
    except Exception as e:
        print("Error occured in services.location.read",e)
        return False
    
def check(name):
    try:
        db = MysqlDB()
        sql = "SELECT * FROM location WHERE name = %s"
        db.cur.execute(sql, (name))
        response = db.cur.fetchall()
        if len(response) == 0:
            return True
        else:
            return False
    except Exception as e:
        print("Error occured in services.location.read",e)
        return False

def read_with_cctv():
    try:
        db = MysqlDB()
        sql = "SELECT l.id as location_id, l.name as location_name, cctv as cctv_id, c.name as cctv_name, url, created_at, thermal_ip, thermal_port, rader_ip, rader_port FROM location as l LEFT JOIN cctv as c ON l.cctv = c.id WHERE c.id IS NOT NULL"
        db.cur.execute(sql)
        response = db.cur.fetchall()
        return response
    except Exception as e:
        print("Error occured in services.location.read",e)
        return False

def update(target, name, cctv):
    try:
        db = MysqlDB()
        if cctv == -1:
            sql = "UPDATE location SET name = %s, cctv = NULL WHERE id = %s"
            db.cur.execute(sql, (name, target))
        else:
            sql = "UPDATE location SET name = %s, cctv = %s WHERE id = %s"
            db.cur.execute(sql, (name, cctv, target))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.location.update",e)
        return False

def update_cctv(target, cctv):
    try:
        db = MysqlDB()
        sql = "UPDATE location SET cctv = %s WHERE id = %s"
        db.cur.execute(sql, (cctv, target))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.location.update_cctv",e)
        return False

def delete(target):
    try:
        db = MysqlDB()
        sql = "DELETE FROM location WHERE id = %s"
        db.cur.execute(sql, (target))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.location.delete",e)
        return False