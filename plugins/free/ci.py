import time, requests, re, random, string
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from values import sk_headers, get_time_taken


@Client.on_message(filters.command("ci", [".", "/", "!"]))
async def stripe_auth(client, message):
    inicio = time.time()
    user_id = message.from_user.id
    nombre = message.from_user.first_name

    # Extraer tarjeta
    if message.reply_to_message:
        texto = message.reply_to_message.text
    else:
        try:
            texto = message.text.split(None, 1)[1]
        except:
            return await message.reply("<b>Formato requerido: CC|MM|AA|CVV</b>", parse_mode="html")

    try:
        cc, mes, ano, cvv = re.findall(r"\d+", texto)[:4]
    except:
        return await message.reply("<b>Error: Formato incorrecto</b>", parse_mode="html")

    if len(ano) == 2:
        ano = "20" + ano

    bin_ = cc[:6]

    # Consulta BIN
    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_}", timeout=10).json()
        banco = r.get("bank", {}).get("name", "N/A")
        tipo = r.get("type", "N/A")
        pais = r.get("country", {}).get("name", "N/A")
        emoji = r.get("country", {}).get("emoji", "")
        esquema = r.get("scheme", "N/A")
    except:
        banco, tipo, pais, emoji, esquema = ["N/A"] * 5

    # Datos aleatorios
    correo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@gmail.com"

    # Stripe AUTH checker con /v1/payment_methods
    sk_key = "pk_live_kbUIwYxKNj8PVjKFAaDN5ZN300MXislCjC"  # 🔐 Cambia a tu sk_live
    headers = sk_headers(sk_key)
    data = {
        "type": "card",
        "card[number]": cc,
        "card[exp_month]": mes,
        "card[exp_year]": ano,
        "card[cvc]": cvv,
        "billing_details[email]": correo,
    }

    try:
        r = requests.post("https://api.stripe.com/v1/payment_methods", headers=headers, data=data, timeout=10)
        res = r.json()
    except Exception:
        return await message.reply("<b>Error al contactar con Stripe</b>", parse_mode="html")

    # Interpretar resultado
    if "id" in res and res.get("card", {}).get("checks", {}).get("cvc_check") == "pass":
        status = "APPROVED ✅ [CVV MATCH]"
    elif "error" in res:
        msg_error = res["error"].get("message", "").upper()
        status = f"REJECTED ❌ [{msg_error}]"
    else:
        status = "REJECTED ❌ [UNKNOWN ERROR]"

    fin = get_time_taken(inicio)

    # Mensaje final
    msg = f"""
<b>【〄】 GATE:</b> STRIPE AUTH [LIVE]
<b>【〄】 INPUT:</b> <code>{cc}|{mes}|{ano}|{cvv}</code>
<b>【〄】 RESULT:</b> <b>{status}</b>
<b>【〄】 BANK:</b> {banco} - {tipo}
<b>【〄】 BIN:</b> <code>{bin_}</code> - <b>{esquema}</b> - <b>{pais} {emoji}</b>
<b>【〄】 CHECKED BY:</b> <a href="tg://user?id={user_id}">{nombre}</a>
<b>【〄】 TIME TAKEN:</b> {fin}s
<b>【〄】 BOT BY:</b> @gsmdiego
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("「ADMIN 1」", url="https://t.me/admin1username"),
            InlineKeyboardButton("「ADMIN 2」", url="https://t.me/admin2username")
        ],
        [
            InlineKeyboardButton("「OWNER」", url="https://t.me/gsmdiego")
        ]
    ])

    # URL de la imagen horizontal que quieres poner al final
    imagen_horizontal = "https://i.pinimg.com/736x/6b/a2/0f/6ba20f856ef336693c95b2347a9cdb42.jpg"  # Cambia por tu imagen

    # Enviar foto con el texto como caption
    await message.reply_photo(
        photo=imagen_horizontal,
        caption=msg,
        reply_markup=buttons,
    )
