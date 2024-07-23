from utils.time import now
from db.controller import MysqlDB

def read(datetime = [], locations = [], types = []):
    try:
        db = MysqlDB()
        _datetime = ""
        _locations = ""
        _types = ""
        sql = ""
        if datetime != []:
            _datetime = f"occurred_at BETWEEN {datetime[0]} AND {datetime[1]}"
        if locations != []:
            _location_list = [f"'{l}'" for l in locations]
            _location_list = ", ".join(_location_list)
            _locations = f"location IN ({_location_list})"
        if types != []:
            _type_list = [f"'{t}'" for t in types]
            _type_list = ", ".join(_type_list)
            _types = f"type IN ({_type_list})"
        sql = "SELECT * FROM log"
        if _datetime != "" or _locations != "" or _types != "":
            sql += " WHERE"
            if _datetime != "":
                sql += " " + _datetime
            if _locations != "":
                if _datetime != "":
                    sql += " AND"
                sql += " " + _locations
            if _types != "":
                if _datetime != "" or _locations != "":
                    sql += " AND"
                sql += " " + _types         
        sql += " ORDER BY id DESC"
        db.cur.execute(sql)
        response = db.cur.fetchall()
        return response
    except Exception as e:
        print("Error occured in services.location.read",e)

def check(target):
    try:
        db = MysqlDB()
        n = now()
        if target == -1:
            sql = "UPDATE log SET checked_at = %s WHERE checked_at IS NULL"
            db.cur.execute(sql, (n))
        else:
            sql = "UPDATE log SET checked_at = %s WHERE id = %s AND checked_at IS NULL"
            db.cur.execute(sql, (n, target))
        db.conn.commit()
        return True
    except Exception as e:
        print("Error occured in services.location.check",e)
        return False