import os
import time
from pyrogram import Client, filters
from telegraph import upload_file
from values import BOT_USERNAME
from values import maindb 

@Client.on_message(filters.command(
    ['takeme', 'register', 'register ', f'register@{BOT_USERNAME}', f'takeme@{BOT_USERNAME}', f'purchase@{BOT_USERNAME}'], 
    prefixes=['.', '/', '!'], 
    case_sensitive=False
) & filters.text)
async def register(Client, message):
    try:
        msg = await message.reply_text("<b>Espera, recopilando tu información...</b>", reply_to_message_id=message.id)

        find = maindb.find_one({"_id": message.from_user.id})
        if find is None:
            # Obtener foto de perfil o imagen por defecto
            if message.from_user.photo is None:
                userimage = "https://te.legra.ph/file/8692b409921efe361831f.png"
            else:
                user_image_path = f"./userimage/{message.from_user.id}.jpg"
                await Client.download_media(message=message.from_user.photo.big_file_id, file_name=user_image_path)
                tlink = upload_file(user_image_path)
                userimage = f"https://telegra.ph{tlink[0]}"
                os.remove(user_image_path)

            # Crear registro nuevo
            mydict = {
                "_id": message.from_user.id,
                "id": message.from_user.id,
                "username": message.from_user.username,
                "plan": "Free Plan",
                "role": "Free User",
                "status": "F",
                "credits": 0,
                "image": userimage
            }
            maindb.insert_one(mydict)
            antidb.set(message.from_user.id, int(time.time()))

            with open('users.txt', 'a+') as file:
                file.write(str(message.from_user.id) + "\n")

            await msg.edit_text("<b>Has sido registrado como usuario gratuito.</b>", disable_web_page_preview=True)

        else:
            await msg.edit_text("<b>Ya estás registrado.</b>", disable_web_page_preview=True)

    except Exception as e:
        print(f"Error en /register: {e}")
