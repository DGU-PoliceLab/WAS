from db.controller import MysqlDB

def create(name, cctv):
    try:
        db = MysqlDB()
        if type(cctv) == int:
            sql = "INSERT INTO location (name, cctv) VALUE (%s, %s)"
            db.cur.execute(sql, (name, cctv))
        else:
            sql = "INSERT INTO location (name) VALUE (%s)"
            db.cur.execute(sql, (name))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.create",e)

def read(target):
    try:
        db = MysqlDB()
        if target == "":
            sql = "SELECT * FROM location"
            print(sql)
            db.cur.execute(sql)
            response = db.cur.fetchall()
            print(response)
        else:
            sql = "SELECT * FROM location WHERE id = %s"
            db.cur.execute(sql, (target))
            response = db.cur.fetchone()
        return response
    except Exception as e:
        print("Error occured in services.location.read",e)

def read_with_cctv():
    try:
        db = MysqlDB()
        sql = "SELECT l.id as location_id, l.name as location_name, cctv as cctv_id, c.name as cctv_name, url, created_at FROM location as l LEFT JOIN cctv as c ON l.cctv = c.id WHERE c.id IS NOT NULL"
        db.cur.execute(sql)
        response = db.cur.fetchall()
        return response
    except Exception as e:
        print("Error occured in services.location.read",e)

def update(target, values):
    try:
        db = MysqlDB()
        if len(values) == 1:
            sql = "UPDATE location SET name = %s WHERE id = %s"
            db.cur.execute(sql, (values[0], target))
        else:
            sql = "UPDATE location SET name = %s, cctv = %s WHERE id = %s"
            db.cur.execute(sql, (values[0], values[1], target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.update",e)

def update_cctv(target, cctv):
    try:
        db = MysqlDB()
        sql = "UPDATE location SET cctv = %s WHERE id = %s"
        db.cur.execute(sql, (cctv, target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.update_cctv",e)

def delete(target):
    try:
        db = MysqlDB()
        sql = "DELETE FROM location WHERE id = %s"
        db.cur.execute(sql, (target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.delete",e)