# Script para que Tkinter ESCRIBA y LEA en PLC
from tkinter import ttk
import paho.mqtt.client as mqtt
from tkinter import *

# Iniciación de variables.
broker = "localhost"
port = 1883
diccionario = {}

# Activar el nodo del flow de node-red.
def true():
    client1 = mqtt.Client("Pruebas")
    client1.connect(broker, port)
    client1.publish("Boton", True)

# Desactivar el nodo del flow de node-red.
def false():
    client1 = mqtt.Client("Pruebas")
    client1.connect(broker, port)
    client1.publish("Boton", False)

# Lanzar esta función al conectar.
def on_connect(client, userdata, flags, rc):
    # Esto se muestra al conectar el código debería de ser 0.
    #print(f"Connected with result code {rc}")
    # El nombre del topic al que hay que conectarse.
    client.subscribe("Datos")

# Lo obtenido del mensaje.
def on_message(client, userdata, msg):
    # Hay que hacer la variable global para poder sacarla de la función.
    global diccionario
    # Comprobar que le llega la información.
    print(f"Message received [{msg.topic}]: {msg.payload}")
    # Pasamos la información a una variable a tratar.
    diccionario = {msg.topic: msg.payload}
    # Decodificar de tipo bytes a string
    diccionario = diccionario['Datos'].decode(
        'UTF-8').replace("false", "False").replace("true", "True")
    # Pasar del string a diccionario.
    diccionario = eval(diccionario)
    # Seteamos los datos del label con la información del diccionario.
    contadorfun="Valor del contador 1: " + str(diccionario['Real'])
    contadorfun2 = "Valor del contador 2: " + str(diccionario['Entero'])
    datos.set(diccionario)
    contador.set(contadorfun)
    contador2.set(contadorfun2)
    if(bool(diccionario['Salida'])) == True:
        # Poner verde.
        my_canvas.itemconfig(my_oval, fill="green")
    else:
        # Poner rojo.
        my_canvas.itemconfig(my_oval, fill="red")

# Creación de la pantalla.
root = Tk()
root.geometry("370x220")
root.title("Mostrado de datos")

# Inicializar variable para almacenar los datos para Tkinter.
datos = StringVar()
datos.set("No hay datos disponibles. Espere un momento. Si no se muestran los datos pasados unos minutos es que hay un error de conexión.")

# Contador 1 y 2
contador =IntVar()
contador.set(0)
contador2 = IntVar()
contador2.set(0)

# Conectar y tomar los datos.
client = mqtt.Client("Pruebas")
client.on_connect = on_connect
client.on_message = on_message

# loop de escucha en este caso es con start para poder seguir ejecutando la pantalla.
client.connect('127.0.0.1', 1883)
client.loop_start()

# El label cambiará de texto según lo reciba de mqtt.
rotulo1 = ttk.Label(root, text="Datos", textvariable=datos)
rotulo1.place(x=0,y=0)

# El label cambiará de texto según lo reciba de mqtt.
rotulo2 = ttk.Label(root, text="Datos", textvariable=contador)
rotulo2.place(x=0, y=30)
 
# El label cambiará de texto según lo reciba de mqtt.
rotulo3 = ttk.Label(root, text="Datos", textvariable=contador2)
rotulo3.place(x=0, y=60)

# El canvas te permite hacer un pack de cosas.
my_canvas = Canvas(root, width=80, height=80)
my_canvas.place(x=130, y=90)

# Boton de encender
boton1 = ttk.Button(root, text="Encender", command=true)
boton1.place(x=60, y=170)

# Boton de apagar
boton2 = ttk.Button(root, text="Apagar", command=false)
boton2.place(x=210, y=170)

# Crear un circulo dentro del canvas
my_oval = my_canvas.create_oval(10, 10, 80, 80, width=2)

# Este loop permite ejecutar de forma infinita la pantalla de tkinter
root.mainloop()