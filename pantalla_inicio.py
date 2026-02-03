# pantalla_inicio.py
import tkinter as tk
from tkinter import Label
from styles import COLOR_TITULO, COLOR_BOTON, COLOR_BOTON_SEC
from packs import exercise_packs


class PantallaInicio:
    def __init__(self, root, fuentes, on_pack_seleccionado):
        self.root = root
        self.fuentes = fuentes
        self.on_pack_seleccionado = on_pack_seleccionado
        self.pack_buttons = []

        # Mensaje de bienvenida
        self.label_msg = Label(
            root,
            text="Bienvenida! ¿Qué entrenamiento deseas realizar?",
            font=fuentes["titulo"],
            fg=COLOR_TITULO,
            bg="#0D1B2A",
            wraplength=900,
            justify="center"
        )
        self.label_msg.place(x=50, y=50)

        # Crear botones dinámicamente según los packs existentes
        for i, pack_name in enumerate(list(exercise_packs.keys())):
            lbl = tk.Label(
                root,
                text=pack_name,
                font=fuentes["boton"],
                fg="#FFFFFF",
                bg=COLOR_BOTON_SEC,
                width=25,
                pady=15,
                cursor="hand2"
            )

            lbl.place(x=350, y=200 + i * 100)

            # Efectos hover
            lbl.bind("<Enter>", lambda e, l=lbl: l.config(bg=COLOR_BOTON))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(bg=COLOR_BOTON_SEC))

            # Click → devuelve el NOMBRE del pack ("Pack 1", "Pack 2", ...)
            lbl.bind(
                "<Button-1>",
                lambda e, p=pack_name: self.on_pack_seleccionado(p)
            )

            self.pack_buttons.append(lbl)

    def mostrar(self):
        self.label_msg.place(x=50, y=50)
        for i, btn in enumerate(self.pack_buttons):
            btn.place(x=350, y=200 + i * 100)

    def ocultar(self):
        self.label_msg.place_forget()
        for btn in self.pack_buttons:
            btn.place_forget()
