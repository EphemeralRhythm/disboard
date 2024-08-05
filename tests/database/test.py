from pymongo import MongoClient
from csvs import stat_gen
import urllib

password = "V*ab_C;%*STATB8"
client = MongoClient(
f"mongodb+srv://shiro:{urllib.parse.quote(password)}@disboard.zz80kgq.mongodb.net/?retryWrites=true&w=majority&appName=Disboard"
)
