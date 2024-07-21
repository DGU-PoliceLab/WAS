import os
from dotenv import load_dotenv

def config_redis():
    try:
        load_dotenv()
        config = {
            'host': os.environ.get('REDIS_HOST'),
            'port': os.environ.get('REDIS_PORT'),
            'db': os.environ.get('REDIS_DATABASE'),
        }
        return config
    except Exception as e:
        print("Error occured in db.config.redis_config",e)

def config_mysql():
    try:
        load_dotenv()
        config = {
            'host': os.environ.get('MYSQL_HOST'),
            'port': os.environ.get('MYSQL_PORT'),
            'user': os.environ.get('MYSQL_USER'),
            'password': os.environ.get('MYSQL_PASSWORD'),
            'db': os.environ.get('MYSQL_DATABASE'),
            'charset': os.environ.get('MYSQL_CHARSET'),
        }
        return config
    except Exception as e:
        print("Error occured in db.config.mysql_config",e)