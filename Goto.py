#Script que se encarga de mandar las ordendenes al turtlebot (publicando en los topics)
#para poder moverlo hasta los puntos indicados mediante la GUI

# -*- coding: utf-8 -*-

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Quaternion
import time 
from datetime import datetime
import cv2 as cv
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
import numpy as np


blue_object = False
check = False



def Subscriber():       #funcion que se subscribe a los topics 
                        #correspondientes a las coordenadas y la camara
        
    sub1 = rospy.Subscriber('/Coord_goals',Pose,callback1)
    sub2 = rospy.Subscriber("/camera/rgb/image_raw",Image,callback2)
    rospy.spin()



def callback1(data):            #callback correspondiente a subscribirnos al topic /Coord_goals
    cliente=ClientGoto()        #creamos un objeto de la clase ClientGoto
    
    cliente.x = data.position.x     #asignamos la posicion y orientacion leaida del topic
    cliente.y = data.position.y
    cliente.q0= data.orientation.x
    cliente.q3 = data.orientation.w

    cliente.Goto()              #llamamos a la funcion que mueve el robot


def callback2(data):            #callback correspondiente a la camara del turtlebot
    scan = ImgScanner()
    bridge = CvBridge()
    frame = bridge.imgmsg_to_cv2(data,"bgr8")   #convertimos la imagen para que cv2 la
                                                # pueda leer
    scan.proccess_frame(frame)




#   Clase ImgScanner que contiene:
#       -1 metodo:
#           "procces_frame" que se encarga de analizar la imagen
#
class ImgScanner:

    def proccess_frame(self,frame):     #funcion que se encarga de detectar si se detecta la señal
                                        #de obejtivo cumplido ( una tarjeta roja)
        global blue_object,check
        hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

        lower = (100,100,20)
        upper = (125,255,255)

        umbr = cv.inRange(hsv,lower,upper)

        contours,_= cv.findContours(umbr,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

        areas = [cv.contourArea(c) for c in contours]
        if areas: 
            area = np.amax(areas)
            cv.drawContours(frame,contours,np.argmax(areas),(255,0,0),3)
            if check == True:
                if  area >= 300:
                    rospy.loginfo("Area good")
                    blue_object = True
        
        cv.imshow("Azul",frame)
        cv.waitKey(3)
        


#   Clase ClientGoto que contiene:
#       -3 atributos correspondientes a las coordenadas (x,y) y la orientación del punto objetivo
#       -2 métodos; 
#             "__init__" que se encarga de crear la acción del cliente y dejar eperandolo al servidor
#             
#             "Goto" que se encarga de enviar el goal hacia el que se mueve el robot

class ClientGoto:
    x=0.0
    y=0.0
    q0=0.0
    q3=0.0

    def __init__(self):
        self.client= actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.client.wait_for_server(rospy.Duration(500))

    def Goto(self):
        #creamos un objeto de tipo MoveBaseGoal 
        #donde tiene campo Point Position y Quaternion orientation
        global check, blue_object

        goal=MoveBaseGoal()

        #rellenamos los campos correspondientes
        goal.target_pose.header.frame_id='map' #sistema de ref que usa el robot
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x=self.x
        goal.target_pose.pose.position.y=self.y
        goal.target_pose.pose.orientation.w= self.q0
        goal.target_pose.pose.orientation.w= self.q3

        #mandamos el goal 
        self.client.send_goal(goal)

        #se va comprobando el estado de la accion
        estado=self.client.get_state()

        #mientras que se este ejecutando o este pendiente
        while estado==GoalStatus.ACTIVE or estado== GoalStatus.PENDING:
            rospy.Rate(10)
            estado=self.client.get_state() #vamos mirando el estado de la accion
	    
        check = True
        
        #esperamos a que la clase ImgScanner detecte la señal de  objetivo cumplido
        spin = blue_object
        while spin == False:
            rospy.Rate(10)
            spin = blue_object

        

        if(self.client.get_result()): #si el resultado es true
            rospy.loginfo("Card detected")
            rospy.loginfo("Goal conseguido")
            check = False
            blue_object = False

if __name__=="__main__":
    
    try:
        rospy.init_node('Go_to')
        
        Subscriber() #llamamos a la funcion que se subscribe al topic

    except rospy.ROSInterruptException:
        rospy.loginfo("Ejecución detenida")

    
