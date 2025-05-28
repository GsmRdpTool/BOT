import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message

def generar_clave(plan: str) -> str:
    # Genera 5 dígitos numéricos
    numeros = ''.join(random.choices(string.digits, k=5))
    # Genera 5 letras mayúsculas
    letras = ''.join(random.choices(string.ascii_uppercase, k=5))
    # Construye la clave en formato requerido
    return f"GSM-{numeros}-{letras}-{plan.upper()}"

@Client.on_message(filters.command("gkey"))
async def generar_key(client, message: Message):
    if message.from_user.id not in [7731790583]:  # Admin ID
        return await message.reply("⛔ Solo administradores pueden generar claves.")
    
    partes = message.text.split()
    if len(partes) != 3:
        return await message.reply("Uso correcto: /gkey <plan> <usos>\nEj: /gkey premium 5")

    plan, usos = partes[1].lower(), partes[2]
    if plan not in ["premium", "diamond"]:
        return await message.reply("Planes válidos: premium, diamond")

    try:
        usos = int(usos)
    except:
        return await message.reply("El número de usos debe ser entero.")

    clave = generar_clave(plan)

    await client.db.keys.insert_one({"key": clave, "plan": plan, "usos": usos})

    texto = (
        "Welcome to 𝑺𝒐𝒏𝒈 𝑱𝒊-𝒘𝒐𝒐 \n"
        f"【〄】Clave Generada {plan.capitalize()}\n"
        "━━━━━━━━━━━━━━\n"
        f"【〄】Key ⮞ `{clave}`\n"
        f"【〄】Plan ⮞ {plan.capitalize()}\n"
        f"【〄】Usos ⮞ {usos}]\n"
        "━━━━━━━━━━━━━━\n"
        f"Recuerda compartir esta clave solo con usuarios confiables."
    )
    await message.reply(texto)

@Client.on_message(filters.command("claim"))
async def reclamar_key(client, message: Message):
    partes = message.text.split()
    if len(partes) != 2:
        return await message.reply("Uso correcto: /claim <clave>")

    clave = partes[1]
    key_data = await client.db.keys.find_one({"key": clave})
    if not key_data:
        return await message.reply("❌ Clave inválida o agotada.")

    await client.db.users.update_one(
        {"_id": message.from_user.id},
        {"$set": {"plan": key_data["plan"]}},
        upsert=True
    )

    if key_data["usos"] > 1:
        await client.db.keys.update_one({"key": clave}, {"$inc": {"usos": -1}})
    else:
        await client.db.keys.delete_one({"key": clave})

    texto = (
        "【〄】Clave Aceptada【〄】\n"
        "━━━━━━━━━━━━━━\n"
        f"【〄】Ahora tienes el plan: **{key_data['plan'].capitalize()}**\n"
        "━━━━━━━━━━━━━━\n"
        "Disfruta de tus beneficios."
    )
    await message.reply(texto)

@Client.on_message(filters.command("myplan"))
async def my_plan(client, message: Message):
    user = await client.db.users.find_one({"_id": message.from_user.id})
    plan = user.get("plan", "free") if user else "free"
    usos = user.get("credits", 0) if user else 0  # Asumiendo que tienes un campo "credits" en users

    texto = (
        "【〄】Información de tu plan【〄】\n"
        "━━━━━━━━━━━━━━\n"
        f"【〄】Tu Plan ⮞ {plan.capitalize()}**\n"
        f"【〄】Créditos ⮞ {usos}**\n"
        "━━━━━━━━━━━━━━\n"
        "Usa los comandos para aprovechar tus beneficios:\n"
        "• /help para ver comandos\n"
        "• /status para ver detalles\n"
    )
    await message.reply(texto)
