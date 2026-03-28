import os
import cloudinary
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent

if os.getenv("FLASK_ENV") != "production":
    load_dotenv(BASE_DIR / ".env")


def get_env(var):
    value = os.getenv(var)
    if not value:
        raise RuntimeError(f"Missing environment variable: {var}")
    return value


def init_cloudinary():
    print("envs found")
    cloudinary.config(
        cloud_name=get_env("CLOUDINARY_CLOUD_NAME"),
        api_key=get_env("CLOUDINARY_API_KEY"),
        api_secret=get_env("CLOUDINARY_API_SECRET")
    )