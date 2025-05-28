import os
import random
import httpx
import requests
import pycountry
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
)
from motor.motor_asyncio import AsyncIOMotorClient
from db_module import users
from tools import cc_gen, ccs
from values import maindb, bins_collection  # Asegúrate de importar correctamente

# Configuración de MongoDB
MONGO_URI = "mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB_NAME = "mills"
mongo_client = AsyncIOMotorClient(MONGO_URI)
maindb = mongo_client[MONGO_DB_NAME]["users"]       # colección usuarios
antidb = mongo_client[MONGO_DB_NAME]["antispam"]    # colección antispam
bins_collection = mongo_client[MONGO_DB_NAME]["bins"]  # colección bins

# ════════════════════════════════════════════════════════════════════════ #

async def myacc(client: Client, message, update: CallbackQuery):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        await client.answer_callback_query(
            callback_query_id=update.id,
            text="Por favor, responde a un mensaje de usuario válido.",
            show_alert=True
        )
        return

    buttons = [
        [InlineKeyboardButton(' MY LIVE ', callback_data='mylives'),
         InlineKeyboardButton(' GATES ', callback_data='gates')],
        [InlineKeyboardButton(' CLOSE ', callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    find = await users.find_one({"_id": message.reply_to_message.from_user.id})

    if find is None:
        await client.answer_callback_query(
            callback_query_id=update.id,
            text="Register First Hit /takeme to register yourself",
            show_alert=True
        )
    else:
        antispam_doc = await antidb.find_one({"_id": message.reply_to_message.from_user.id})
        antispam_str = datetime.utcfromtimestamp(antispam_doc["time"]).strftime('%H:%M:%S %d-%m-%Y') if antispam_doc and "time" in antispam_doc else "No registrado"

        text = f"""
<b>〄</b> User Information:
<b>〄</b> First Name: <b>{message.reply_to_message.from_user.first_name}</b>
<b>〄</b> User Name: <b>{message.reply_to_message.from_user.username}</b>
<b>〄</b> User Id: <b><code>{message.reply_to_message.from_user.id}</code></b>
<b>〄</b> Profile Link: <b><a href="tg://user?id={message.reply_to_message.from_user.id}">Click Here</a></b>

<b>〄</b> User Database Information:-
<b>〄</b> Role: <b>{find.get('role', 'N/A')}</b>
<b>〄</b> Plan: <b>{find.get('plan', 'N/A')}</b>
<b>〄</b> Status: <b>{find.get('status', 'N/A')}</b>
<b>〄</b> Credits: <b>{find.get('credits', 'N/A')}</b>
<b>〄</b> AntiSpam Time: <b>{antispam_str}</b>

<b>〄</b> Chat Information:-
<b>〄</b> Chat Name: <b>{message.reply_to_message.chat.title if message.reply_to_message.chat else 'N/A'}</b>
<b>〄</b> User Name: <b>{message.reply_to_message.chat.username if message.reply_to_message.chat else 'N/A'}</b>
<b>〄</b> Chat Id: <b><code>{message.reply_to_message.chat.id if message.reply_to_message.chat else 'N/A'}</code></b>
"""
        await client.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.id,
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

# ════════════════════════════════════════════════════════════════════════ #

async def gates(client: Client, message, update: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(' FREE ', callback_data='free'),
         InlineKeyboardButton(' PAID ', callback_data='paid')],
        [InlineKeyboardButton(' TOOLS ', callback_data='tools'),
         InlineKeyboardButton(' CLOSE ', callback_data='close')]
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
    await client.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# ════════════════════════════════════════════════════════════════════════ #

async def paid(client: Client, message, update: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(' AUTH ', callback_data='auth'),
         InlineKeyboardButton(' CHARGE ', callback_data='charge')],
        [InlineKeyboardButton(' EXTRA ', callback_data='extra'),
         InlineKeyboardButton(' TOOLS ', callback_data='tools')],
        [InlineKeyboardButton(' CLOSE ', callback_data='close')]
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
    await client.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# ════════════════════════════════════════════════════════════════════════ #

async def free(client: Client, message, update: CallbackQuery):
    buttons = [
        [InlineKeyboardButton('⤶ RETURN ⤶', callback_data='gates')],
        [InlineKeyboardButton(' CLOSE ', callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    text = """
<b>〄</b> Free Gates:

<b>〄</b> <b>/ca</b>: <b>Stripe Auth [1]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/ch</b>: <b>Stripe Auth [2]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/ci</b>: <b>Stripe Auth [3]</b> || <b>Status: On ✅</b>
"""
    await client.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# ════════════════════════════════════════════════════════════════════════ #

async def auth(client: Client, message, update: CallbackQuery):
    buttons = [
        [InlineKeyboardButton(' BUY ', callback_data='buy'),
         InlineKeyboardButton(' CHARGE ', callback_data='charge')],
        [InlineKeyboardButton('⤶ RETURN ⤶', callback_data='gates'),
         InlineKeyboardButton(' CLOSE ', callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    text = """
<b>〄</b> Auth Gates:
<b>📢</b> <b><i>2 credits per check.</i></b>
<b>〄</b> <b>/sa</b>: <b>Stripe [1]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/sc</b>: <b>Stripe [2]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/sf</b>: <b>Stripe [3]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/sh</b>: <b>Stripe [4]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/si</b>: <b>Stripe [5]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/sl</b>: <b>Stripe [6]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/sm</b>: <b>Stripe [7]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/so</b>: <b>Stripe [8]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/sp</b>: <b>Stripe [9]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/ss</b>: <b>Stripe [10]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/st</b>: <b>Stripe [11]</b> || <b>Status: On ✅</b>
<b>〄</b> <b>/su</b>: <b>Stripe [12]</b> || <b>Status: On ✅</b>
"""
    await client.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
  

async def charge(Client, message , update):
  buttons = [
    [
        InlineKeyboardButton(' BUY ', callback_data='buy'),
        InlineKeyboardButton(' EXTRA ', callback_data='extra')
    ],
    [
        InlineKeyboardButton('⤶ RETURN ⤶', callback_data='gates'),
        InlineKeyboardButton(' CLOSE ', callback_data='close')
    ]
    ]
  reply_markup = InlineKeyboardMarkup(buttons)
  text = """
<b>〄</b> Charge Gates:
<b>📢</b> <b><i>2 credits per check.</i></b>

<b>〄</b> <b>/za</b>: <b>Stripe [1]</b> || <b>Status: On ✅ </b>
<b>〄</b> <b>/zc</b>: <b>Stripe [2]</b> || <b>Status: On ✅ </b>
<b>〄</b> <b>/zm</b>: <b>Stripe [4]</b> || <b>Status: On ✅ </b>
<b>〄</b> <b>/zo</b>: <b>Stripe [5]</b> || <b>Status: On ✅ </b>
<b>〄</b> <b>/zt</b>: <b>Stripe [6]</b> || <b>Status: Off ❌</b>
<b>〄</b> <b>/zu</b>: <b>Stripe [7]</b> || <b>Status: Off ❌</b>
"""
  await Client.edit_message_text(
      chat_id=message.chat.id,
      text=text,
      reply_markup=reply_markup,
      message_id=message.id,
      disable_web_page_preview=True
  )

async def extra(Client, message , update):
  buttons = [
    [
        InlineKeyboardButton(' BUY ', callback_data='buy'),
        InlineKeyboardButton(' AUTH ', callback_data='auth')
    ],
    [
        InlineKeyboardButton('⤶ RETURN ⤶', callback_data='paid'),
        InlineKeyboardButton('CLOSE ', callback_data='close')
    ]
    ]
  reply_markup = InlineKeyboardMarkup(buttons)
  text = """
<b>〄</b> Extra Gates:

<b>〄</b> <b>/za</b>: <b>Stripe Auth [1]</b> || <b>Status: Off ❌</b>
<b>〄</b> <b>/zc</b>: <b>Stripe Auth [2]</b> || <b>Status: Off ❌</b>
<b>〄</b> <b>/zm</b>: <b>Stripe Auth [4]</b> || <b>Status: Off ❌</b>
<b>〄</b> <b>/zo</b>: <b>Stripe Auth [5]</b> || <b>Status: Off ❌</b>
<b>〄</b> <b>/zt</b>: <b>Stripe Auth [6]</b> || <b>Status: Off ❌</b>
<b>〄</b> <b>/zu</b>: <b>Stripe Auth [7]</b> || <b>Status: Off ❌</b>
"""
  await Client.edit_message_text(
      chat_id=message.chat.id,
      text=text,
      reply_markup=reply_markup,
      message_id=message.id,
      disable_web_page_preview=True
  )
  
  
async def buy(Client, message , update):
  buttons = [
    [
        InlineKeyboardButton(' BUY ', url='https://t.me/gsmdiego'),
        InlineKeyboardButton(' CHANNEL ', url='https://t.me/scrappersong')
    ],
    [
        InlineKeyboardButton('⤶ RETURN ⤶', callback_data='gates'),
        InlineKeyboardButton(' CLOSE ', callback_data='close')
    ]
    ]
  reply_markup = InlineKeyboardMarkup(buttons)
  text = """
<b>〄</b> Prices:

<b>〄</b> <b>5$</b>: <b>250 Credits</b> || <b>Access all gates</b>
<b>〄</b> <b>10$</b>: <b>600 Credits</b> || <b>Access all gates</b>
<b>〄</b> <b>20$</b>: <b>1500 Credits</b> || <b>Access all gates</b>
<b>〄</b> <b>25$</b>: <b>3000 Credits</b> || <b>Access all gates</b>
<b></b> <b><i>ONLY ACCEPTED CRYPTO CURRRENCY && UPI.</i></b>
"""
  await Client.edit_message_text(
      chat_id=message.chat.id,
      text=text,
      reply_markup=reply_markup,
      message_id=message.id,
      disable_web_page_preview=True
  )

async def gen(Client, message , update):
  buttons = [
    [
        InlineKeyboardButton(' BUY ', url='https://t.me/gsmdiego'),
        InlineKeyboardButton(' CHANNEL ', url='https://t.me/scrappersong')
    ],
    [
        InlineKeyboardButton('⤶ RETURN ⤶', callback_data='gates'),
        InlineKeyboardButton(' CLOSE ', callback_data='close')
    ]
    ]

# BINs bloqueados
banned_bins = []

# Lista temporal para almacenar tarjetas generadas
ccs = []

# ─── FUNCIONES UTILITARIAS ───────────────────────────────────────────────────

def get_country_name(code):
    try:
        country = pycountry.countries.get(alpha_2=code.upper())
        return country.name if country else code
    except:
        return code

def get_flag_emoji(code):
    try:
        return ''.join(chr(127397 + ord(c.upper())) for c in code)
    except:
        return '🌐'

def cc_gen(bin_pattern, mes, ano, cvv):
    bin_len = len(bin_pattern)
    faltantes = 16 - bin_len
    if faltantes > 0:
        bin_pattern += "x" * faltantes

    card_number = ""
    for ch in bin_pattern[:15]:
        card_number += str(random.randint(0, 9)) if ch.lower() == 'x' else ch

    def luhn_checksum(card_number):
        def digits_of(n): return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd = digits[-1::-2]
        even = digits[-2::-2]
        checksum = sum(odd)
        for d in even:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def calculate_luhn(card_number):
        checksum = luhn_checksum(card_number + '0')
        return str((10 - checksum) % 10)

    last_digit = calculate_luhn(card_number)
    card_number += last_digit

    mes = mes if mes.lower() != 'x' else f"{random.randint(1,12):02}"
    ano = ano if ano.lower() != 'x' else str(random.randint(26, 30))
    cvv = cvv if cvv.lower() != 'x' else f"{random.randint(100, 999)}"

    tarjeta = f"{card_number}|{mes}|{ano}|{cvv}"
    ccs.append(tarjeta)

# ─── CALLBACK RE-GEN ─────────────────────────────────────────────────────────

@Client.on_callback_query(filters.regex(r"^gen_(.+)$"))
async def gen_callback(client, callback_query):
    try:
        print("Entró a gen_callback")
        await callback_query.answer()

        data = callback_query.data.split("_", 1)[1]
        cc, mes, ano, cvv = (data.split("|") + ['x', 'x', 'x', 'x'])[:4]

        bin_code = cc[:6].replace('x', '0').replace('X', '0')
        if bin_code in banned_bins:
            await callback_query.answer("❌ Bin bloqueado.", show_alert=True)
            return

        bin_data = await bins_collection.find_one({"iin_start": int(bin_code)})
        if bin_data:
            bank = bin_data.get("bank_name", "Desconocido")
            country_code = bin_data.get("country", "N/A")
            country = get_country_name(country_code)
            emoji = get_flag_emoji(country_code)
            tipo = bin_data.get("type", "N/A").capitalize()
            nivel = bin_data.get("brand", "N/A")
        else:
            res = requests.get(f"https://lookup.binlist.net/{bin_code}")
            if res.status_code != 200:
                await callback_query.message.edit("❌ Bin no encontrado.")
                return
            j = res.json()
            bank = j.get("bank", {}).get("name", "Desconocido")
            country = j.get("country", {}).get("name", "Desconocido")
            emoji = j.get("country", {}).get("emoji", "🌐")
            tipo = j.get("type", "N/A").capitalize()
            nivel = j.get("brand", "N/A")
            code = j.get("country", {}).get("alpha2", "XX")
            await bins_collection.insert_one({
                "iin_start": int(bin_code),
                "scheme": j.get("scheme", ""),
                "brand": nivel,
                "type": tipo.lower(),
                "country": code,
                "bank_name": bank,
                "bank_url": j.get("bank", {}).get("url", ""),
                "bank_phone": j.get("bank", {}).get("phone", ""),
                "bank_city": j.get("bank", {}).get("city", "")
            })

        ccs.clear()
        for _ in range(10):
            cc_gen(cc, mes, ano, cvv)
        tarjetas = '\n'.join(ccs)
        ccs.clear()

        user = callback_query.from_user
        user_data = await maindb.find_one({"_id": user.id})
        rol = user_data.get("role", "Free") if user_data else "Free"

        hora = datetime.now().strftime("%H:%M:%S")

        texto = f"""
<b>════════════════════</b>
<b>【〄】 GENERADOR DE TARJETAS 【〄】</b>
<b>════════════════════</b>
<code>{tarjetas}</code>
<b>════════════════════</b>
<b>【〄】 Format:</b> <code>{cc}|{mes}|{ano}|{cvv}</code>
<b>【〄】 Bank:</b> <b>{bank}</b>
<b>【〄】 Country:</b> <b>{country} {emoji}</b>
<b>【〄】 Info:</b> <b>{tipo}</b> - <b>{nivel}</b>
<b>【〄】 Bin:</b> <code>{bin_code}</code>
<b>════════════════════</b>
<b>【〄】 Gen By:</b> <b><a href="tg://user?id={user.id}">{user.first_name}</a> - {rol}</b>
<b>〄 Re-Gen:</b> <i>{hora}</i>
"""

        botones = [[InlineKeyboardButton("Re-Gen", callback_data=f"gen_{cc}|{mes}|{ano}|{cvv}")]]
        markup = InlineKeyboardMarkup(botones)

        print("Editando mensaje...")
        await callback_query.message.edit(texto, reply_markup=markup)

    except Exception as e:
        print(f"❌ Error en re-gen: {e}")
        try:
            await callback_query.message.edit("❌ Error al regenerar tarjetas.")
        except:
            pass



async def tools(Client, message , update):
  buttons = [
    [
        InlineKeyboardButton('⤶ RETURN ⤶', callback_data='gates')
    ],
    [
        InlineKeyboardButton(' CLOSE ', callback_data='close')
    ]
    ]
  reply_markup = InlineKeyboardMarkup(buttons)
  text = """
<b>〄</b> Tools

<b>〄</b> <b>/info</b>: <b>Your Information</b>
<b>〄</b> <b>/bin</b>: <b>Bin Information</b>
<b>〄</b> <b>/gen</b>: <b>Genrate ccs from bin</b>
<b>〄</b> <b>/vbv</b>: <b>Check for vbv</b>
"""
# <b>/ci</b>: <b>Stripe Auth</b> || <b>Status: On ✅</b>
  await Client.edit_message_text(
      chat_id=message.chat.id,
      text=text,
      reply_markup=reply_markup,
      message_id=message.id,
      disable_web_page_preview=True
  )



@Client.on_callback_query()
async def button(Client, update: CallbackQuery):
    cb_data = update.data

    try:
        if cb_data == "myacc":
            await update.answer()  # Responde sin alerta
            await myacc(Client, update.message, update.from_user)

        elif cb_data == "close":
            await update.answer()
            await update.message.delete()

        elif "gates" in cb_data:
            await update.answer()
            await gates(Client, update.message, update)

        elif "free" in cb_data:
            await update.answer()
            await free(Client, update.message, update)

        elif "paid" in cb_data:
            await update.answer()
            await paid(Client, update.message, update)

        elif "auth" in cb_data:
            await update.answer()
            await auth(Client, update.message, update)

        elif "charge" in cb_data:
            await update.answer()
            await charge(Client, update.message, update)

        elif "extra" in cb_data:
            await update.answer()
            await extra(Client, update.message, update)

        elif "buy" in cb_data:
            await update.answer()
            await buy(Client, update.message, update)

        elif "gen" in cb_data:
            await update.answer()
            await gen(Client, update.message, update)

        elif "tools" in cb_data:
            await update.answer()
            await tools(Client, update.message, update)

        elif cb_data == "mylives":
            # Aquí sólo responder con alerta, no otro await update.answer()
            await update.answer("Coming Soon", show_alert=True)

    except RPCError as e:
        if "QUERY_ID_INVALID" in str(e):
            pass  # Ignorar este error común
        else:
            print(f"❌ Callback error: {e}")