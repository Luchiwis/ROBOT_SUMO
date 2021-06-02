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
        self.funcionActual = {}

        #test
        self.flipflop = True
    
    def detener(self):
        self.vel = 0
        self.setVI(self.vel)
        self.setVD(self.vel)

    def rotar(self, angulo):
        """
        10rep > +-180grad
        """
        angulo %= 360 #normalizar angulo

        if angulo>=0:
            f = lambda :(self.setVI(self.vel),self.setVD(-self.vel)) #horario
        else:
            f = lambda :(self.setVI(-self.vel),self.setVD(self.vel)) #antihorario

        
        ciclos = (angulo*10)/180 #ciclos
        
        self.repetir(f, ciclos)

    def repetir(self, funcion=None, ciclos=None):
        """repite una funcion x cantidad de ciclos
            sin argumentos simplemente actualiza un ciclo
            si se ordena una funcion mientras otra se ejecuta: se interrumpe la anterior
        """
        if (funcion and ciclos):
            #se ordeno una funcion nueva
            self.funcionActual = {
                "func":funcion,
                "start":self.cicloActual,
                "duration":ciclos
                }

        elif (self.funcionActual):
            #no se ordeno ninguna funcion, se sigue con la anterior si hay
            
            if (((self.cicloActual) - (self.funcionActual["start"])) >= (self.funcionActual["duration"])):
                #si ya supero su duracion se termina la funcion
                self.funcionActual = None
                self.detener()
            else:
                #si no; ejecutar
                self.funcionActual["func"]()
        

            
    
    def update(self):
        """abstraccion del loop llevado a un metodo"""
        
        #test
        if self.flipflop:
            self.flipflop = False
            self.rotar(180)

        self.repetir()

        self.cicloActual +=1
        print(f"ciclo: {self.cicloActual}")
        




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




while bondiola.step():
    
    bondiola.update()