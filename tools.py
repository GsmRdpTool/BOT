import random

ccs = []

def cc_gen(bin, mes, ano, cvv):
    bin = bin.replace("x", "0")
    for _ in range(1):  # genera 1 tarjeta por llamada
        cc = ""
        for c in bin:
            if c == "x":
                cc += str(random.randint(0, 9))
            else:
                cc += c
        mes_final = mes if mes != "x" else str(random.randint(1, 12)).zfill(2)
        ano_final = ano if ano != "x" else str(random.randint(25, 30))
        cvv_final = cvv if cvv != "x" else str(random.randint(100, 999))
        ccs.append(f"{cc}|{mes_final}|{ano_final}|{cvv_final}")
