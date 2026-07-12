# app_gui.py
import tkinter as tk
from styles import cargar_fuentes
from packs import exercise_packs  # importamos los packs
from pantalla_login import PantallaLogin         # <-- Asegúrate de tener importada tu pantalla de login
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

        # --- Variables de sesión del usuario ---
        self.usuario_id = None
        self.usuario_nombre = None

        # Variables de control para el MAIN
        self.selected_pack = None
        self.ejercicio_actual = 0
        self.confirmado = False  # Bandera clave para disparar la cámara

        # 1. Creamos las pantallas tal y como las tienes
        self.inicio = PantallaInicio(self.root, self.fuentes, self.seleccion_pack)
        self.entrenamiento = PantallaEntrenamiento(self.root, self.fuentes)
        self.final = PantallaFinal(self.root, self.fuentes, self.reiniciar_entrenamiento, self.salir)
        
        # 2. Inicializamos la Pantalla de Login pasándole el método on_login_exitoso
        self.login = PantallaLogin(self.root, self.fuentes, self.on_login_exitoso)

        # 3. ¡EL TRUCO! Ocultamos inmediatamente la de inicio que se acaba de auto-colocar
        self.inicio.ocultar()

        # 4. Mostramos el login para que sea lo único que se vea al arrancar
        self.login.mostrar()

    def on_login_exitoso(self, user_id, username):
        """Callback ejecutado por la pantalla de login al autenticarse con éxito"""
        self.usuario_id = user_id
        self.usuario_nombre = username
        
        # Cambiamos el título de la ventana para ver qué usuario está activo
        self.root.title(f"Entrenamiento Postural - Usuario: {username}")
        
        # Ocultamos el login y ahora SÍ permitimos pasar a la pantalla de inicio
        self.login.ocultar()
        self.inicio.mostrar()

    # --- El resto de tus métodos se quedan exactamente IGUAL sin tocar una sola línea ---

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

    def seleccion_pack(self, pack_name):
        """Se ejecuta al elegir un pack en la pantalla de inicio"""
        self.selected_pack = pack_name
        self.confirmado = False 
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