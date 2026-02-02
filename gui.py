# gui_entrenamiento_v5.py
import tkinter as tk
from tkinter import font, Toplevel, Label, Button

# ---- Datos de los packs y ejercicios ----
packs = {
    1: ["Brazos estirados", "Brazos a 90°"],
    2: ["Brazo derecho 90°, izquierdo estirado",
        "Brazo izquierdo 90°, derecho estirado"]
}
TIEMPO_EJERCICIO = 5  # segundos

# ---- Variables globales ----
selected_pack = None
ejercicio_actual = 0


# ---- Funciones ----
def seleccionar_pack(pack_id):
    global selected_pack
    selected_pack = pack_id
    mostrar_confirmacion_pack(pack_id)


def mostrar_confirmacion_pack(pack_id):
    ejercicios_pack = packs[pack_id]
    ejercicios_texto = "\n".join(
        [f"{i+1}. {e}" for i, e in enumerate(ejercicios_pack)]
    )

    ventana = Toplevel(root)
    ventana.title("Confirmación de Pack")
    ventana.geometry("600x400")
    ventana.configure(bg="#0D1B2A")

    Label(
        ventana,
        text=f"Has seleccionado Pack {pack_id}",
        font=title_font,
        fg="#E0F7FA",
        bg="#0D1B2A"
    ).pack(pady=20)

    Label(
        ventana,
        text=(
            f"Este pack contiene {len(ejercicios_pack)} ejercicios:\n\n"
            f"{ejercicios_texto}\n\n"
            f"Cada ejercicio dura {TIEMPO_EJERCICIO} segundos"
        ),
        font=text_font,
        fg="#80D8FF",
        bg="#0D1B2A",
        justify="center"
    ).pack(pady=10)

    btn_frame = tk.Frame(ventana, bg="#0D1B2A")
    btn_frame.pack(pady=20)

    Button(
        btn_frame,
        text="Aceptar",
        font=btn_font,
        fg="#FFFFFF",
        bg="#42A5F5",
        width=12,
        pady=10,
        command=lambda: [ventana.destroy(), iniciar_simulacion(0)]
    ).pack(side="left", padx=20)

    Button(
        btn_frame,
        text="Cancelar",
        font=btn_font,
        fg="#FFFFFF",
        bg="#1B3B5F",
        width=12,
        pady=10,
        command=ventana.destroy
    ).pack(side="left", padx=20)


def iniciar_simulacion(idx):
    global ejercicio_actual
    ejercicio_actual = idx

    for lbl in pack_buttons:
        lbl.place_forget()
    label_msg.place_forget()

    mostrar_ejercicio()


def mostrar_ejercicio():
    nombre_ejercicio = packs[selected_pack][ejercicio_actual]

    contador_label.place(x=50, y=50)
    nombre_label.config(text=nombre_ejercicio)
    nombre_label.place(x=50, y=120)

    correccion_label.config(
        text=f"Simulación de correcciones...\n"
             f"Ejercicio {ejercicio_actual + 1}/{len(packs[selected_pack])}"
    )
    correccion_label.place(x=50, y=200)

    ejecutar_contador(TIEMPO_EJERCICIO)


def ejecutar_contador(tiempo):
    global ejercicio_actual

    if tiempo >= 0:
        contador_label.config(text=f"{tiempo}s")
        root.after(1000, ejecutar_contador, tiempo - 1)
    else:
        ejercicio_actual += 1
        if ejercicio_actual < len(packs[selected_pack]):
            mostrar_ejercicio()
        else:
            mostrar_fin_entrenamiento()


def mostrar_fin_entrenamiento():
    contador_label.place_forget()
    nombre_label.place_forget()
    correccion_label.place_forget()

    label_msg.config(
        text=(
            "¡Has completado todos los ejercicios del pack!\n\n"
            "¿Deseas realizar otro entrenamiento o salir?"
        ),
        fg="#00E676",
        justify="center",
        wraplength=900
    )
    label_msg.place(x=50, y=250)

    aceptar_btn.config(
        text="Realizar otro entrenamiento",
        width=25,
        pady=12,
        command=lambda: [
            aceptar_btn.place_forget(),
            cancelar_btn.place_forget(),
            reiniciar_entrenamiento()
        ]
    )

    cancelar_btn.config(
        text="Salir",
        width=12,
        pady=12,
        command=root.destroy
    )

    aceptar_btn.place(x=150, y=420)
    cancelar_btn.place(x=620, y=420)


def reiniciar_entrenamiento():
    global selected_pack, ejercicio_actual
    selected_pack = None
    ejercicio_actual = 0

    label_msg.config(
        text="Bienvenida! ¿Qué entrenamiento deseas realizar?",
        fg="#E0F7FA"
    )
    label_msg.place(x=50, y=50)

    for i, lbl in enumerate(pack_buttons):
        lbl.place(x=350, y=200 + i * 100)

    aceptar_btn.place_forget()
    cancelar_btn.place_forget()


# ---- Creación de la ventana ----
root = tk.Tk()
root.title("Entrenamiento Postural")
root.geometry("1000x700")
root.configure(bg="#0D1B2A")

# ---- Fonts ----
title_font = font.Font(family="Helvetica", size=28, weight="bold")
btn_font = font.Font(family="Helvetica", size=20, weight="bold")
contador_font = font.Font(family="Helvetica", size=48, weight="bold")
text_font = font.Font(family="Helvetica", size=18)
correccion_font = font.Font(family="Helvetica", size=20)

# ---- Labels principales ----
label_msg = Label(
    root,
    text="Bienvenida! ¿Qué entrenamiento deseas realizar?",
    font=title_font,
    fg="#E0F7FA",
    bg="#0D1B2A",
    wraplength=900,
    justify="center"
)
label_msg.place(x=50, y=50)

contador_label = Label(
    root,
    text="",
    font=contador_font,
    fg="#00B0FF",
    bg="#0D1B2A"
)

nombre_label = Label(
    root,
    text="",
    font=btn_font,
    fg="#42A5F5",
    bg="#0D1B2A"
)

correccion_label = Label(
    root,
    text="",
    font=correccion_font,
    fg="#80D8FF",
    bg="#0D1B2A",
    justify="left",
    wraplength=900
)

# ---- Botones de selección de packs ----
pack_buttons = []
for i, texto in enumerate(["Pack 1", "Pack 2"]):
    lbl = tk.Label(
        root,
        text=texto,
        font=btn_font,
        fg="#FFFFFF",
        bg="#1B3B5F",
        width=25,
        pady=15,
        cursor="hand2"
    )
    lbl.place(x=350, y=200 + i * 100)
    lbl.bind("<Enter>", lambda e, l=lbl: l.config(bg="#42A5F5"))
    lbl.bind("<Leave>", lambda e, l=lbl: l.config(bg="#1B3B5F"))
    lbl.bind("<Button-1>", lambda e, p=i + 1: seleccionar_pack(p))
    pack_buttons.append(lbl)

# ---- Botones finales (ocultos por defecto) ----
aceptar_btn = tk.Button(
    root,
    text="Aceptar",
    font=btn_font,
    fg="#FFFFFF",
    bg="#42A5F5",
    width=18,
    pady=10
)

cancelar_btn = tk.Button(
    root,
    text="Cancelar",
    font=btn_font,
    fg="#FFFFFF",
    bg="#1B3B5F",
    width=18,
    pady=10
)

root.mainloop()
