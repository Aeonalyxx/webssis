import pymysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'decepticons',
    'database': 'webssis'
}

def get_db_connection():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=DictCursor
    )
    return connection

def close_connection(connection):
    if connection:
        connection.close()
