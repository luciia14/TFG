import customtkinter as ctk
from styles import COLOR_OK, COLOR_BOTON, COLOR_BOTON_SEC

class PantallaFinal:
    def __init__(self, root, fuentes, reiniciar_callback, salir_callback):
        self.root = root
        self.fuentes = fuentes
        self.reiniciar_callback = reiniciar_callback
        self.salir_callback = salir_callback

        # Configurar el color de fondo general de la ventana
        self.root.configure(fg_color="#0D1B2A")

        # Texto principal todavía más grande y llamativo
        self.label_msg = ctk.CTkLabel(
            root, 
            text="", 
            font=("Arial", 36, "bold"), 
            text_color="#FFFFFF", 
            fg_color="#0D1B2A", 
            bg_color="#0D1B2A",
            justify="center", 
            wraplength=950
        )
        
        # Botones gigantes y letras interiores muy grandes
        self.aceptar_btn = ctk.CTkButton(
            root, 
            text="Realizar otro entrenamiento", 
            font=("Arial", 22, "bold"), 
            text_color="#FFFFFF", 
            fg_color=COLOR_BOTON,
            hover_color="#1B4965",
            width=420,
            height=85,
            corner_radius=16,
            command=self.reiniciar_callback
        )
        
        self.cancelar_btn = ctk.CTkButton(
            root, 
            text="Salir", 
            font=("Arial", 22, "bold"), 
            text_color="#FFFFFF", 
            fg_color=COLOR_BOTON_SEC,
            hover_color="#C0392B",
            width=260,
            height=85,
            corner_radius=16,
            command=self.salir_callback
        )

    def mostrar(self, mensaje="¡Has completado todos los ejercicios del pack!\n\n¿Deseas realizar otro entrenamiento o salir?"):
        self.label_msg.configure(text=mensaje)
        
        # Texto principal colocado un poco más abajo para acercarlo a los botones
        self.label_msg.place(relx=0.5, y=190, anchor="center")
        
        # Botones situados más cerca del texto superior (y=360)
        self.aceptar_btn.place(relx=0.34, y=360, anchor="center")
        self.cancelar_btn.place(relx=0.71, y=360, anchor="center")

    def ocultar(self):
        self.label_msg.place_forget()
        self.aceptar_btn.place_forget()
        self.cancelar_btn.place_forget()