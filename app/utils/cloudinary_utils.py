import cloudinary
from app.config import Config

def configure_cloudinary():
    cloudinary.config(
        cloud_name=Config.CLOUDINARY['cloud_name'],
        api_key=Config.CLOUDINARY['api_key'],
        api_secret=Config.CLOUDINARY['api_secret']
    )
