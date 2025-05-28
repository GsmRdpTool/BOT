from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from functools import wraps

# Diccionario global para registrar handlers de callback_data
_callback_handlers = {}

def callback(data: str):
    """
    Decorador para registrar funciones que manejan un callback_data específico.
    """
    def decorator(func):
        _callback_handlers[data] = func

        @wraps(func)
        async def wrapper(client: Client, callback_query: CallbackQuery):
            await func(client, callback_query)
        return wrapper
    return decorator

async def handle_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    handler = _callback_handlers.get(data)
    if handler:
        await handler(client, callback_query)
    else:
        # Opcional: responde si no hay handler definido
        await callback_query.answer("Acción no definida", show_alert=True)
