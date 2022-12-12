# Script para que Tkinter ESCRIBA en PLC
import paho.mqtt.client as paho
import tkinter as tk
from tkinter import ttk

#Creación del cliente y envio de datos
broker = "localhost"
port = 1883
def true():
    client1 = paho.Client("Pruebas")
    client1.connect(broker, port)
    client1.publish("Boton", True)
def false():
    client1 = paho.Client("Pruebas")
    client1.connect(broker, port)
    client1.publish("Boton", False)

#Creación de la pantalla    
root = tk.Tk()
root.config(width=350, height=150)
root.title("Activación mediante pantalla.")

#Boton de encender
boton1 = ttk.Button(text="Encender", command=true)
boton1.place(x=50, y=50)

#Boton de apagar
boton2 = ttk.Button(text="Apagar", command=false)
boton2.place(x=200, y=50)

#Esto al final
root.mainloop()
