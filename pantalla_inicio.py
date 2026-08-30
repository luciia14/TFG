import customtkinter as ctk
import tkinter as tk
from styles import COLOR_TITULO, COLOR_BOTON, COLOR_BOTON_SEC
from packs import exercise_packs


class PantallaInicio:
    def __init__(self, root, fuentes, on_pack_seleccionado, cb_volver=None):
        self.root = root
        self.fuentes = fuentes
        self.on_pack_seleccionado = on_pack_seleccionado
        self.cb_volver = cb_volver

        # Contenedor base de toda la pantalla
        self.frame = ctk.CTkFrame(root, fg_color="#0D1B2A", corner_radius=0)


        self.header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(20, 10), padx=45)

        # Botón de Flecha Circular Grande
        self.btn_volver = ctk.CTkButton(
            self.header_frame, 
            text="←", 
            font=ctk.CTkFont(size=26, weight="bold"), 
            fg_color="transparent", 
            hover_color="#1E3A5F", 
            text_color="#80D8FF",
            width=48,
            height=48,
            corner_radius=24,
            command=self.volver
        )
        self.btn_volver.pack(side="left")

        # Título de la sección
        ctk.CTkLabel(
            self.header_frame, 
            text="MÓDULOS DE ENTRENAMIENTO", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color="#80D8FF"
        ).pack(side="right")

        # Línea divisora superior
        ctk.CTkFrame(self.frame, height=1, fg_color="#1E3A5F").pack(fill="x", padx=45, pady=(5, 15))

        ctk.CTkLabel(
            self.frame, 
            text="¿Qué entrenamiento deseas realizar?", 
            font=ctk.CTkFont(size=28, weight="bold"), 
            text_color="#FFFFFF"
        ).pack(pady=(5, 15))

        self.scroll_container = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="transparent",
            scrollbar_button_color="#1E3A5F",
            scrollbar_button_hover_color="#80D8FF",
            width=620
        )
        self.scroll_container.pack(expand=True, fill="both", padx=40, pady=(0, 20))

        font_btn = ctk.CTkFont(size=18, weight="bold")

        # Generación dinámica de packs con tamaño uniforme y scroll automático
        for pack_name, ejercicios in exercise_packs.items():
            num_ejercicios = len(ejercicios)
            texto_boton = f"{pack_name.upper()}  •  ({num_ejercicios} EJERCICIOS)" if isinstance(ejercicios, list) else pack_name.upper()

            btn = ctk.CTkButton(
                self.scroll_container,
                text=texto_boton,
                font=font_btn,
                fg_color="#13273D",
                border_color="#80D8FF",
                border_width=2,
                text_color="#FFFFFF",
                hover_color="#1E3A5F",
                corner_radius=16,
                height=65,
                command=lambda p=pack_name: self.on_pack_seleccionado(p)
            )
            btn.pack(fill="x", padx=25, pady=8)

    def volver(self):
        """Ejecuta el callback para volver al menú principal."""
        if self.cb_volver:
            self.cb_volver()
        else:
            self.ocultar()

    def mostrar(self):
        self.frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    def ocultar(self):
        self.frame.place_forget()