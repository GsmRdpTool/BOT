# utils/db/antispam.py

# Diccionario que simula base de datos antispam
antidb = {}

# Ejemplo de función para actualizar antispam
def update_antispam(user_id, timestamp):
    antidb[user_id] = timestamp

# Ejemplo de función para consultar antispam
def get_last_action(user_id):
    return antidb.get(user_id)
