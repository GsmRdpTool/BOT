import random, string
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta

def generar_clave(plan: str) -> str:
    prefijo = "SONG"
    numero = ''.join(random.choices(string.digits, k=5))
    codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    plan_upper = plan.upper()
    return f"{prefijo}-{numero}-{codigo}-{plan_upper}"

@Client.on_message(filters.command("gkey"))
async def generar_key(client, message: Message):
    if message.from_user.id not in [7731790583]:  # Admin ID
        return await message.reply("⛔ Solo administradores pueden generar claves.")
    
    partes = message.text.split()
    if len(partes) != 4:
        return await message.reply("Uso correcto: /gkey <plan> <usos> <días_expiración>\nEj: /gkey premium 5 30")

    plan, usos_str, dias_str = partes[1].lower(), partes[2], partes[3]
    if plan not in ["premium", "diamond"]:
        return await message.reply("Planes válidos: premium, diamond")

    try:
        usos = int(usos_str)
        dias = int(dias_str)
    except:
        return await message.reply("❌ Usos y días deben ser enteros.")

    clave = generar_clave(plan)
    fecha_expira = datetime.utcnow() + timedelta(days=dias)

    await client.db.keys.insert_one({
        "key": clave,
        "plan": plan,
        "usos": usos,
        "expires_at": fecha_expira
    })

    texto = (
        f"Welcome to 𝑺𝒐𝒏𝒈 𝑱𝒊-𝒘𝒐𝒐 {plan.capitalize()} users\n"
        "━━━━━━━━━━━━━━\n"
        f"【〄】 Key ⮞ [`{clave}`](https://t.me/{client.me.username}?start=claim_{clave}) <—- Click key\n"
        f"【〄】 Days ⮞ [{dias}]\n"
        f"【〄】 Rank ⮞ {plan.capitalize()}\n"
        f"【〄】 Credits ⮞ [0]\n"
        "━━━━━━━━━━━━━━━━━\n"
        "To see how many days, credits, and antispam you have, type /myplan"
    )

    await message.reply(texto, disable_web_page_preview=True)

@Client.on_message(filters.command("claim"))
async def reclamar_key(client, message: Message):
    partes = message.text.split()
    if len(partes) != 2:
        return await message.reply("Uso correcto: /claim <clave>")

    clave = partes[1]
    key_data = await client.db.keys.find_one({"key": clave})
    if not key_data:
        return await message.reply("❌ Clave inválida o inexistente.")

    ahora = datetime.utcnow()
    if "expires_at" in key_data and ahora > key_data["expires_at"]:
        await client.db.keys.delete_one({"key": clave})
        return await message.reply("❌ Esta clave ha expirado.")

    # Actualizar usuario: plan, fecha reclamación, mantener o inicializar créditos
    user = await client.db.users.find_one({"_id": message.from_user.id})
    if user and "credits" in user:
        credits = user["credits"]
    else:
        credits = 0

    await client.db.users.update_one(
        {"_id": message.from_user.id},
        {"$set": {
            "plan": key_data["plan"],
            "claimed_date": ahora,
            "credits": credits  # No modificamos créditos aquí
        }},
        upsert=True
    )

    if key_data["usos"] > 1:
        await client.db.keys.update_one({"key": clave}, {"$inc": {"usos": -1}})
    else:
        await client.db.keys.delete_one({"key": clave})

    await message.reply(f"✅ Clave aceptada. Plan asignado: **{key_data['plan'].upper()}**.")

@Client.on_message(filters.command("myplan"))
async def my_plan(client, message: Message):
    user = await client.db.users.find_one({"_id": message.from_user.id})
    if not user:
        return await message.reply("❌ No tienes plan asignado. Usa /claim para activar uno.")

    plan = user.get("plan", "free").capitalize()
    credits = user.get("credits", 0)
    claimed_date = user.get("claimed_date")

    texto = (
        f"Welcome to 𝑺𝒐𝒏𝒈 𝑱𝒊-𝒘𝒐𝒐 {plan} users\n"
        "━━━━━━━━━━━━━━\n"
        f"【〄】 Tu Plan ⮞ {plan}**\n"
        f"【〄】 Créditos ⮞ [{credits}]\n"
    )

    if claimed_date:
        if isinstance(claimed_date, list) and claimed_date:
            claimed_date = claimed_date[0]

        if isinstance(claimed_date, str):
            try:
                claimed_date = datetime.fromisoformat(claimed_date)
            except ValueError:
                try:
                    claimed_date = datetime.strptime(claimed_date, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    claimed_date = None

        if isinstance(claimed_date, datetime):
            expiracion = claimed_date + timedelta(days=30)
            texto += f"【〄】 Expira el ⮞ {expiracion.strftime('%d/%m/%Y %H:%M UTC')}\n"
        else:
            texto += "【〄】 Fecha de expiración: formato desconocido\n"
    else:
        texto += "【〄】 Fecha de expiración: No disponible\n"

    texto += (
        "━━━━━━━━━━━━━━━━━\n"
        "Para ver más detalles, usa /status\n"
    )

    await message.reply(texto, disable_web_page_preview=True)
