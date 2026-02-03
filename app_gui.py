# app_gui.py
import tkinter as tk
from styles import cargar_fuentes
from packs import exercise_packs  # importem els packs
from pantalla_inicio import PantallaInicio
from pantalla_entrenamiento import PantallaEntrenamiento
from pantalla_final import PantallaFinal

# Temps fixe per cada exercici
TIEMPO_EJERCICIO = 5

class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Entrenamiento Postural")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0D1B2A")

        self.fuentes = cargar_fuentes(self.root)

        # Variables
        self.selected_pack = None
        self.ejercicio_actual = 0

        # Pantallas
        self.inicio = PantallaInicio(self.root, self.fuentes, self.seleccion_pack)
        self.entrenamiento = PantallaEntrenamiento(self.root, self.fuentes)
        self.final = PantallaFinal(self.root, self.fuentes, self.reiniciar_entrenamiento, self.salir)

        self.inicio.mostrar()

    # Callbacks
    def seleccion_pack(self, pack_name):
        self.selected_pack = pack_name
        self.mostrar_confirmacion(pack_name)

    def mostrar_confirmacion(self, pack_name):
        from tkinter import Toplevel, Label, Button

        ejercicios_pack = exercise_packs[pack_name]
        ejercicios_texto = "\n".join([f"{i+1}. {e['nombre']}" for i, e in enumerate(ejercicios_pack)])

        ventana = Toplevel(self.root)
        ventana.title("Confirmación de Pack")
        ventana.geometry("600x400")
        ventana.configure(bg="#0D1B2A")

        Label(ventana, text=f"Has seleccionado {pack_name}", font=self.fuentes["titulo"],
              fg="#E0F7FA", bg="#0D1B2A").pack(pady=20)

        Label(ventana,
              text=f"Este pack contiene {len(ejercicios_pack)} ejercicios:\n\n{ejercicios_texto}\n\nCada ejercicio dura {TIEMPO_EJERCICIO} segundos",
              font=self.fuentes["texto"], fg="#80D8FF", bg="#0D1B2A", justify="center").pack(pady=10)

        btn_frame = tk.Frame(ventana, bg="#0D1B2A")
        btn_frame.pack(pady=20)

        Button(btn_frame, text="Aceptar", font=self.fuentes["boton"], fg="#FFFFFF", bg="#42A5F5",
               width=12, pady=10, command=lambda: [ventana.destroy(), self.iniciar_simulacion(0)]).pack(side="left", padx=20)
        Button(btn_frame, text="Cancelar", font=self.fuentes["boton"], fg="#FFFFFF", bg="#1B3B5F",
               width=12, pady=10, command=ventana.destroy).pack(side="left", padx=20)

    def iniciar_simulacion(self, idx):
        self.ejercicio_actual = idx
        self.inicio.ocultar()
        self.final.ocultar()
        self.mostrar_ejercicio()

    def mostrar_ejercicio(self):
        ejercicio = exercise_packs[self.selected_pack][self.ejercicio_actual]
        nombre = ejercicio["nombre"]

        self.entrenamiento.mostrar_ejercicio(
            nombre,
            segundos=TIEMPO_EJERCICIO,
            actual=self.ejercicio_actual + 1,
            total=len(exercise_packs[self.selected_pack])
        )
        self.root.after(1000, self.contador, TIEMPO_EJERCICIO - 1)

    def contador(self, segundos):
        if segundos >= 0:
            self.entrenamiento.actualizar_contador(segundos)
            self.root.after(1000, self.contador, segundos - 1)
        else:
            self.ejercicio_actual += 1
            if self.ejercicio_actual < len(exercise_packs[self.selected_pack]):
                self.mostrar_ejercicio()
            else:
                self.mostrar_final()

    def mostrar_final(self):
        self.entrenamiento.ocultar()
        self.final.mostrar()

    def reiniciar_entrenamiento(self):
        self.final.ocultar()
        self.selected_pack = None
        self.ejercicio_actual = 0
        self.inicio.mostrar()

    def salir(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppGUI()
    app.run()

