from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DATABASE = {
        'host': os.getenv('DATABASE_HOST'),
        'user': os.getenv('DATABASE_USER'),
        'password': os.getenv('DATABASE_PASSWORD'),
        'database': os.getenv('DATABASE_NAME'),
    }
    CLOUDINARY = {
        'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'api_key': os.getenv('CLOUDINARY_API_KEY'),
        'api_secret': os.getenv('CLOUDINARY_API_SECRET'),
    }
