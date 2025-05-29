from pyrogram import Client, filters
from values import lista  # función para separar el texto del mensaje

# Define aquí los IDs de tus administradores como enteros:
admins = [7731790583, 7731790583]  # <-- Cambia por los IDs reales de tus admins

@Client.on_message(filters.command('addbin', prefixes=['.', '/', '!'], case_sensitive=False) & filters.text)
async def banbin(client, message):
    try:
        user_id = message.from_user.id

        # Verificamos si el usuario es admin
        if user_id not in admins:
            await message.reply_text("<b>No tienes permisos para usar este comando.</b>", reply_to_message_id=message.id)
            return

        # Obtenemos argumentos (debe venir el BIN después del comando)
        args = lista(message.text)  # lista devuelve lista de palabras
        if len(args) < 2:
            await message.reply_text("<b>Por favor, especifica un BIN válido.</b>", reply_to_message_id=message.id)
            return

        bin_code = args[1][:6]  # Solo primeros 6 dígitos del BIN

        # Leer BINs baneados desde archivo
        try:
            with open('files/bannedbin.txt', 'r') as f:
                banned_bins = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            # Si el archivo no existe, se asume vacío
            banned_bins = []

        # Verificamos si el BIN ya está baneado
        if bin_code in banned_bins:
            await message.reply_text("<b>Este BIN ya está baneado.</b>", reply_to_message_id=message.id)
            return

        # Añadimos el BIN al archivo
        with open('files/bannedbin.txt', 'a') as f:
            f.write(bin_code + "\n")

        await message.reply_text("<b>BIN baneado correctamente.</b>", reply_to_message_id=message.id)

    except Exception as e:
        print(f"Error en comando addbin: {e}")
        await message.reply_text("<b>Ocurrió un error al procesar el comando.</b>", reply_to_message_id=message.id)
