import time
import re
import json
import string
import random
import requests
from requests.exceptions import ProxyError
from pyrogram import Client, filters
import pymongo
import redis
from defs import get_time_taken, get_email

@Client.on_message(filters.command(["zc"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
async def stripe_charge(Client, message):
    try:
        started_time = time.time()
       
                
        msg = await message.reply_text(
            f"""<b>【〄】</b> GATE: <b>STRIPE CHARGE [2]</b>
<b>【〄】</b> RESULT: <b>CHECKING YOUR INPUT</b>
<b>【〄】</b> PROCESS: <b>□□□□□□□□□□ 0% </b>
<b>【〄】</b> CHECKING BY: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a></b>
<b>【〄】</b> TIME TAKING: {get_time_taken(started_time)}'s
<b>【〄】</b> BOT BY: <b>@gsmdiego</b>""",
            reply_to_message_id=message.id
        )

        mongourl = "mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        maindb = pymongo.MongoClient(mongourl)["mills"]["users"]
        user = maindb.find_one({"_id": message.from_user.id})

        if not user:
            return await msg.edit_text("<b>Register Yourself To Use Me. Hit /takeme To Register Yourself</b>")
        if user['status'] == "F" or int(user['credits']) == 0:
            return await msg.edit_text("<b>Buy a paid plan to use this gate. Use /buy to see premium plans</b>")
        if user['status'] == "P" and int(user['credits']) < 2:
            await msg.edit_text("<b>You consumed all your credits. Use /buy to get more. You are now demoted to Free User</b>")
            maindb.update_one(
                {'_id': message.from_user.id},
                {'$set': {"plan": "Free Plan", "role": "Free User", "status": "F", "credits": 0}}
            )
            return

        r = redis.Redis(
            host="redis-17574.c10.us-east-1-4.ec2.redns.redis-cloud.com",
            port=17574,
            password="MILUDQruVeqxBoO0G0eLdAP9V45R0td2",
        )
        last_time = r.get(message.from_user.id)
        if last_time:
            spam_time = int(time.time()) - int(last_time.decode())
            if user['status'] == "P" and spam_time < 20:
                return await msg.edit_text(f"<b> AntiSpam: try again after {20 - spam_time}'s</b>")

        if message.reply_to_message:
            message.text = message.reply_to_message.text

        input_data = re.findall(r"[0-9]+", message.text)

        if len(input_data) < 3:
            return await msg.edit_text("Your Card Is Empty or Incorrect")

        if len(input_data) == 4:
            cc, mes, ano, cvv = input_data
        elif len(input_data) == 3:
            cc = input_data[0]
            mes = input_data[1][:2]
            ano = input_data[1][2:]
            cvv = input_data[2]
        else:
            return await msg.edit_text("Invalid card format.")

        if len(mes) > 2:
            mes, cvv = cvv, mes

        if int(cc[0]) in [1, 2, 7, 8, 9, 0] or len(cc) not in [15, 16]:
            return await msg.edit_text("Your Card Is Invalid")
        if not (len(mes) == 2 and '01' <= mes <= '12'):
            return await msg.edit_text("Your Card Month Is Incorrect")
        if len(ano) not in [2, 4]:
            return await msg.edit_text("Your Card Year Is Incorrect")
        if (cc.startswith("3") and len(cvv) != 4) or not (3 <= len(cvv) <= 4):
            return await msg.edit_text("Your Card Cvv Is Incorrect")

        lista = f"{cc}|{mes}|{ano}|{cvv}"
        bin_ = cc[:6]
        session = requests.Session()
        session.proxies = {
            "http": "http://bfpiydpo-rotate:jommyvzkwcdl@p.webshare.io:80/",
            "https": "http://bfpiydpo-rotate:jommyvzkwcdl@p.webshare.io:80/",
        }

        bin_info = session.get(f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_}")
        if bin_info.status_code != 200 or not json.loads(bin_info.text).get('result'):
            return await msg.edit_text("Your Card's BIN Is Invalid")

        with open("bannedbin.txt", "r") as b:
            if str(message.chat.id) + "\n" in b.readlines():
                return await msg.edit_text("Your Card's Bin Is Banned")

        # Aquí continuarías con la construcción del payload y envío a Stripe
        await msg.edit_text("<b>✔ Datos verificados correctamente. Falta terminar el envío a Stripe.</b>")
        r.set(message.from_user.id, int(time.time()))

    except Exception as e:
        await message.reply_text(f"<b>❌ Error: {e}</b>")
