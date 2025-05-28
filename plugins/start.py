from datetime import datetime
from pymongo.errors import *
from values import *
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from values import BOT_USERNAME
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

REPLY_MARKUP  = InlineKeyboardMarkup([
    [
    InlineKeyboardButton('Tools', callback_data='tools'),
    InlineKeyboardButton(' Gateways ', callback_data='gates')
    ],
    [
        InlineKeyboardButton('CLOSE', callback_data='close')
    ]
])


@Client.on_message(filters.command(['start', f'start@{BOT_USERNAME}'], prefixes=['/', '.', '!']) & filters.text)
async def start(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)

        user = message.from_user
        nombre_completo = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Usuario"
        mencion_clickable = f'<a href="tg://user?id={user.id}">{nombre_completo}</a>'
        nombre_bot = "𝑺𝒐𝒏𝒈 𝑱𝒊-𝒘𝒐𝒐"
        mension_bot = f'<a href="https://t.me/{BOT_USERNAME}">{nombre_bot}</a>'

        texto = f"""
<b>━━━━━━━━━━━━━━</b>
<b> Hola Bienvenid@ a </b>{mension_bot}
<b>━━━━━━━━━━━━━━</b>
<b> Usuario:</b> {mencion_clickable}
<b>━━━━━━━━━━━━━━</b>
<b> Nueva Versión 2.0</b>
<b>━━━━━━━━━━━━━━</b>
"""

        gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXVpdmI0cXVnMjJkMWFwb3NobHUxNjBsNjdkYzRtb2MxdHV6a2NqYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vQ0g0Ah0AE5A1quzKt/giphy.gif"  # Puedes cambiar este

        await message.reply_animation(
            animation=gif_url,
            caption=texto,
            reply_markup=REPLY_MARKUP,
        )

    except Exception as e:
        await message.reply(f"❌ Error al iniciar: {e}")
