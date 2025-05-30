#pylint:disable=C0114
import logging
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient

# Configuración básica de logs
logging.basicConfig(level=logging.INFO)

# ✅ Conexión a MongoDB
mongo = AsyncIOMotorClient("mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Cambia si usas Atlas
db = mongo["mills"]  # mills es tu base de datos

# ✅ Crear instancia del bot
bot = Client(
    "bot",
    api_id=23361603,
    api_hash="01f4d3cb3732b8ffdaadfd3843ffee1d",
    bot_token="8082652479:AAHGABcgGO7vlvh2RcVyBnzkqwEMd0sD5is",
    plugins=dict(root="plugins"),
)

# ✅ Inyectar la base de datos en el cliente
bot.db = db

# ✅ Ejecutar el bot
try:
    bot.run()
except Exception as e:
    print(e)
