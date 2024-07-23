from db.controller import MysqlDB

def create(e_type, name):
    try:
        db = MysqlDB()
        sql = "INSERT INTO event (type, name) VALUE (%s, %s)"
        db.cur.execute(sql, (e_type, name))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.event.create",e)

def read(target):
    try:
        db = MysqlDB()
        if target == "":
            sql = "SELECT * FROM event"
            db.cur.execute(sql)
            response = db.cur.fetchall()
        else:
            sql = "SELECT * FROM event WHERE id = %s"
            db.cur.execute(sql, (target))
            response = db.cur.fetchone()
        return response
    except Exception as e:
        print("Error occured in services.event.read",e)

def update(target, e_type, name):
    try:
        db = MysqlDB()
        sql = "UPDATE event SET type = %s, name = %s WHERE id = %s"
        db.cur.execute(sql, (e_type, name, target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.event.update",e)

def delete(target):
    try:
        db = MysqlDB()
        sql = "DELETE FROM event WHERE id = %s"
        db.cur.execute(sql, (target))
        db.conn.commit()
    except Exception as e:
        print("Error occured in services.event.delete",e)