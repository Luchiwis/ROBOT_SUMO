#RobotName: lucio
"""
NOTA: NO USAR TILDES NI EN LOS COMENTARIOS PORQUE SE CAGA TOD0

TODO:
    modificar la funcion "repetir" para poder ejecutar mas de una funcion en paralelo;
    crear la funcion "interrumpir" que con un parametro se pueda elegir que funcion interrumpir;
    terminar el test de input manual;
"""


from RobotRL import RobotRL
import keyboard

class Bondiola(RobotRL):
    def __init__(self):
        super().__init__()
        self.vel = 100
        self.cicloActual = 0
        self.ACELERACION = 1.5
        # self.repeticionActual = {}
        self.cola = []  #cola de procesos[f,f2,f3,f4...]

    #funciones fisicas
    def detener(self, executeFunc=False):    #sin Executefunc la funcion se agrega a la cola, con Executefunc se ejecuta
        if executeFunc:
            #ejecutar la funcion
            self.vel = 0
            self.setVI(self.vel)
            self.setVD(self.vel)
        else:
            #Agregar funcion a la cola
            info = (self.detener, ())
            self.cola.append(info)

    def avanzar(self, ciclos, executeFunc=False):    #sin Executefunc la funcion se agrega a la cola, con Executefunc se ejecuta
        if executeFunc:
            #ejecutar la funcion
            """
            avanzar con una aceleracion aceptable
            """
            #aceleracion
            if not self.vel:
                self.vel = 1
            elif self.vel<100:
                self.vel *= self.ACELERACION
            elif self.vel>100:
                self.vel = 100
            
            self.setVI(self.vel)
            self.setVD(self.vel)
            print(f"velocidad: {self.vel}")
        else:
            #si el metodo fue llamado por fuera de la clase
            info = (self.avanzar, (ciclos,))
            for _ in range(ciclos):
                self.cola.append(info)              #agregar funcion a la cola por x cantidad de ciclos
            self.cola.append((self.detener, ()))      #agregar funcion para detenerse a la cola

    def rotar(self, angulo, executeFunc=False):  #sin Executefunc la funcion se agrega a la cola, con Executefunc se ejecuta
        if executeFunc:
            #ejecutar la funcion

            angulo %= 360 #normalizar angulo
            self.vel = 0
            if angulo>=0:
                (self.setVI(100),self.setVD(-100)) #horario
            else:
                (self.setVI(-100),self.setVD(100)) #antihorario
        
            # self.repetir(f, ciclos)
        else:
            #si el metodo fue llamado por fuera de la clase
            ciclos = (angulo*10)//180 #ciclos
            info = (self.rotar, (angulo,))
            for _ in range(ciclos):
                self.cola.append(info)  #agregar funcion a la cola por x cantidad de ciclos
            self.cola.append((self.detener, ()))      #agregar funcion para detenerse a la cola

            

    def ejecutarProcesos(self):
        if (self.cola):         #(not self.repeticionActual) and 
            #si no hay procesos en ejecucion y hay procesos en cola

            """
            cuando se llama una funcion externamente, por default, se guarda esa informacion en la cola de funciones y luego
            desde esta funcion se decide cuando debe ejecutarse

            formato de una funcion en cola:
            cola = [(nameFunc, (arg1,arg2,arg3))]

            """
            funcion = self.cola[0][0]
            argumentos = self.cola[0][1]
            funcion(*argumentos, True) #ejecuta la ultima funcion con los argumentos desempaquetados de la tupla. True significa que la accion debe ejecutarse
            self.cola.pop(0)
            print(f"ejecutando el proceso {funcion.__name__}, quedan {len(self.cola)} procesos en cola")
            # print(f"repeticion actual:{self.repeticionActual}")

    
    def update(self):   #loop

        # self.repetir()
        self.ejecutarProcesos()

        print(f"ciclo: {self.cicloActual}")
        self.cicloActual +=1

        
        


        




"""
def actualizar_acciones_manuales():
    accion = {
    "w":"recto",
    "a":"izquierda",
    "s":"retroceder",
    "d":"derecha"}

    for k in accion.keys():
        try:
            if keyboard.is_pressed(k):
                accion[k]()
            else:
                detener()
        except:
            pass
"""

bondiola = Bondiola()



#test
flipflop = 0

while bondiola.step():

    bondiola.update()
    
    #test
    if (flipflop==0):
        flipflop = 1
        bondiola.rotar(90)
    # if (flipflop == 1):
    #     # flipflop = 2
    #     print(flipflop)
    #     bondiola.avanzar(30)
    