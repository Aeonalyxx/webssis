import pymysql
from pymysql.cursors import DictCursor
import cloudinary
from app.config import Config

# ===================
# Database Utilities
# ===================
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

# ==========================
# Cloudinary Configuration
# ==========================
def configure_cloudinary():
    cloudinary.config(
        cloud_name=Config.CLOUDINARY['cloud_name'],
        api_key=Config.CLOUDINARY['api_key'],
        api_secret=Config.CLOUDINARY['api_secret']
    )
