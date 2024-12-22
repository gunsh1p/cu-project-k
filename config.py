import os

from dotenv import load_dotenv


load_dotenv()


TOKEN = os.environ.get("TOKEN")
API_HOST = os.environ.get("API_HOST", "http://127.0.0.1:5000")
