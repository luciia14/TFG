# pantalla_entrenamiento.py
from tkinter import Label
from styles import COLOR_CONTADOR, COLOR_BOTON, COLOR_TEXTO

class PantallaEntrenamiento:
    def __init__(self, root, fuentes):
        self.root = root
        self.fuentes = fuentes

        self.contador_label = Label(root, text="", font=fuentes["contador"], fg=COLOR_CONTADOR, bg="#0D1B2A")
        self.nombre_label = Label(root, text="", font=fuentes["boton"], fg=COLOR_BOTON, bg="#0D1B2A")
        self.feedback_label = Label(root, text="", font=fuentes["feedback"], fg=COLOR_TEXTO, bg="#0D1B2A", justify="left", wraplength=900)

    def mostrar_ejercicio(self, nombre, feedback="", segundos=0, actual=1, total=1):
        self.contador_label.config(text=f"{segundos}s")
        self.contador_label.place(x=50, y=50)

        self.nombre_label.config(text=nombre)
        self.nombre_label.place(x=50, y=120)

        self.feedback_label.config(text=f"{feedback}\nEjercicio {actual}/{total}")
        self.feedback_label.place(x=50, y=200)

    def actualizar_contador(self, segundos):
        self.contador_label.config(text=f"{segundos}s")

    def actualizar_feedback(self, texto):
        self.feedback_label.config(text=texto)

    def ocultar(self):
        self.contador_label.place_forget()
        self.nombre_label.place_forget()
        self.feedback_label.place_forget()
