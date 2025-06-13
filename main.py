#pylint:disable=C0114
import logging
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# -----------------------------------------------
# CONFIGURACIÓN DE LOGS
# -----------------------------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------------------------
# CONEXIÓN A MONGODB (puedes usar Atlas o local)
# -----------------------------------------------
mongo = AsyncIOMotorClient(
    "mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = mongo["mills"]  # Cambia "mills" por el nombre de tu base si es diferente

# -----------------------------------------------
# CONFIGURACIÓN DEL BOT DE TELEGRAM
# -----------------------------------------------
bot = Client(
    "bot",  # Nombre de la sesión
    api_id=23361603,
    api_hash="01f4d3cb3732b8ffdaadfd3843ffee1d",
    bot_token="7942809098:AAFLPoxwQuWviZxVxC_rCdoUC9p0R7f6a1k",
    plugins=dict(root="plugins"),  # O quita esta línea si no usas plugins
)

# -----------------------------------------------
# INYECTAR DB EN EL CLIENTE PARA USO FUTURO
# -----------------------------------------------
bot.db = db

# -----------------------------------------------
# HANDLER BÁSICO PARA /start
# -----------------------------------------------
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text(
        "👋 ¡Hola! El bot ya está funcionando correctamente desde Termux.\n"
        "Puedes comenzar a desarrollar tus comandos personalizados. 🚀"
    )

# -----------------------------------------------
# INICIO DEL BOT
# -----------------------------------------------
if __name__ == "__main__":
    try:
        logging.info("🚀 Iniciando bot...")
        bot.run()
    except Exception as e:
        print("❌ Error al iniciar el bot:", e)
