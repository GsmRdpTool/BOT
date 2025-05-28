from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InputMediaAnimation
from datetime import datetime
from pymongo import MongoClient

mongo = MongoClient("mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo["mills"]
users = db["users"]
antispam = db["antispam"]

loggp = 123456789  # Reemplaza por tu chat ID válido

@Client.on_message(filters.command(['info', 'myacc'], prefixes=['.', '/', '!'], case_sensitive=False))
async def info(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)

        gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXVpdmI0cXVnMjJkMWFwb3NobHUxNjBsNjdkYzRtb2MxdHV6a2NqYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vQ0g0Ah0AE5A1quzKt/giphy.gif"

        gif_msg = await message.reply_animation(
            animation=gif_url,
            caption="<b>Espera un momento, obteniendo tu información...</b>"
        )

        user = message.from_user
        if not user:
            await gif_msg.edit_caption("No se pudo obtener la información del usuario.")
            return

        find = users.find_one({"_id": user.id})
        if not find:
            await gif_msg.edit_caption("<b>Por favor regístrate primero con el comando /takeme</b>")
            return

        anti_val = antispam.find_one({"_id": user.id})
        antispam_time = anti_val.get("time", 0) if anti_val else 0
        antispam_str = datetime.utcfromtimestamp(antispam_time).strftime('%H:%M:%S %d-%m-%Y') if antispam_time > 0 else "N/A"

        role = find.get('role', 'Ninguno')
        plan = find.get('plan', 'Gratis')
        status = find.get('status', 'Desconocido')
        credits = find.get('credits', 0)

        first_name = getattr(user, "first_name", "Desconocido")
        username = getattr(user, "username", "Desconocido")
        user_id = getattr(user, "id", "Desconocido")

        text = f"""
<b>【〄】</b> Información del Usuario:
<b>【〄】</b> Nombre: <b>{first_name}</b>
<b>【〄】</b> Usuario: <b>{username}</b>
<b>【〄】</b> ID: <b><code>{user_id}</code></b>
<b>【〄】</b> Perfil: <b><a href="tg://user?id={user_id}">Ver Perfil</a></b>

<b>【〄】</b> Datos en Base:
<b>【〄】</b> Rol: <b>{role}</b>
<b>【〄】</b> Plan: <b>{plan}</b>
<b>【〄】</b> Estado: <b>{status}</b>
<b>【〄】</b> Créditos: <b>{credits}</b>
<b>【〄】</b> AntiSpam Time: <b>{antispam_str}</b>
"""
        await gif_msg.edit_caption(text)

    except Exception as e:
        try:
            await client.send_message(chat_id=loggp, text=f"Error en comando /info: {str(e)}")
        except Exception as e2:
            print(f"No se pudo enviar mensaje de error: {e2}")
        print(f"Error en comando /info: {e}")
