import tkinter as tk
from tkinter import Label, Button
from styles import COLOR_TITULO, COLOR_BOTON, COLOR_BOTON_SEC, COLOR_OK

class PantallaPrincipal:
    # 1. Quitamos cb_custom de los parámetros
    def __init__(self, root, fuentes, cb_entrenamiento, cb_progreso, cb_logout):
        self.root = root
        self.fuentes = fuentes
        
        # 2. Asignamos solo los que quedan
        self.cb_entrenamiento = cb_entrenamiento
        self.cb_progreso = cb_progreso
        self.cb_logout = cb_logout

        self.frame = tk.Frame(root, bg="#0D1B2A")

        # --- HEADER ---
        self.header_frame = tk.Frame(self.frame, bg="#0D1B2A")
        self.header_frame.pack(fill="x", pady=15, padx=30)

        Button(self.header_frame, text="← Cerrar Sesión", font=self.fuentes["texto"], fg="#FF5252", bg="#1B3B5F", bd=0, cursor="hand2", command=self.cb_logout).pack(side="left")
        self.label_saludo = Label(self.header_frame, text="¡Hola!", font=self.fuentes["titulo"], fg=COLOR_TITULO, bg="#0D1B2A")
        self.label_saludo.pack(side="right")

        # --- CUERPO CENTRAL ---
        self.body_frame = tk.Frame(self.frame, bg="#0D1B2A")
        self.body_frame.pack(expand=True)

        Label(self.body_frame, text="¿Qué deseas hacer hoy?", font=self.fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=(0, 30))

        # Solo dejamos Entrenamiento y Progreso
        Button(self.body_frame, text="MODO ENTRENAMIENTO\n(Packs predefinidos)", font=self.fuentes["boton"], fg="#FFFFFF", bg=COLOR_BOTON, width=35, pady=10, cursor="hand2", command=self.cb_entrenamiento).pack(pady=10)
        
        Button(self.body_frame, text="MI PROGRESO Y RECOMENDACIONES\n(Estadísticas)", font=self.fuentes["boton"], fg="#FFFFFF", bg=COLOR_OK, width=35, pady=10, cursor="hand2", command=self.cb_progreso).pack(pady=10)

    # --- Acciones de Interfaz ---
    def actualizar_saludo(self, nombre):
        self.label_saludo.config(text=f"¡Hola, {nombre}!")

    def mostrar(self):
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def ocultar(self):
        self.frame.place_forget()