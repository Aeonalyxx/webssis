import pymysql
from pymysql.cursors import DictCursor
from app.config import Config

def get_db_connection():
    db_config = Config.DATABASE
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=DictCursor
    )
    return connection

def close_connection(connection):
    if connection:
        connection.close()
