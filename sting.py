#RobotName: sting
from RobotRL import RobotRL

senIz = 0
senDer = 0

robot = RobotRL()
speed = 50

print(robot.getVI())
print(robot.getVD())

def go():
    robot.setVI(speed)
    robot.setVD(speed)

def back():
    robot.setVI(-speed)
    robot.setVD(-speed)

def left():
    robot.setVI(-40)
    robot.setVD(40)

def right():
    robot.setVI(40)
    robot.setVD(-40)

def stop():
    robot.setVI(0)
    robot.setVD(0)

def dontOut():
    if(robot.getColorPiso() > 90):
        stop()
        back()
        robot.esperar(1)
        left()
        robot.esperar(1)

def buscar():
    global senDer, senIz
    senIz = robot.getDI()
    senDer = robot.getVD()
    if ((senIz < 100) and (senDer < 100)):
        go()
        return
    if ((senIz == 100) and (senDer < 100)):
        right()
        return
    if ((senIz < 100) and (senDer == 100)):
        left()
        return

while robot.step():
    go()
    dontOut()
    buscar()