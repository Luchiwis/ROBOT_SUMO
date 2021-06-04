#RobotName: lucio
"""
NOTA: NO USAR TILDES NI EN LOS COMENTARIOS PORQUE SE CAGA TOD0
"""


from RobotRL import RobotRL


class Bondiola(RobotRL):
    def __init__(self):
        super().__init__()
        self.vel = 100
        self.cicloActual = 0
        self.ACELERACION = 10
        self.cola = []  # cola de procesos[f,f2,f3,f4...]

    """funciones fisicas:
    sin Executefunc la funcion se agrega a la cola, con Executefunc se ejecuta
    cada vez que la funcion es llamada desde afuera, se espera que no se use el parametro executeFunc
    por lo tanto la funcion se agrega a la cola y es gestionada por ejecutarProcesos mas adelante
    """

    def print_estadisticas(self):
        # print("velocidad: ",self.getVI(),self.getVD())
        print("colorPiso: ",self.getColorPiso())
        print("distancia: ",self.getDI(),self.getDD())
        print("bumpers: ",self.getBI(),self.getBD())


    def detener(self, executeFunc=False):
        if executeFunc:
            # ejecutar la funcion
            self.vel = 0
            self.setVI(self.vel)
            self.setVD(self.vel)
        else:
            # Agregar funcion a la cola
            info = (self.detener, ())
            self.cola.append(info)

    def avanzar(self, ciclos, executeFunc=False):
        if executeFunc:
            # ejecutar la funcion
            """
            avanzar con una aceleracion aceptable
            """
            # aceleracion
            if not self.vel:
                self.vel = 1
            elif self.vel < 100:
                self.vel += self.ACELERACION
            elif self.vel > 100:
                self.vel = 100

            self.setVI(self.vel)
            self.setVD(self.vel)
            # print(f"velocidad: {self.vel}")
        else:
            # si el metodo fue llamado por fuera de la clase
            info = (self.avanzar, (ciclos,))
            for _ in range(ciclos):
                # agregar funcion a la cola por x cantidad de ciclos
                self.cola.append(info)
            # agregar funcion para detenerse a la cola
            self.cola.append((self.detener, ()))

    def retroceder(self, ciclos, executeFunc=False):
        if executeFunc:
            # ejecutar la funcion
            """
            avanzar con una aceleracion aceptable
            """
            # aceleracion
            if not self.vel:
                self.vel = 1
            elif self.vel < 100:
                self.vel += self.ACELERACION
            elif self.vel > 100:
                self.vel = 100

            self.setVI(-self.vel)
            self.setVD(-self.vel)
            # print(f"velocidad: {self.vel}")
        else:
            # si el metodo fue llamado por fuera de la clase
            info = (self.retroceder, (ciclos,))
            for _ in range(ciclos):
                # agregar funcion a la cola por x cantidad de ciclos
                self.cola.append(info)
            # agregar funcion para detenerse a la cola
            self.cola.append((self.detener, ()))

    def rotar(self, angulo, executeFunc=False):
        #FIXME: precision (sacrificar velocidad por precision)
        VEL_ROTACION = 50
        if executeFunc:
            # ejecutar la funcion
            
            self.vel = 0
            if angulo >= 0:
                # angulo = (angulo%360)
                (self.setVI(VEL_ROTACION), self.setVD(-VEL_ROTACION))  # horario
            else:
                # angulo = -(angulo%360)
                (self.setVI(-VEL_ROTACION), self.setVD(VEL_ROTACION))  # antihorario

        else:
            # si el metodo fue llamado por fuera de la clase
            CICLOS_180 = 40*27//VEL_ROTACION    #regla de 3 inversa
            ciclos = (abs(angulo)*CICLOS_180)//180  #regla de 3 simple
            info = (self.rotar, (angulo,))  # funcion en formato de cola
            for _ in range(ciclos):
                # agregar funcion a la cola por x cantidad de ciclos
                self.cola.append(info)
            # agregar funcion para detenerse al final de la cola
            self.cola.append((self.detener, ()))


    """
    funciones internas
    """

    def ejecutarProcesos(self):
        """
        cuando se llama una funcion externamente, por default, se guarda esa informacion en la cola de funciones y luego
        desde esta funcion se decide cuando debe ejecutarse.
        para ejecutarla se ingresa True en el parametro executeFunc

        formato de una funcion en cola:
        cola = [(nameFunc, (arg1,arg2,arg3))]
        """
        if (self.cola):
            # si hay procesos en cola
            funcion = self.cola[0][0]
            argumentos = self.cola[0][1]
            # ejecuta la ultima funcion con los argumentos desempaquetados de la tupla. True significa que la accion debe ejecutarse
            funcion(*argumentos, True)
            self.cola.pop(0)    #eliminar el proceso actual de la cola
            # print(f"ejecutando el proceso {funcion.__name__}, quedan {len(self.cola)} procesos en cola")

    def abortar(self):
        """aborta todos los procesos en cola"""
        self.cola = []



    def update(self):  # loop
        self.cicloActual += 1
        # print(f"ciclo: {self.cicloActual}")

        self.ejecutarProcesos()



bondiola = Bondiola()
#FIXME: arreglar parte logica
# def buscar():
#         global di, dd
#         di = bondiola.getDI()
#         dd = bondiola.getDD()
#         print("Sensor",dd)
#         if ((di < 100) and (dd < 100)):
#             bondiola.avanzar(30)
#             print("adelante 1")
            
#         elif ((di == 100) and (dd < 100)):
#             bondiola.rotar(30)
#             print("adelante")
            
#         elif ((di < 100) and (dd == 100)):
#             bondiola.rotar(-30)
#             print("girar")
            
#         elif ((di == 100) and (dd == 100)):
#             bondiola.rotar(20)
#             print("adelante",dd)
             
# test

def interrupciones():
    pisoBlanco = bondiola.getColorPiso() > 70
    pisoGris = bondiola.getColorPiso() in range(30,70)



    if pisoBlanco:
        bondiola.abortar()
        bondiola.rotar(180)
    elif pisoGris:
        bondiola.abortar()
        bondiola.rotar(90)

    
        
inicio = 0

while bondiola.step():
    
        
    bondiola.update()
    


        