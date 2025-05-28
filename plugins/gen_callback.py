from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re, random, requests
from values import ccs, banned_bins, maindb
import pycountry

bins_collection = maindb["bins"]  # ✅ definición aquí

# (pegar aquí tus funciones get_country_name, get_flag_emoji, etc.)

@Client.on_callback_query(filters.regex(r"^gen_"))
async def re_gen_callback(client, callback_query):
    try:
        await callback_query.answer()  # Cierra el "relojito" de espera

        user_data = maindb.find_one({"_id": callback_query.from_user.id})
        if not user_data:
            await callback_query.message.edit_text("❌ No estás registrado en la base de datos.")
            return

        data = callback_query.data.split("gen_")[1]
        cc, mes, ano, cvv = data.split("|")
        bin_code = cc[:6].replace('x', '0').replace('X', '0')

        if f"{bin_code}\n" in banned_bins():
            await callback_query.message.edit_text("❌ Bin bloqueado.")
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
                await callback_query.message.edit_text("❌ Bin no encontrado.")
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
        tarjetas = ''.join(ccs)
        ccs.clear()

        rol = user_data.get("role", "Free")
        nombre = callback_query.from_user.first_name
        user_id = callback_query.from_user.id

        texto = f"""
<b>════════════════════</b>
<b>【〄】 RE-GENERADOR DE TARJETAS 【〄】</b>
<b>════════════════════</b>
<code>{tarjetas}</code>
<b>════════════════════</b>
<b>【〄】 Bin ingresado:</b> <code>{cc}|{mes}|{ano}|{cvv}</code>
<b>【〄】 Banco:</b> <b>{bank}</b>
<b>【〄】 País:</b> <b>{country} {emoji}</b>
<b>【〄】 Tipo:</b> <b>{tipo}</b> - <b>{nivel}</b>
<b>【〄】 Bin:</b> <code>{bin_code}</code>
<b>════════════════════</b>
<b>【〄】 Gen By:</b> <b><a href="tg://user?id={user_id}">{nombre}</a> - {rol}</b>
"""

        botones = [[InlineKeyboardButton("Re-Gen", callback_data=f"gen_{cc}|{mes}|{ano}|{cvv}")]]
        markup = InlineKeyboardMarkup(botones)
        await callback_query.message.edit_text(texto, reply_markup=markup)

    except Exception as e:
        print(f"Error en re-gen: {e}")
        await callback_query.message.edit_text("❌ Error al regenerar tarjetas.")
