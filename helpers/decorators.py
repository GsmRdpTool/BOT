from functools import wraps
from pyrogram.types import Message
from pyrogram import Client, filters

def requiere_plan(permitidos: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message: Message):
            user = await mdb.users.find_one({"_id": message.from_user.id})
            plan = user.get("plan", "Free") if user else "Free"
            if plan.lower() not in [p.lower() for p in permitidos]:
                return await message.reply("🚫 Este comando requiere un plan: " + " / ".join(permitidos))
            return await func(client, message)
        return wrapper
    return decorator
