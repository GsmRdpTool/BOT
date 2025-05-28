from helpers.decorators import requiere_plan
from pyrogram import Client, filters

@Client.on_message(filters.command("checker"))
@requiere_plan(["premium", "diamond"])
async def checker(client, message):
    await message.reply("✅ Tienes acceso al checker.")
