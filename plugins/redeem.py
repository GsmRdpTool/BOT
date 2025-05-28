from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta

@Client.on_message(filters.command("redeem"))
async def canjear_clave(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2:
        return await message.reply("❌ Uso correcto: `/redeem <clave>`")

    key = args[1].strip().upper()
    user_id = message.from_user.id

    clave = await mdb.keys.find_one({"_id": key})
    if not clave:
        return await message.reply("❌ Clave inválida o inexistente.")
    
    if clave.get("claimed_by"):
        return await message.reply("❌ Esta clave ya ha sido canjeada.")

    # Marcar como canjeada
    await mdb.keys.update_one(
        {"_id": key},
        {"$set": {"claimed_by": user_id, "claimed_at": datetime.utcnow()}}
    )

    dias = clave["dias"]
    tipo = clave["tipo"].capitalize()

    expire_date = datetime.utcnow() + timedelta(days=dias)

    await mdb.users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "role": tipo,
                "plan": tipo,
                "claimed_date": datetime.utcnow(),
                "expire_days": dias
            }
        },
        upsert=True
    )

    await message.reply(f"✅ Clave canjeada con éxito.\n\n🎫 Plan: `{tipo}`\n⏳ Válido por: `{dias}` días.")
