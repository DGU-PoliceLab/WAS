def create(db, name, cctv):
    try:
        print(cctv, type(cctv))
        if type(cctv) == int:
            sql = "INSERT INTO location (name, cctv) VALUE (%s, %s)"
            db.cur.execute(sql, (name, cctv))
        else:
            sql = "INSERT INTO location (name) VALUE (%s)"
            db.cur.execute(sql, (name))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.create",e)

def read(db, target):
    try:
        if type(target) == tuple:
            sql = "SELECT * FROM location"
            db.cur.execute(sql)
            response = db.cur.fetchall()
        else:
            sql = "SELECT * FROM location WHERE id = %s"
            db.cur.execute(sql, (target))
            response = db.cur.fetchone()
        return response
    except Exception as e:
        print("Error occured in services.location.read",e)

def update(db, target, values):
    try:
        if len(values) == 1:
            sql = "UPDATE location SET name = %s WHERE id = %s"
            db.cur.execute(sql, (values[0], target))
        else:
            sql = "UPDATE location SET name = %s, cctv = %s WHERE id = %s"
            db.cur.execute(sql, (values[0], values[1], target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.update",e)

def update_cctv(db, target, cctv):
    try:
        sql = "UPDATE location SET cctv = %s WHERE id = %s"
        db.cur.execute(sql, (cctv, target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.update_cctv",e)

def delete(db, target):
    try:
        sql = "DELETE FROM location WHERE id = %s"
        db.cur.execute(sql, (target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.location.delete",e)