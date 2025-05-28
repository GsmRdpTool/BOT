from pymongo.errors import *
from values import *
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

@Client.on_message(filters.command(['price','buy' ,'purchase', f'buy@{BOT_USERNAME}' , f'price@{BOT_USERNAME}', f'purchase@{BOT_USERNAME}'],prefixes=['.','/','!'],case_sensitive=False) & filters.text)
async def register(client, message):
    try: 
        buttons = [[InlineKeyboardButton(' BUY ', callback_data='buy')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        text = "<b>【〄】 Comprar un plan 【〄】</b>\n\n" \
        "Si desea comprar un plan, por favor contacte al administrador del bot.\n\n" \
        "Si desea ver los precios de los planes, use el comando /price.\n\n" \

        gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXVpdmI0cXVnMjJkMWFwb3NobHUxNjBsNjdkYzRtb2MxdHV6a2NqYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vQ0g0Ah0AE5A1quzKt/giphy.gif"  # Puedes cambiar la URL por otro gif

        await message.reply_animation(
            animation=gif_url,
            caption=text,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(e)
