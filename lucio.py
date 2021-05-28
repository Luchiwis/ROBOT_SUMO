#RobotName: Lucio
from RobotRL import RobotRL

robot = RobotRL()

velocidad = 100

di = 0
dd = 0

def recto():
    print("recto")
    robot.setVI(velocidad)
    robot.setVD(velocidad)

def retroceder():
    robot.setVI(-velocidad)
    robot.setVD(-velocidad)

def irIzquierda():
    robot.setVI(-velocidad)
    robot.setVD(velocidad)

def irDerecha():
    robot.setVI(velocidad)
    robot.setVD(-velocidad)

def parar():
    robot.setVI(0)
    robot.setVD(0)

def noCaer():
    if (robot.getColorPiso() > 90):
        retroceder()
        robot.esperar(2)
        irIzquierda()
        robot.esperar(1)

"""funciones manuales de lucio"""



def moverse(direccion):
    pass

import keyboard
def actualizar_acciones_manuales():
    accion = {
    "w":recto,
    "a":"izquierda",
    "s":retroceder,
    "d":"derecha"
}

    for k in accion.keys():
        try:
            if keyboard.is_pressed(k):
                accion[k]()
        except:
            pass











while robot.step():
    # noCaer()


    actualizar_acciones_manuales()