import math
import time
import logging
import requests
import re
import sys
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pyrogram import Client, filters
from pyrogram.errors import RPCError, BadRequest, Forbidden, FloodWait
from pyrogram.handlers import MessageHandler
from typing import Text
from values import *

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

admins = [
    "7731790583",  # Pon aquí los IDs de los admins que autorizas
    "987"
]

def verified_gps():
    """
    Lee el archivo 'files/groups.txt' y devuelve la lista de grupos permitidos (IDs con salto de línea).
    """
    try:
        with open('files/groups.txt', 'r') as file:
            grupos = file.readlines()
        return grupos
    except FileNotFoundError:
        return []

@Client.on_message(filters.command('addgp', prefixes=['.', '/', '!'], case_sensitive=False) & filters.text)
async def add_group(Client, message):
    try:
        user_id_str = str(message.from_user.id)
        if user_id_str in admins:
            grupos = verified_gps()
            group_id_str = str(message.chat.id) + "\n"
            if group_id_str not in grupos:
                with open('files/groups.txt', 'a+') as file:
                    file.write(group_id_str)
                await message.reply_text(
                    text="<b>✅ Grupo añadido correctamente.</b>",
                    reply_to_message_id=message.id
                )
            else:
                await message.reply_text(
                    text="<b>⚠️ Este grupo ya está añadido.</b>",
                    reply_to_message_id=message.id
                )
        else:
            await message.reply_text(
                text="<b>❌ No tienes permisos para usar este comando.</b>",
                reply_to_message_id=message.id
            )
    except Exception as e:
        logging.error(f"Error en add_group: {e}")
        await message.reply_text(
            text=f"<b>⚠️ Error:</b> {e}",
            reply_to_message_id=message.id
        )
