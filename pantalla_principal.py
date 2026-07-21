import customtkinter as ctk
import tkinter as tk
from styles import COLOR_TITULO, COLOR_BOTON, COLOR_BOTON_SEC, COLOR_OK

class PantallaPrincipal:
    def __init__(self, root, fuentes, cb_entrenamiento, cb_progreso, cb_logout):
        self.root = root
        self.fuentes = fuentes
        
        self.cb_entrenamiento = cb_entrenamiento
        self.cb_progreso = cb_progreso
        self.cb_logout = cb_logout

        # Contenedor base de toda la ventana
        self.frame = ctk.CTkFrame(root, fg_color="#0D1B2A", corner_radius=0)

        # ==========================================
        # 1. ENCABEZADO (HEADER)
        # ==========================================
        self.header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(25, 10), padx=40)

        # Título del Sistema (Izquierda)
        header_left = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_left.pack(side="left")

        ctk.CTkLabel(
            header_left, 
            text="ENTRENAMIENTO POSTURAL", 
            font=ctk.CTkFont(size=28, weight="bold"), 
            text_color="#80D8FF"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header_left, 
            text="Panel Principal de Control", 
            font=ctk.CTkFont(size=15), 
            text_color="#A0AAB2"
        ).pack(anchor="w")

        # Saludo al usuario (Derecha, en grande)
        self.label_saludo = ctk.CTkLabel(
            self.header_frame, 
            text="¡Hola!", 
            font=ctk.CTkFont(size=32, weight="bold"), 
            text_color=COLOR_TITULO
        )
        self.label_saludo.pack(side="right")

        # Línea divisora superior neón
        ctk.CTkFrame(self.frame, height=2, fg_color="#1E3A5F").pack(fill="x", padx=40, pady=(10, 15))

        # ==========================================
        # 2. CUERPO CENTRAL (DISEÑO LIMPIO)
        # ==========================================
        self.body_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.body_frame.pack(expand=True, fill="both", padx=40, pady=5)

        # Pregunta principal
        ctk.CTkLabel(
            self.body_frame, 
            text="¿Qué deseas hacer hoy?", 
            font=ctk.CTkFont(size=48, weight="bold"), 
            text_color="#FFFFFF"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            self.body_frame, 
            text="", 
            font=ctk.CTkFont(size=15), 
            text_color="#80D8FF"
        ).pack(pady=(0, 25))

        # Tipografía para botones
        font_btn = ctk.CTkFont(size=21, weight="bold")

        # Botón 1: Modo Entrenamiento
        self.btn_entrenamiento = ctk.CTkButton(
            self.body_frame, 
            text="MODO ENTRENAMIENTO\n(Packs predefinidos)", 
            font=font_btn, 
            fg_color="#0D1B2A", 
            border_color="#80D8FF", 
            border_width=2, 
            text_color="#FFFFFF", 
            hover_color="#16324F", 
            corner_radius=20, 
            width=580, 
            height=95, 
            command=self.cb_entrenamiento
        )
        self.btn_entrenamiento.pack(pady=12)

        # Botón 2: Mi Progreso
        self.btn_progreso = ctk.CTkButton(
            self.body_frame, 
            text="MI PROGRESO Y RECOMENDACIONES\n(Estadísticas)", 
            font=font_btn, 
            fg_color="#0D1B2A", 
            border_color="#80D8FF", 
            border_width=2, 
            text_color="#FFFFFF", 
            hover_color="#16324F", 
            corner_radius=20, 
            width=580, 
            height=95, 
            command=self.cb_progreso
        )
        self.btn_progreso.pack(pady=12)

        # Recuadro informativo de Consejo (Ampliado y adaptativo)
        self.tip_card = ctk.CTkFrame(
            self.body_frame, 
            fg_color="#102238", 
            border_color="#80D8FF", 
            border_width=1, 
            corner_radius=15
        )
        self.tip_card.pack(pady=(20, 10), padx=20, fill="x")

        ctk.CTkLabel(
            self.tip_card, 
            text="💡 CONSEJO POSTURAL: Mantén la espalda erguida y realiza descansos cada 45 minutos de trabajo.", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            text_color="#80D8FF",
            wraplength=750
        ).pack(pady=14, padx=20)

        # ==========================================
        # 3. PIE DE PÁGINA (BOTÓN CERRAR SESIÓN ABAJO A LA IZQUIERDA)
        # ==========================================
        # Línea divisora inferior
        ctk.CTkFrame(self.frame, height=2, fg_color="#1E3A5F").pack(fill="x", padx=40, pady=(10, 0))

        self.footer_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.footer_frame.pack(fill="x", side="bottom", pady=(10, 25), padx=40)

        # Botón ubicado en la esquina inferior izquierda
        self.btn_logout = ctk.CTkButton(
            self.footer_frame, 
            text="Cerrar Sesión", 
            font=ctk.CTkFont(size=15, weight="bold"), 
            fg_color="transparent", 
            hover_color="#1E3A5F", 
            text_color="#FF5252",
            width=140,
            height=35,
            corner_radius=12,
            command=self.cb_logout
        )
        self.btn_logout.pack(side="left")

    # --- Acciones de Interfaz ---
    def actualizar_saludo(self, nombre):
        self.label_saludo.configure(text=f"¡Hola, {nombre}!")

    def mostrar(self):
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def ocultar(self):
        self.frame.place_forget()