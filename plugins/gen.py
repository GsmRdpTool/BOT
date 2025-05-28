from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re, requests
import pycountry
from values import ccs, banned_bins, maindb
import random

bins_collection = maindb["bins"]

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

# Luhn para validar tarjetas
def luhn_checksum(card_number: str) -> int:
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def calculate_luhn(partial_card_number: str) -> str:
    checksum = luhn_checksum(partial_card_number + '0')
    return str((10 - checksum) % 10)

def generate_valid_card(bin_pattern: str) -> str:
    # Determina longitud según el patrón
    clean_bin = bin_pattern.replace('x', '0').replace('X', '0')
    if clean_bin.startswith(("34", "37")):
        length = 15
    else:
        length = 16

    card_number = ''
    for char in bin_pattern:
        if char.lower() == 'x':
            card_number += str(random.randint(0, 9))
        else:
            card_number += char

    # Completar si faltan dígitos
    while len(card_number) < length - 1:
        card_number += str(random.randint(0, 9))

    # Agregar dígito Luhn
    check_digit = calculate_luhn(card_number)
    return card_number + check_digit

def generate_expiry():
    month = random.randint(1, 12)
    year = random.randint(25, 30)
    return f"{month:02d}", str(year)

def generate_cvv(card_number):
    if len(card_number) == 15:
        return f"{random.randint(1000, 9999)}"
    return f"{random.randint(100, 999)}"

def cc_gen(bin_code, mes='x', ano='x', cvv='x'):
    card = generate_valid_card(bin_code)
    if mes == 'x' or ano == 'x':
        mes, ano = generate_expiry()
    if cvv == 'x':
        cvv = generate_cvv(card)
    tarjeta = f"{card}|{mes}|{ano}|{cvv}"
    ccs.append(tarjeta)


@Client.on_message(filters.command(["gen", "make"], [".", "/", "!"]))
async def gen(client, message):
    try:
        text = message.reply_to_message.text if message.reply_to_message else message.text

        user_data = maindb.find_one({"_id": message.from_user.id})
        if not user_data:
            await message.reply("❌ No estás registrado en la base de datos.")
            return

        input_data = re.findall(r"[0-9xX]+", text)
        cc = mes = ano = cvv = 'x'

        if not input_data:
            cc = "453958xxxxxxxxxx"
        else:
            cc = input_data[0]
            if len(input_data) >= 2: mes = input_data[1]
            if len(input_data) >= 3: ano = input_data[2]
            if len(input_data) >= 4: cvv = input_data[3]

        if len(cc.replace("x", "").replace("X", "")) < 6:
            await message.reply("❌ Bin inválido.")
            return

        bin_code = cc[:6].replace('x', '0').replace('X', '0')
        if f"{bin_code}\n" in banned_bins():
            await message.reply("❌ Bin bloqueado.")
            return

        bin_data = bins_collection.find_one({"iin_start": int(bin_code)})
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
                await message.reply("❌ Bin no encontrado.")
                return
            j = res.json()
            bank = j.get("bank", {}).get("name", "Desconocido")
            country = j.get("country", {}).get("name", "Desconocido")
            emoji = j.get("country", {}).get("emoji", "🌐")
            tipo = j.get("type", "N/A").capitalize()
            nivel = j.get("brand", "N/A")
            code = j.get("country", {}).get("alpha2", "XX")
            bins_collection.insert_one({
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

        rol = user_data.get("role", "Free")
        nombre = message.from_user.first_name
        user_id = message.from_user.id

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
<b>【〄】 Gen By:</b> <b><a href="tg://user?id={user_id}">{nombre}</a> - {rol}</b>
"""

        botones = [[InlineKeyboardButton("Re-Gen", callback_data=f"gen_{cc}|{mes}|{ano}|{cvv}")]]
        markup = InlineKeyboardMarkup(botones)
        await message.reply(texto, reply_markup=markup)

    except Exception as e:
        print(f"Error en /gen: {e}")
        await message.reply("❌ Ocurrió un error al generar las tarjetas.")
