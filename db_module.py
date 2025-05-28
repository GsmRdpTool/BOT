from pymongo import MongoClient

mongo = MongoClient("mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo["mills"]
users = db["users"]
