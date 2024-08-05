import os
import urllib

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
password = os.getenv('database_key')

client = MongoClient(
f"mongodb+srv://shiro:{urllib.parse.quote(password)}@disboard.zz80kgq.mongodb.net/?retryWrites=true&w=majority&appName=Disboard"
)

db = client["Disboard"]
players_collection = db["players"]
