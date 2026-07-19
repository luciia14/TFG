import tkinter as tk
from styles import cargar_fuentes
from packs import exercise_packs
from pantalla_login import PantallaLogin
from pantalla_principal import PantallaPrincipal
from pantalla_inicio import PantallaInicio
from pantalla_entrenamiento import PantallaEntrenamiento
from pantalla_final import PantallaFinal
from pantalla_historial import PantallaHistorial

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

        # Variables de control para el flujo
        self.selected_pack = None
        self.ejercicio_actual = 0
        self.confirmado = False  

        # 1. Creamos las pantallas
        self.inicio = PantallaInicio(self.root, self.fuentes, self.seleccion_pack)
        self.entrenamiento = PantallaEntrenamiento(self.root, self.fuentes)
        self.final = PantallaFinal(self.root, self.fuentes, self.reiniciar_entrenamiento, self.salir)
        
        # 2. Inicializamos el Dashboard Principal (sin botón custom)
        self.principal = PantallaPrincipal(
            self.root, 
            self.fuentes, 
            cb_entrenamiento=self.abrir_modo_entrenamiento,
            cb_progreso=self.abrir_progreso,
            cb_logout=self.cerrar_sesion
        )
        
        # 3. Inicializamos el Historial
        self.historial = PantallaHistorial(self.root, self.fuentes, self.volver_a_principal)
        
        # 4. Inicializamos Login
        self.login = PantallaLogin(self.root, self.fuentes, self.on_login_exitoso)

        # 5. Ocultamos las que no deben verse al arrancar
        self.inicio.ocultar()
        self.principal.ocultar()
        self.historial.ocultar()

        # 6. Mostramos el login
        self.login.mostrar()

    # ==========================================
    # SISTEMA DE NAVEGACIÓN Y SESIÓN
    # ==========================================
    def on_login_exitoso(self, user_id, username):
        self.usuario_id = user_id
        self.usuario_nombre = username
        self.root.title(f"Entrenamiento Postural - Usuario: {username}")
        self.principal.actualizar_saludo(username)
        self.login.ocultar()
        self.principal.mostrar()

    def abrir_modo_entrenamiento(self):
        self.principal.ocultar()
        self.inicio.mostrar()

    def abrir_progreso(self):
        self.principal.ocultar()
        self.historial.mostrar(self.usuario_id)

    def volver_a_principal(self):
        self.historial.ocultar()
        self.principal.mostrar()

    def cerrar_sesion(self):
        self.usuario_id = None
        self.usuario_nombre = None
        self.root.title("Entrenamiento Postural")
        self.principal.ocultar()
        self.login.mostrar()

    # ==========================================
    # FLUJO DE ENTRENAMIENTO
    # ==========================================
    def confirmar_seleccion(self):
        self.confirmado = True
        if hasattr(self, 'ventana_confirmacion'):
            self.ventana_confirmacion.destroy()
        # Aquí dispararías el flujo hacia la pantalla de entrenamiento

    def actualizar_interfaz_ejercicio(self, idx, nombre, total_ejercicios):
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
        self.entrenamiento.actualizar_contador(segundos)
        self.entrenamiento.actualizar_feedback(feedback_texto)

    def finalizar_entrenamiento_gui(self):
        self.entrenamiento.ocultar()
        self.final.mostrar()

    def seleccion_pack(self, pack_name):
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

        Label(ventana, text=f"Has seleccionado {pack_name}", font=self.fuentes["titulo"], fg="#E0F7FA", bg="#0D1B2A").pack(pady=20)

        Label(ventana, text=f"Este pack contiene {len(ejercicios_pack)} ejercicios:\n\n{ejercicios_texto}\n\nCada ejercicio dura {TIEMPO_EJERCICIO} segundos",
              font=self.fuentes["texto"], fg="#80D8FF", bg="#0D1B2A", justify="center").pack(pady=10)

        btn_frame = tk.Frame(ventana, bg="#0D1B2A")
        btn_frame.pack(pady=20)

        Button(btn_frame, text="Aceptar", font=self.fuentes["boton"], fg="#FFFFFF", bg="#42A5F5", width=12, pady=10, command=self.confirmar_seleccion).pack(side="left", padx=20)
        Button(btn_frame, text="Cancelar", font=self.fuentes["boton"], fg="#FFFFFF", bg="#1B3B5F", width=12, pady=10, command=self.cancelar_seleccion).pack(side="left", padx=20)
        
        self.ventana_confirmacion = ventana

    def cancelar_seleccion(self):
        self.selected_pack = None
        self.confirmado = False
        self.ventana_confirmacion.destroy()

    def reiniciar_entrenamiento(self):
        self.final.ocultar()
        self.selected_pack = None
        self.confirmado = False
        self.ejercicio_actual = 0
        self.principal.mostrar() 

    def salir(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppGUI()
    app.run()