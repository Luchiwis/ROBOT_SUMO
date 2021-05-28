import keyboard

def moverse():
    print("moviendose")


accion = {
    "w":lambda:moverse(),
    "b":"atras",
    "c":"palcostao",
    "d":"palotrocostao"
}

while True:
    for k in accion.keys():
        try:
            if keyboard.is_pressed(k):
                accion[k]()
        except:
            pass