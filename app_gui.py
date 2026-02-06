import tkinter as tk
from styles import cargar_fuentes
from packs import exercise_packs  # importamos los packs
from pantalla_inicio import PantallaInicio
from pantalla_entrenamiento import PantallaEntrenamiento
from pantalla_final import PantallaFinal

# Tiempo fijo por defecto
TIEMPO_EJERCICIO = 5

class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Entrenamiento Postural")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0D1B2A")

        self.fuentes = cargar_fuentes(self.root)

        # Variables de control para el MAIN
        self.selected_pack = None
        self.ejercicio_actual = 0
        self.confirmado = False  # Bandera clave para disparar la cámara

        # Pantallas
        self.inicio = PantallaInicio(self.root, self.fuentes, self.seleccion_pack)
        self.entrenamiento = PantallaEntrenamiento(self.root, self.fuentes)
        self.final = PantallaFinal(self.root, self.fuentes, self.reiniciar_entrenamiento, self.salir)

        self.inicio.mostrar()

    # --- Métodos de sincronización con MAIN ---

    def confirmar_seleccion(self):
        """Activa la bandera para que el hilo del main inicie la cámara"""
        self.confirmado = True
        if hasattr(self, 'ventana_confirmacion'):
            self.ventana_confirmacion.destroy()

    def actualizar_interfaz_ejercicio(self, idx, nombre, total_ejercicios):
        """Prepara la pantalla de entrenamiento para un nuevo ejercicio"""
        self.ejercicio_actual = idx
        self.inicio.ocultar()
        self.final.ocultar()
        
        self.entrenamiento.mostrar_ejercicio(
            nombre,
            segundos=TIEMPO_EJERCICIO,
            actual=idx + 1,
            total=total_ejercicios
        )

    def actualizar_datos_tiempo_real(self, segundos, feedback_texto):
        """Actualiza el contador y los mensajes recibidos desde el hilo de la cámara"""
        self.entrenamiento.actualizar_contador(segundos)
        self.entrenamiento.actualizar_feedback(feedback_texto)

    def finalizar_entrenamiento_gui(self):
        """Muestra la pantalla final y limpia estados"""
        self.entrenando = False
        self.entrenamiento.ocultar()
        self.final.mostrar()

    # --- Callbacks y navegación ---

    def seleccion_pack(self, pack_name):
        """Se ejecuta al elegir un pack en la pantalla de inicio"""
        self.selected_pack = pack_name
        self.confirmado = False # Aseguramos que no empiece antes de confirmar
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

        # Botón Aceptar: Llama a confirmar_seleccion para avisar al Main
        Button(btn_frame, text="Aceptar", font=self.fuentes["boton"], fg="#FFFFFF", bg="#42A5F5",
               width=12, pady=10, command=self.confirmar_seleccion).pack(side="left", padx=20)
        
        Button(btn_frame, text="Cancelar", font=self.fuentes["boton"], fg="#FFFFFF", bg="#1B3B5F",
               width=12, pady=10, command=self.cancelar_seleccion).pack(side="left", padx=20)
        
        self.ventana_confirmacion = ventana

    def cancelar_seleccion(self):
        self.selected_pack = None
        self.confirmado = False
        self.ventana_confirmacion.destroy()

    def reiniciar_entrenamiento(self):
        """Resetea todo para poder elegir otro pack"""
        self.final.ocultar()
        self.selected_pack = None
        self.confirmado = False
        self.ejercicio_actual = 0
        self.inicio.mostrar()

    def salir(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppGUI()
    app.run()