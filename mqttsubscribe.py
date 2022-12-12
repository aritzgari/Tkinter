from tkinter import ttk
import paho.mqtt.client as mqtt
from tkinter import *

# Creación de la pantalla    
ventana = Tk()
ventana.geometry("450x250")
ventana.title("Mostrado de datos")

# Inicialización de variables.
diccionario= {}
datos = StringVar()
datos.set("No hay datos disponibles. Espere un momento. Si no se muestran los datos pasados unos minutos es que hay un error de conexión.")

# Subscripción
def on_connect(client, userdata, flags, rc):
        # Esto se muestra al conectar el código debería de ser 0
        print(f"Connected with result code {rc}")
        # El nombre del topic al que hay que conectarse.
        client.subscribe("Datos")

# Lo obtenido del mensaje
def on_message(client, userdata, msg):
        # Hay que hacer la variable global para poder sacarla de la función
        global diccionario
        #Comprobar que le llega la información
        print(f"Message received [{msg.topic}]: {msg.payload}")
        #Pasamos la información a una variable a tratar
        diccionario = {msg.topic: msg.payload}
        #Decodificar de tipo bytes a string
        diccionario = diccionario['Datos'].decode('UTF-8').replace("false","False").replace("true","True")
        #Pasar del string a diccionario
        diccionario = eval(diccionario)
        # Seteamos los datos del label con la información del diccionario
        datos.set(diccionario)
        if(bool(diccionario['Salida']))==True:
            # Fill the circle with GREED
            my_canvas.itemconfig(my_oval, fill="green")
        else:
            my_canvas.itemconfig(my_oval, fill="red")
        
# Conectar y tomar los datos
client = mqtt.Client("Pruebas")
client.on_connect = on_connect
client.on_message = on_message

# loop de escucha en este caso es con start para poder seguir ejecutando la pantalla
client.connect('127.0.0.1', 1883)
client.loop_start()

# El label cambiará de texto según lo reciba de mqtt
rotulo1 = ttk.Label(ventana, text="Datos", textvariable=datos, justify=LEFT, wraplength=398)
rotulo1.pack()

# El canvas te permite hacer un pack de cosas
my_canvas = Canvas(ventana, width=200, height=200)
my_canvas.pack()

# Crear un circulo dentro del canvas
my_oval = my_canvas.create_oval(50, 50, 100, 100)

ventana.mainloop()
