#SCRIPT QUE SE ENCARGA DE CREAR LA GUI PARA
#QUE EL USUARIO PUEDA SELECCIONAR LOS PUNTOS A 
#LOS QUE QUIERE DIRIGIR EL TURTLEBOT
#O LAS TRAYECTORIAS PREDEFINIDAS QUE QUIERE QUE SIGA

from tkinter import *
import tkinter as tk
import os
from PIL import Image, ImageTk

#Parametros de configuración de la GUI
NAME_WINDOW="Mapa Farmacia"
FONT_BUTTON="Roman 10 italic bold"


#EVENTOS de los botones de la GUI
#Botón Goto que se encarga de lanzar el script Goto.py
def Goto(): 

    os.system('gnome-terminal -x python3 Goto.py')          #lanzamos el goto

#Botón punto1 que se encarga de lanzar el script leerFichero pasandole como 
#argumento por la línea de comandos el número de coordenada correspondiente (1)
def punto1():

    os.system('gnome-terminal -x python3 leerFichero.py 0')   #lanzamos el leerFichero

#Botón punto2 que se encarga de lanzar el script leerFichero pasandole como 
#argumento por la línea de comandos el número de coordenada correspondiente (2)
def punto2():

    os.system('gnome-terminal -x python3 leerFichero.py 1')   #lanzamos el leerFichero

#Botón punto3 que se encarga de lanzar el script leerFichero pasandole como 
#argumento por la línea de comandos el número de coordenada correspondiente (3)
def punto3():

    os.system('gnome-terminal -x python3 leerFichero.py 2')   #lanzamos el leerFichero

#Botón punto4 que se encarga de lanzar el script leerFichero pasandole como 
#argumento por la línea de comandos el número de coordenada correspondiente (4)
def punto4():

    os.system('gnome-terminal -x python3 leerFichero.py 3')   #lanzamos el leerFichero

#Botón trayectoria1 que se encarga de lanzar el script leerFichero pasandole como 
#argumentos por la línea de comandos los números de coordenadas correspondientes (0-1-2)
def trayectoria1():

    os.system('gnome-terminal -x python3 leerFichero.py 0 1 2')   #lanzamos el leerFichero

#Botón trayectoria2 que se encarga de lanzar el script leerFichero pasandole como 
#argumentos por la línea de comandos los números de coordenadas correspondientes (0-1-2)
def trayectoria2():

    os.system('gnome-terminal -x python3 2 leerFichero.py 1 2 0')   #lanzamos el leerFichero

#Botón trayectoria3 que se encarga de lanzar el script leerFichero pasandole como 
#argumentos por la línea de comandos los números de coordenadas correspondientes (0-1-2)
def trayectoria3():

    os.system('gnome-terminal -x python3 3 leerFichero.py 2 1 0')   #lanzamos el leerFichero







#VENTANA PRINCIPAL
window=Tk()
window.title(NAME_WINDOW)       #le asignamos un titulo a la ventana principal
window.geometry("750x750")      #le asignamos un tamaño a la ventana principal



#ADD IMAGE FILE; establecemos la imagen del mapa como fondo de la ventana
"""image = Image.open('background.pgm')
copy_of_image = image.copy()
background_img = ImageTk.PhotoImage(image)"""
background_img = PhotoImage(file = "background.pgm")
background_img = background_img.zoom(2)
background = Label(window, image=background_img)

#background.pack(fill=BOTH, expand=YES)
#background.bind('<Configure>', resize_image)
background.place(x=0, y=0)


#ADD BUTTON; añadimos el boton correspondiente al Goto en el frame1
frame1=Frame(window)
frame1.pack(pady=10)

but_goto = Button(frame1, fg="white", bg="red", font=FONT_BUTTON, text="GoTo", command=Goto)
but_goto.grid(row=0, column=0)


#ADD BUTTON; añadimos los botones correspondientes a los puntos 1, 2, 3 y 4 en el frame 2
frame2=Frame(window)
frame2.pack(pady=10)

but_p1 = Button(frame2, fg="white", bg="black", font=FONT_BUTTON, text="Habitación 0", command=punto1)
but_p1.grid(row=0, column=0)

but_p2 = Button(frame2, fg="white", bg="black", font=FONT_BUTTON, text="Habitación 1", command=punto2)
but_p2.grid(row=0, column=1)

but_p3 = Button(frame2, fg="white", bg="black", font=FONT_BUTTON, text="Habitación 2", command=punto3)
but_p3.grid(row=0, column=3)

but_p4 = Button(frame2, fg="white", bg="black", font=FONT_BUTTON, text="Habitación 3", command=punto4)
but_p4.grid(row=0, column=4)

#ADD BUTTON; añadimos los botones correspondientes a las trayectorias 1, 2 y 3 en el frame 3
frame3=Frame(window)
frame3.pack(pady=10)


but_tray1 = Button(frame3, bg="white",font=FONT_BUTTON, text="Trayectoria 1", command=trayectoria1)
but_tray1.grid(row=0, column=0)

but_tray2 = Button(frame3, bg="white", font=FONT_BUTTON, text="Trayectoria 2", command=trayectoria2)
but_tray2.grid(row=0, column=1)

but_tray3 = Button(frame3, bg="white", font=FONT_BUTTON, text="Trayectoria 3", command=trayectoria3)
but_tray3.grid(row=0, column=3)


#Se muestra la pantalla y se espera a que el usuario interactue con ella
window.mainloop()

