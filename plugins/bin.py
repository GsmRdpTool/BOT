import requests
from pyrogram import Client, filters
from values import *  # verified_gps, use_not_registered, waste_cards, lista
import json

@Client.on_message(filters.command('bin', prefixes=['.', '/', '!']) & filters.text)
async def bin(Client, message):
    try:
        gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXVpdmI0cXVnMjJkMWFwb3NobHUxNjBsNjdkYzRtb2MxdHV6a2NqYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vQ0g0Ah0AE5A1quzKt/giphy.gif"
        gif_msg = await message.reply_animation(gif, caption="Consultando información del BIN...", reply_to_message_id=message.message_id)
        await Client.send_chat_action(message.chat.id, "typing")

        if message.reply_to_message and message.reply_to_message.text:
            message_text = message.reply_to_message.text
        else:
            message_text = message.text

        user_obj = message.from_user
        if not user_obj or isinstance(user_obj, str):
            await gif_msg.edit_caption("❌ No se pudo identificar al usuario correctamente (from_user no válido).")
            return

        if not hasattr(user_obj, "id") or not hasattr(user_obj, "first_name"):
            await gif_msg.edit_caption("❌ Información del usuario incompleta (faltan atributos).")
            return

        user = await maindb.find_one({"_id": user_obj.id})
        if not user:
            await gif_msg.edit_caption(use_not_registered)
            return

        datos = lista(message_text)
        if not datos or len(datos[0]) < 6:
            await gif_msg.edit_caption("❌ El BIN está vacío o es demasiado corto.")
            return

        bin_code = datos[0]

        if not bin_code or not bin_code[0].isdigit() or int(bin_code[0]) in waste_cards:
            await gif_msg.edit_caption("❌ El BIN es inválido.")
            return

        req = requests.get(f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_code}")
        if req.status_code == 200:
            j = req.json()
            rol = user.get('role', 'Usuario')
            user_id = user_obj.id
            nombre = user_obj.first_name
            texto = f"""
<b>【〄】 BIN:</b> <code>{j['data']['bin']}</code>
<b>【〄】 Vendor:</b> <b>{j['data']['vendor']}</b>
<b>【〄】 Tipo:</b> <b>{j['data']['type']}</b>
<b>【〄】 Nivel:</b> <b>{j['data']['level']}</b>
<b>【〄】 Banco:</b> <b>{j['data']['bank']}</b>
<b>【〄】 País:</b> <b>{j['data']['country']} {j['data']['countryInfo']['emoji']}</b>
<b>【〄】 Código Tel:</b> <b>{j['data']['countryInfo']['dialCode']}</b>
<b>【〄】 Verificado por:</b> <b><a href="tg://user?id={user_id}">{nombre}</a> - {rol}</b>
<b>【〄】 BOT BY:</b> <b>@gsmdiego</b>
"""
            await gif_msg.edit_caption(texto, disable_web_page_preview=True)
        else:
            await gif_msg.edit_caption("❌ Error al obtener los datos del BIN.")

    except Exception as e:
        print(f"[Error /bin] {e}")
        try:
            await gif_msg.edit_caption("❌ Ocurrió un error al procesar el comando.")
        except:
            pass
