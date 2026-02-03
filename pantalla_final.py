# pantalla_final.py
from tkinter import Label, Button
from styles import COLOR_OK, COLOR_BOTON, COLOR_BOTON_SEC

class PantallaFinal:
    def __init__(self, root, fuentes, reiniciar_callback, salir_callback):
        self.root = root
        self.fuentes = fuentes
        self.reiniciar_callback = reiniciar_callback
        self.salir_callback = salir_callback

        self.label_msg = Label(root, text="", font=fuentes["titulo"], fg=COLOR_OK, bg="#0D1B2A", justify="center", wraplength=900)
        self.aceptar_btn = Button(root, text="Realizar otro entrenamiento", font=fuentes["boton"], fg="#FFFFFF", bg=COLOR_BOTON, width=25, pady=12, command=self.reiniciar_callback)
        self.cancelar_btn = Button(root, text="Salir", font=fuentes["boton"], fg="#FFFFFF", bg=COLOR_BOTON_SEC, width=12, pady=12, command=self.salir_callback)

    def mostrar(self, mensaje="¡Has completado todos los ejercicios del pack!\n\n¿Deseas realizar otro entrenamiento o salir?"):
        self.label_msg.config(text=mensaje)
        self.label_msg.place(x=50, y=250)
        self.aceptar_btn.place(x=150, y=420)
        self.cancelar_btn.place(x=620, y=420)

    def ocultar(self):
        self.label_msg.place_forget()
        self.aceptar_btn.place_forget()
        self.cancelar_btn.place_forget()
