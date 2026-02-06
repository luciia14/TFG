# pantalla_entrenamiento.py
from tkinter import Label
from styles import COLOR_CONTADOR, COLOR_BOTON, COLOR_TEXTO

class PantallaEntrenamiento:
    def __init__(self, root, fuentes):
        self.root = root
        self.fuentes = fuentes
        
        # Inicializamos variables de estado para evitar AttributeError
        self.actual = 0
        self.total = 0

        self.contador_label = Label(root, text="", font=fuentes["contador"], fg=COLOR_CONTADOR, bg="#0D1B2A")
        self.nombre_label = Label(root, text="", font=fuentes["boton"], fg=COLOR_BOTON, bg="#0D1B2A")
        self.feedback_label = Label(root, text="", font=fuentes["feedback"], fg=COLOR_TEXTO, bg="#0D1B2A", justify="left", wraplength=900)

    def mostrar_ejercicio(self, nombre, feedback="", segundos=0, actual=1, total=1):
        """Prepara y muestra la pantalla con los datos iniciales del ejercicio"""
        # IMPORTANTE: Guardamos el estado para que actualizar_feedback pueda usarlo
        self.actual = actual
        self.total = total
        
        # Configurar y posicionar etiquetas
        self.contador_label.config(text=f"{segundos}s")
        self.contador_label.place(x=50, y=50)

        self.nombre_label.config(text=nombre)
        self.nombre_label.place(x=50, y=120)

        # Mostrar el feedback inicial junto con el progreso
        texto_inicial = f"{feedback}\nEjercicio {self.actual}/{self.total}"
        self.feedback_label.config(text=texto_inicial)
        self.feedback_label.place(x=50, y=200)

    def actualizar_contador(self, segundos):
        """Actualiza solo el número de segundos en pantalla"""
        self.contador_label.config(text=f"{segundos}s")

    def actualizar_feedback(self, texto_nuevo):
        """Actualiza el mensaje de corrección manteniendo el contador de ejercicio"""
        # Ahora self.actual y self.total siempre están definidos
        texto_completo = f"{texto_nuevo}\nEjercicio {self.actual}/{self.total}"
        self.feedback_label.config(text=texto_completo)

    def ocultar(self):
        """Esconde todos los elementos de esta pantalla"""
        self.contador_label.place_forget()
        self.nombre_label.place_forget()
        self.feedback_label.place_forget()