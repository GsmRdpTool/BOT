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
        return [line.strip() for line in f]

def admins():
    with open('files/admins.txt', 'r') as f:
        return [line.strip() for line in f]

def verified_gps():
    with open('files/groups.txt', 'r') as f:
        return [line.strip() for line in f]

# --- Mensajes del sistema ---
use_not_registered = "<b>Register Yourself To Use Me. Hit /register To Register Yourself</b>"
buy_premium = "<b>Take Paid Plan To Use Me In Private Mode. Hit /buy To See My Premium Plans</b>"
free_user = "<b>Buy paid plan to use this gate. Hit /buy to see my premium plans</b>"

# --- Generador de tarjetas ---
ccs = []

def cc_gen(cc, mes='x', ano='x', cvv='x', amount='x'):
    amount = int(amount) if amount != 'x' else 15
    genrated = 0
    while genrated < amount:
        genrated += 1
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
    elif 11 <= h < 16:
        return "Good Afternoon <b>🌣</b>"
    elif 17 <= h < 19:
        return "Good Evening <b>🌅</b>"
    elif 19 <= h < 24:
        return "Good Night <b>🌃</b>"
    return "Hello"

def save_live(lista):
    with open('files/cvvs/cvv.txt', 'a+') as file:
        file.seek(0)
        if str(lista) + "\n" not in file.readlines():
            file.write(str(lista) + "\n")

def save_ccn(lista):
    with open('files/cvvs/ccn.txt', 'a+') as file:
        file.seek(0)
        if str(lista) + "\n" not in file.readlines():
            file.write(str(lista) + "\n")

# --- Validación principal ---
def main(cc, mes, ano, cvv):
    req = requests.Session()

    # Datos aleatorios de usuario
    r = requests.get("https://randomuser.me/api/?nat=us&inc=name,location")
    rd = r.json()["results"][0]
    first, last = rd['name']['first'], rd['name']['last']
    address = f"{rd['location']['street']['number']} {rd['location']['street']['name']}"
    city, state, zip_code = rd['location']['city'], rd['location']['state'], rd['location']['postcode']
    phone = "225" + ''.join(random.choices("0123456789", k=7))
    email = get_email()
    user = get_username()

    # Info del BIN
    bin_res = requests.get(f"https://zdgghhhvvdds.herokuapp.com/api/{str(cc)}")
    vendor = bin_res.json().get("data", {}).get("vendor", "").lower()

    # Paso 1: obtener cbid
    headers1 = {
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://buddlycrafts.com',
        'referer': 'https://buddlycrafts.com/checkout/step1/',
        'user-agent': 'Mozilla/5.0'
    }
    step1 = req.post("https://buddlycrafts.com/checkout/step1/", headers=headers1, data=f"email={user}%40gmail.com")
    match = re.search(r'/checkout/step2/(.*)/', step1.text)
    if not match:
        return None

    cbid = match.group(1)

    return {
        'vendor': vendor,
        'cbid': cbid,
        'name': f"{first} {last}",
        'address': address,
        'city': city,
        'state': state,
        'zip': zip_code,
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
