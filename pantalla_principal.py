# pantalla_principal.py
import tkinter as tk
from tkinter import Label, Button
from styles import COLOR_TITULO, COLOR_BOTON, COLOR_BOTON_SEC, COLOR_OK

class PantallaPrincipal:
    def __init__(self, root, fuentes, cb_entrenamiento, cb_custom, cb_progreso, cb_logout):
        self.root = root
        self.fuentes = fuentes
        
        # Callbacks (funciones que se ejecutarán al pulsar los botones)
        self.cb_entrenamiento = cb_entrenamiento
        self.cb_custom = cb_custom
        self.cb_progreso = cb_progreso
        self.cb_logout = cb_logout

        # Contenedor principal que ocupará toda la ventana para poder alinear el header
        self.frame = tk.Frame(root, bg="#0D1B2A")

        # ==========================================
        # HEADER (Barra superior)
        # ==========================================
        self.header_frame = tk.Frame(self.frame, bg="#0D1B2A")
        self.header_frame.pack(fill="x", pady=15, padx=30)

        # Botón Cerrar Sesión (Izquierda)
        Button(self.header_frame, text="← Cerrar Sesión", font=self.fuentes["texto"], fg="#FF5252", bg="#1B3B5F", bd=0, cursor="hand2", command=self.cb_logout).pack(side="left")

        # Saludo personalizado (Derecha)
        self.label_saludo = Label(self.header_frame, text="¡Hola!", font=self.fuentes["titulo"], fg=COLOR_TITULO, bg="#0D1B2A")
        self.label_saludo.pack(side="right")

        # ==========================================
        # CUERPO CENTRAL (Botones)
        # ==========================================
        self.body_frame = tk.Frame(self.frame, bg="#0D1B2A")
        self.body_frame.pack(expand=True)

        Label(self.body_frame, text="¿Qué deseas hacer hoy?", font=self.fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=(0, 30))

        Button(self.body_frame, text="MODO ENTRENAMIENTO\n(Packs predefinidos)", font=self.fuentes["boton"], fg="#FFFFFF", bg=COLOR_BOTON, width=35, pady=10, cursor="hand2", command=self.cb_entrenamiento).pack(pady=10)
        
        Button(self.body_frame, text="CUSTOMIZAR NUEVO ENTRENAMIENTO\n(Crea tu rutina)", font=self.fuentes["boton"], fg="#FFFFFF", bg=COLOR_BOTON_SEC, width=35, pady=10, cursor="hand2", command=self.cb_custom).pack(pady=10)

        Button(self.body_frame, text="MI PROGRESO Y RECOMENDACIONES\n(Estadísticas)", font=self.fuentes["boton"], fg="#FFFFFF", bg=COLOR_OK, width=35, pady=10, cursor="hand2", command=self.cb_progreso).pack(pady=10)

    # --- Acciones de Interfaz ---
    def actualizar_saludo(self, nombre):
        """Actualiza el texto del header con el nombre del usuario"""
        self.label_saludo.config(text=f"¡Hola, {nombre}!")

    def mostrar(self):
        """Muestra la pantalla ocupando toda la ventana"""
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def ocultar(self):
        self.frame.place_forget()