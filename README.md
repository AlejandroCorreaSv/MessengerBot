<h1 align="center"> MessengerBot</h1>

<p align="center">
  <img width="600" height="200" src="https://user-images.githubusercontent.com/61583836/210230646-43c5e377-0e0e-4604-a9f1-759a582ca440.png">
</p>


# Índice:file_folder:

* [Descripción del proyecto realizado](#descripcion-del-proyecto-realizado)

* [Pre-Requisitos](#pre-reqiusitos)

* [Aplicaciones del Proyecto](#aplicaciones-del-proyecto)

* [Guia de Uso](#guia-de-uso)

## Descripción del proyecto realizado:page_with_curl:
Aplicacion para utilizar al turtlebot en modo de mensajero, de manera que sea capaz de moverse a unas coordenadas especificas dentro de un entorno conocido. 

## Pre-Requisitos:arrow_down:
Para utilizar la aplicacion en un turtlebot real, solamente es preciso tener ros noetic instalado, sin embargo, para realizar pruebas en simulacion se necesita instalar tambien los paquetes referentes al turtlebot3. Para ello utilizamos los siguientes comandos.

```
sudo apt install ros-noetic-desktop-full
sudo apt isntall ros-noetic-turtlebo
```

Para copiar este repositorio de Github en su dispositvo copie la siguiente linea.
```
git clone https://github.com/AlejandroCorreaSv/MessengerBot
```

## Aplicaciones del Proyecto

El enfoque principal de este proyecto fue el de utilizarse en hopitales donde el turtlebot haga viajes desde la farmacia hacia las distintas habitaciones, llevando medicamentos a los pacientes. Sin embargo, esta es una aplicacion especifica que se le ha dado pero no es la unica, ya que este se puede utilizar en cualquier entorno y con cualquier finalidad

## Guia de Uso:video_game:

### Simulacion:computer:

Primeramente, para abrir la simulacion de nuestro robot debemos introducir lso siguientes comandos en dos terminales distintas.

* Primera terminal
  ```
  export TURTLEBOT3_MODEL=waffle
  roslaunch turtlebot3_gazebo turtlebot3_house.launch
  ```
* Segunda terminal
  ```
  export TURTLEBOT3_MODEL=waffle
  roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$ PATH_TO_REPOSITORY/MessengerBot/house.yaml
  ```
  
  Una vez ejecutado esto, se abriran dos aplicaciones, gazebo y RVIZ, en la primera estara la simulacion del entorno en la que se encunetra nuestro robot, en al segundo se ecuntra la herramienta que proporciona ROS para la visualizacion de todas las herramientas que usa nuestro robot como su laser, el mapa, los sistemas de referencia etc.
  
  Con la simulacion en marcha ya podremos ejecutar nuestra aplicacion. Para ello introduzca el siguiente comando en una terminal de la carpeta que contenga al repositorio.
  
  ```
  python3 Interfaz_farmacia.py
  ```
  
  Esto abrira la siguiente aplicacion
<p align="center">
  <img width="377" height="377" src="https://user-images.githubusercontent.com/61583836/210241606-5649c3fe-ed95-47d7-a6e5-488eb2637a30.png">
</p>

Para que la aplicacion funcione, lo primero que hay que hacer es pulsar el boton cuya etiqueta es "GoTo", que lanzara el nodo que realiza el movimiento del robot. Teniendo esto en marcha, se puede proceder a enviar el ordenardor a cualquiera de los puntos establecidos o que realize una trayectoria, con los botones correspondientes.

### Turtlebot real:turtle:

La manera de utilizar la aplicacion con un turtlebot real es la misma que en simulacion, pero en vez de ejecutar gazebo, debemos conectarnos a nuestro turtlebot.

```
ssh turtlebot@ipturtlebot
```
Una vez dentro del robot, deberemos lanzar los siguentes launch dentro de este.
```
roslaunch turtlebot_bringup minimal.launch
roslaunch turtlebot_bringup hokuyo_ust10lx.launch
```
Con el robot ya operativo, debemos lanzar el nodo que nos permite utilizar el algoritmo de navecaion de ROS y abra una pestaña de RVIZ con toda la informacion, pero esta vez real. Tambien desde dentro del robot.

```
export TURTLEBOT_3D_SENSOR=astra
roslaunch turtlebot_navigation amcl_demo.launch map_file:=/home/turtlebot/FICHERO_DEL_MAPA.yaml
```

Una vez hecho todo esto, ya podemos utilizar la aplicacion igual que antes.


### Guardar objetivos:round_pushpin:

Para guardar los puntos a los que queremos mover el turtlebot hemos desarrollado un script, que junto a RVIZ, permite realizar esta tarea de forma comoda. Para ello debemos tener abierto la aplicacion de RVIZ con nuestro mapa en ella y ejecutar en un terminal de la carpeta del repositorio el siguiente comando.

```
python3 coordenadas.py
```

Con esto ya podemos guardar nuestros puntos, para ello utilizaremos la herramienta de RVIZ "Publish Point". Para guardar un punto, simplemente pincharemos en la herramienta y haremos click en el punto del mapa que queramos guardar, seguidamente, volveremos a seleccionar la herramienta, y pincharemos en la direccion que queramos que tenga este objetivo, es decir, hacia donde estara enfocado el turtlebot una vez llegue el objetivo.



<p align="center">
  <img width="600" height="437" src="https://user-images.githubusercontent.com/61583836/210245576-7a548c6f-4479-48ff-9b7b-8c6ecf37c46c.jpg">
</p>

