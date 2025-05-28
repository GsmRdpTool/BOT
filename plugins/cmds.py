from datetime import datetime
import time
from telegraph import upload_file
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from pymongo.errors import *
from values import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command(['cmds', 'gates', 'commands', f'gates@{BOT_USERNAME}', f'cmds@{BOT_USERNAME}', f'commands@{BOT_USERNAME}'], prefixes=['.', '/', '!'], case_sensitive=False) & filters.text)
async def cmds(Client, message):
    try:
        buttons = [
            [
                InlineKeyboardButton(' FREE ', callback_data='free'), 
                InlineKeyboardButton(' PAID ', callback_data='paid')
            ],
            [
                InlineKeyboardButton(' TOOLS ', callback_data='tools'),
                InlineKeyboardButton(' CLOSE ', callback_data='close')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        text = """
<b>【〄】 Bienvenido a Songji-woo Checker / gateways</b>
<b>━━━━━━━━━━━━━━━━━</b>
<b>Gates (56)</b>
<b>━━━━━━━━━━━━━━━━━</b>
<b>Auth (7) | Charged (7)</b>
<b>CCN (10) | Special (8)</b>
<b>Free (5) | Diamond (14)</b>
<b>Mass Checking (5)</b>
<b>━━━━━━━━━━━━━━━━━</b>
        """

        gif_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXVpdmI0cXVnMjJkMWFwb3NobHUxNjBsNjdkYzRtb2MxdHV6a2NqYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vQ0g0Ah0AE5A1quzKt/giphy.gif"  # Puedes cambiar este

        await message.reply_animation(
            animation=gif_url,
            caption=text,
            reply_markup=reply_markup
        )

    except Exception as e:
        print(e)
