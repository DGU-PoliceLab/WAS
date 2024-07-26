from datetime import datetime as dt
from utils.time import now
from db.controller import MysqlDB

def read(datetime = [], locations = [], types = []):
    try:
        db = MysqlDB()
        query_params = []
        conditions = []

        if datetime:
            start_time = dt.strptime(datetime[0], "%Y-%m-%dT%H:%M:%S.%fZ")
            end_time = dt.strptime(datetime[1], "%Y-%m-%dT%H:%M:%S.%fZ")
            conditions.append("occurred_at BETWEEN %s AND %s")
            query_params.extend([start_time, end_time])

        if locations:
            _locations = ", ".join(["%s"] * len(locations))
            conditions.append(f"location IN ({_locations})")
            query_params.extend(locations)

        if types:
            _types = ", ".join(["%s"] * len(types))
            conditions.append(f"type IN ({_types})")
            query_params.extend(types)

        sql = "SELECT * FROM log"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id DESC"

        db.cur.execute(sql, query_params)
        response = db.cur.fetchall()
        return response
    except Exception as e:
        print("Error occured in services.log.read", e)
        return []
    
def read(datetime = [], locations = [], types = []):
    try:
        db = MysqlDB()
        query_params = []
        conditions = []

        if datetime:
            start_time = dt.strptime(datetime[0], "%Y-%m-%dT%H:%M:%S.%fZ")
            end_time = dt.strptime(datetime[1], "%Y-%m-%dT%H:%M:%S.%fZ")
            conditions.append("occurred_at BETWEEN %s AND %s")
            query_params.extend([start_time, end_time])

        if locations:
            _locations = ", ".join(["%s"] * len(locations))
            conditions.append(f"location IN ({_locations})")
            query_params.extend(locations)

        if types:
            _types = ", ".join(["%s"] * len(types))
            conditions.append(f"type IN ({_types})")
            query_params.extend(types)

        sql = "SELECT * FROM log"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id DESC LIMIT 100"

        db.cur.execute(sql, query_params)
        response = db.cur.fetchall()
        return response
    except Exception as e:
        print("Error occured in services.log.read", e)
        return []

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
        print("Error occured in services.log.check",e)
        return False