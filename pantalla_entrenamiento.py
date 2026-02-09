# pantalla_entrenamiento.py
from tkinter import Label
from styles import COLOR_CONTADOR, COLOR_BOTON, COLOR_TEXTO

class PantallaEntrenamiento:
    def __init__(self, root, fuentes):
        self.root = root
        self.fuentes = fuentes
        
        self.actual = 0
        self.total = 0

        # Fuentes personalizadas para que sean mucho más grandes
        # Si prefieres usar las de styles.py, cámbialas aquí, pero para legibilidad recomiendo:
        self.fuente_gigante = ("Helvetica", 28, "bold") 

        self.contador_label = Label(root, text="", font=fuentes["contador"], fg=COLOR_CONTADOR, bg="#0D1B2A")
        self.nombre_label = Label(root, text="", font=fuentes["boton"], fg=COLOR_BOTON, bg="#0D1B2A")
        
        # Configuramos el feedback_label para párrafos centrados y letra grande
        self.feedback_label = Label(
            root, 
            text="", 
            font=self.fuente_gigante, 
            fg="#00FFCC", # Color cian brillante para alta visibilidad
            bg="#0D1B2A", 
            justify="center", # Centra el texto de cada párrafo
            wraplength=900    # Permite que el texto baje si es muy largo
        )

    def mostrar_ejercicio(self, nombre, feedback="", segundos=0, actual=1, total=1):
        """Prepara y muestra la pantalla con los datos iniciales"""
        self.actual = actual
        self.total = total
        
        # Contador arriba a la izquierda
        self.contador_label.config(text=f"{segundos}s")
        self.contador_label.place(x=50, y=50)

        # Nombre del ejercicio arriba (como subtítulo)
        self.nombre_label.config(text=f"{nombre.upper()} ({self.actual}/{self.total})")
        self.nombre_label.place(x=50, y=130)

        # Feedback centrado en pantalla
        self.feedback_label.config(text=feedback.upper())
        self.feedback_label.place(relx=0.5, rely=0.55, anchor="center")

    def actualizar_contador(self, segundos):
        self.contador_label.config(text=f"{segundos}s")

    def actualizar_feedback(self, texto_nuevo):
        """Actualiza el mensaje. El MAIN ya envía los saltos de línea con \\n"""
        # Solo mostramos el texto de corrección para maximizar el tamaño
        self.feedback_label.config(text=texto_nuevo.upper())

    def ocultar(self):
        self.contador_label.place_forget()
        self.nombre_label.place_forget()
        self.feedback_label.place_forget()