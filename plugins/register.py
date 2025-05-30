import os
import time
from pyrogram import Client, filters
from telegraph import upload_file
from values import BOT_USERNAME, maindb
from utils.db.antispam import update_antispam

@Client.on_message(filters.command(
    ['takeme', 'register', f'register@{BOT_USERNAME}', f'takeme@{BOT_USERNAME}', f'purchase@{BOT_USERNAME}'],
    prefixes=['.', '/', '!'],
    case_sensitive=False
) & filters.text)
async def register(Client, message):
    try:
        msg = await message.reply_text("<b>Espera, recopilando tu información...</b>", reply_to_message_id=message.id)

        user_id = message.from_user.id
        username = message.from_user.username or "SinUsername"
        find = await maindb.users.find_one({"_id": user_id})

        if find is None:
            os.makedirs("userimage", exist_ok=True)
            userimage = "https://te.legra.ph/file/8692b409921efe361831f.png"

            try:
                photos = await Client.get_profile_photos(user_id)
                if photos.total_count > 0:
                    path = f"userimage/{user_id}.jpg"
                    await Client.download_media(photos[0].file_id, file_name=path)

                    # CORREGIDO: no usar 'await' con función síncrona
                tgraph = upload_file(path)
                if tgraph:
                    userimage = f"https://telegra.ph{tgraph[0]['src']}"

                    os.remove(path)
            except Exception as e:
                print(f"[Foto de perfil] Error: {e}")

            new_user = {
                "_id": user_id,
                "id": user_id,
                "username": username,
                "plan": "Free Plan",
                "role": "Free User",
                "status": "F",
                "credits": 0,
                "image": userimage
            }

            await maindb.users.insert_one(new_user)
            update_antispam(user_id, int(time.time()))

            with open('users.txt', 'a+', encoding='utf-8') as f:
                f.write(f"{user_id}\n")

            await msg.edit_text("<b>Has sido registrado como usuario gratuito.</b>", disable_web_page_preview=True)
        else:
            await msg.edit_text("<b>Ya estás registrado.</b>", disable_web_page_preview=True)

    except Exception as e:
        print(f"Error en /register: {e}")
        await message.reply_text(f"<b>Error al registrar:</b> <code>{str(e)}</code>")
