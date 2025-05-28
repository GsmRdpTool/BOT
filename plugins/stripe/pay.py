from pyrogram import Client, filters
import stripe
import os

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "sk_test_XXXXXXXXXXXXXXXXXXXX")
stripe.api_key = STRIPE_API_KEY

@Client.on_message(filters.command("pago") & filters.private)
async def stripe_pay_command(client, message):
    amount_cents = 1000  # 10 USD en centavos
    currency = "usd"
    description = f"Pago solicitado por {message.from_user.first_name} ({message.from_user.id})"

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            payment_method_types=["card"],
            description=description,
        )
        client_secret = payment_intent.client_secret
        await message.reply(
            f"Pago creado con éxito.\n\n"
            f"Client Secret:\n`{client_secret}`\n\n"
            "Usa este client_secret en tu frontend para completar el pago."
        )
    except Exception as e:
        await message.reply(f"❌ Error creando pago:\n{e}")
