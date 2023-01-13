#Script que se encarga de subscribirse al topic /clicked_point, en el cual
#publica RVIZ con la herramienta Publish Point, para poder almacenar
#los puntos establecidos en un fichero .txt

import rospy
from geometry_msgs.msg import PointStamped
from datetime import datetime
from math import *


#   Clase Coord que contiene:
#       -3 atributos correspondientes a las coordenadas (x,y) y oreintacion de los puntos seleccionados en RVIZ
#       -6 métodos; 
#             "__init__" que se encarga de subscribirse al topic /clicked_point
#             
#             "orientacion" que se encarga de obtener la orientación pasada por parametro a cuaternios
#
#             "escribirFichero" que se encarga de almacenar las coordenadas obtenidas a traves del topic
#              /clicked_point en el fichero coor_gazebo.txt
#
#             "callback" del subscriber al topic /clicked_point que se encarga de almacenar en los vectores x[] 
#              e y[] las coordenadas de los puntos publicados en ese topic
#
#              "shutdown" que se encarga de informar cuando la ejecución se ha detenido
#
#              "main" que se encarga de llamar al método orientacion y al método escribirFichero 

class Coord():
    x =[]
    y =[]

    def __init__(self):
        rospy.on_shutdown(self.shutdown)
        rospy.Subscriber('/clicked_point',PointStamped,self.callback)

    def orientacion(self, x1,y1,x2,y2): 
        quat=[]                                 #array donde se almacenaran los cuaternios
        v = [x2-x1, y2-y1]                      #vector de direccion del eje x nuevo (cuando se mueve)
        prodEscalar= v[0]*1 + v[1]*0            #producto escalar entre la dir nueva del eje x y la dir del eje x de la base (1,0) 
        mod_v= sqrt(v[0]*v[0] + v[1]*v[1])      #se calcula el modulo del vector director v
        ang=acos(prodEscalar/mod_v)             #calculamos el angulo entre los dos vectores en RADIANES
        quat=[cos(ang/2),0,0,sin(ang/2)]        #se calcula el cuaternio [q0,q1,q2,q3], donde q0 es la componente escalar

        #borramos el contenido de self.x y self.y
        self.x[:]=[]
        self.y[:]=[]

        return quat

    def escribirFichero(self, x, y, cuaternio):
        f=open("coord_lab.txt", "a")
        f.write(str(x))
        f.write(";")
        f.write(str(y))
        f.write(";")
        f.write(str(cuaternio[0]))
        f.write(";")
        f.write(str(cuaternio[1]))
        f.write(";")
        f.write(str(cuaternio[2]))
        f.write(";")
        f.write(str(cuaternio[3]))
        f.write("\n")
        f.close()

    def callback(self,msg):
        self.x.append(msg.point.x) 
        self.y.append(msg.point.y)

    def shutdown(self):
        rospy.loginfo("Ejecución detenida")
        

    def main(self):
        if(len(self.x) == 2):                   # Comprobamos que sean dos por que utilizamos el primer
                                                #click para la pos y el segundo para la orient
            posx = self.x[0]
            posy = self.y[0]
            cuater= self.orientacion(self.x[0],self.y[0],self.x[1],self.y[1]) 
            self.escribirFichero(posx,posy,cuater)

if __name__=='__main__':
    try: 
        Actual = Coord()                                        #creamos un objeto de la clase
        while not rospy.is_shutdown():                          #mientras no se detenga la ejecuión desde el terminal
            rospy.init_node('goal_publisher', anonymous=True)   #iniciamos el nodo
            Actual.main()                                       #de esta manera el self de la funcion main tenga los atributos de la clase Coord
            rospy.sleep(1)

    except rospy.ROSInterruptException:                         #se informa de que la ejecución ha sido detenida
        rospy.loginfo("Ejecución detenida")
        