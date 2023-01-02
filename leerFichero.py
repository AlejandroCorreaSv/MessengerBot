#SCRIPT QUE SE ENCARGA DE LEER EL FICHERO .txt, 
#QUE CONTIENE ALMACENADAS LAS COORDENADAS DE LOS 
#PUNTOS PREVIAMENTE ESTABLECIDOS, EN FUNCIÓN DE 
#LA SELECCIÓN DEL USUARIO A TRAVÉS DE LA INTERFÁZ

import sys
import rospy
from geometry_msgs.msg import Pose
from datetime import datetime
import time

pub=rospy.Publisher('/Coord_goals',Pose,queue_size=10)      #publicamos en el topic /Coord_goals 

#   Clase Posicion que contiene:
#       -6 atributos correspondientes a las coordenadas (x,y) y a las orientaciones (x,y,z,w) del punto
#       -3 métodos; 
#             "Publish" que se encarga de publicar en el topic /Coord_goals los atributos de la clase
#             
#             "leerFichero" que se encarga de abrir el fichero .txt y almacenar en los atributos de la
#              clase las coordenadas correspondientes segun lo que haya seleccionado el usuario en la 
#              interfáz. Una vez se ha extraido una coordenada del fichero .txt se llama al método Publish
#              explicado anteriormente. 
#
#              "shutdown" que se encarga de informar cuando la ejecución se ha detenido


class Posicion():

    x=0.0
    y=0.0
    q0=0.0
    q1=0.0
    q2=0.0
    q3=0.0


    def Publish(self):
        pose_msg=Pose()
        pose_msg.position.x=self.x
        pose_msg.position.y=self.y
        pose_msg.orientation.x=self.q0
        pose_msg.orientation.y=self.q1
        pose_msg.orientation.z=self.q2
        pose_msg.orientation.w=self.q3

        pub.publish(pose_msg)

    def leerFichero(self):
        rate=rospy.Rate(1)
        f = open("/home/alejandro/Git/MessengerBot/coord_gazebo.txt")
        
        lineas=f.readlines() #guardamos las lineas que hay en el fichero para poder recorrerlo posteriormente
        f.close()
        

        for i in range(1,len(sys.argv)):     
            numCoord = int(sys.argv[i])
            
            
            frase=lineas[numCoord].strip()  #extraemos la linea numCoord borrando los espacios y los \n del string

            if(frase!= ""):                 #comprobamos que no sea una linea en blanco
                                            #Extraemos cada componente del string obtenido del fichero .txt, los cuales estan separados por ;
                self.x=float(frase.partition(";")[0])
                self.y=float(frase.partition(";")[2].partition(";")[0])
                
                orientacion=frase.partition(";")[2].partition(";")[2]

                self.q0=float(orientacion.partition(";")[0])
                self.q1=float(orientacion.partition(";")[2].partition(";")[0])
                self.q2=float(orientacion.partition(";")[2].partition(";")[2].partition(";")[0])
                self.q3=float(orientacion.partition(";")[2].partition(";")[2].partition(";")[2].partition(";")[0])
                
                self.Publish()              #llamamos al metodo publish para mandar los datos extraidos

            rate.sleep()

    def shutdown(self):
        rospy.loginfo("Ejecución detenida")
        


if __name__=='__main__':
    Goals=Posicion()                                #creamos un objeto de la clase Posicion
    try:
        rospy.init_node('coord', anonymous=True)    #iniciamos el nodo coord
        

        
        Goals.leerFichero()                         #llamamos al método de la clase leerFichero



    except rospy.ROSInterruptException:             #se informa de que la ejecución ha sido detenida en caso de error
        rospy.loginfo("Ejecución detenida")
