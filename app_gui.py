import customtkinter as ctk
import tkinter as tk
from styles import cargar_fuentes
from packs import exercise_packs
from pantalla_login import PantallaLogin
from pantalla_principal import PantallaPrincipal
from pantalla_inicio import PantallaInicio
from pantalla_entrenamiento import PantallaEntrenamiento
from pantalla_final import PantallaFinal
from pantalla_historial import PantallaHistorial

# Configuración global de CustomTkinter
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")


TIEMPO_EJERCICIO = 5

class AppGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Entrenamiento Postural")
        self.root.geometry("1000x700")
       
        self.root.configure(fg_color="#0D1B2A")

        self.fuentes = cargar_fuentes(self.root)

       
        self.usuario_id = None
        self.usuario_nombre = None

        # Variables de control para el flujo
        self.selected_pack = None
        self.ejercicio_actual = 0
        self.confirmado = False  

        # Creamos las pantallas 
        self.inicio = PantallaInicio(
            self.root, 
            self.fuentes, 
            self.seleccion_pack, 
            cb_volver=self.volver_a_principal
        )
        self.entrenamiento = PantallaEntrenamiento(self.root, self.fuentes)
        self.final = PantallaFinal(self.root, self.fuentes, self.reiniciar_entrenamiento, self.salir)
        
        # Inicializamos el Dashboard Principal
        self.principal = PantallaPrincipal(
            self.root, 
            self.fuentes, 
            cb_entrenamiento=self.abrir_modo_entrenamiento,
            cb_progreso=self.abrir_progreso,
            cb_logout=self.cerrar_sesion
        )
        
        # Inicializamos el Historial
        self.historial = PantallaHistorial(self.root, self.fuentes, self.volver_a_principal)
        
        # Inicializamos Login
        self.login = PantallaLogin(self.root, self.fuentes, self.on_login_exitoso)

        # Ocultamos las que no deben verse al arrancar
        self.inicio.ocultar()
        self.principal.ocultar()
        self.historial.ocultar()

        # Mostramos el login
        self.login.mostrar()

    
    def on_login_exitoso(self, user_id, username):
        self.usuario_id = user_id
        self.usuario_nombre = username
        self.root.title(f"Entrenamiento Postural - Usuario: {username}")
        self.principal.actualizar_saludo(username)
        
        # Destruimos la pantalla de login para liberar la memoria
        self.login.destroy() 
        
        # Mostramos la pantalla principal
        self.principal.mostrar()

    def abrir_modo_entrenamiento(self):
        self.principal.ocultar()
        self.inicio.mostrar()

    def abrir_progreso(self):
        self.principal.ocultar()
        self.historial.mostrar(self.usuario_id)

    def volver_a_principal(self):
        # Ocultamos tanto el historial como la pantalla de packs
        self.historial.ocultar()
        self.inicio.ocultar()
        self.principal.mostrar()

    def cerrar_sesion(self):
        self.usuario_id = None
        self.usuario_nombre = None
        self.root.title("Entrenamiento Postural")
        self.principal.ocultar()
        self.login.mostrar()

  
    def confirmar_seleccion(self):
        self.confirmado = True
        if hasattr(self, 'ventana_confirmacion'):
            self.ventana_confirmacion.destroy()

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
        ejercicios_pack = exercise_packs[pack_name]
        ejercicios_texto = "\n".join([f"{i+1}. {e['nombre']}" for i, e in enumerate(ejercicios_pack)])

        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Confirmación de Pack")
        ventana.geometry("600x400")
        ventana.configure(fg_color="#0D1B2A")

        ctk.CTkLabel(ventana, text=f"Has seleccionado {pack_name}", font=self.fuentes["titulo"], text_color="#E0F7FA", fg_color="transparent").pack(pady=20)

        ctk.CTkLabel(ventana, text=f"Este pack contiene {len(ejercicios_pack)} ejercicios:\n\n{ejercicios_texto}\n\nCada ejercicio dura {TIEMPO_EJERCICIO} segundos",
                     font=self.fuentes["texto"], text_color="#80D8FF", fg_color="transparent", justify="center").pack(pady=10)

        btn_frame = ctk.CTkFrame(ventana, fg_color="#0D1B2A")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Aceptar", font=self.fuentes["boton"], text_color="#FFFFFF", fg_color="#42A5F5", width=120, height=40, command=self.confirmar_seleccion).pack(side="left", padx=20)
        ctk.CTkButton(btn_frame, text="Cancelar", font=self.fuentes["boton"], text_color="#FFFFFF", fg_color="#1B3B5F", width=120, height=40, command=self.cancelar_seleccion).pack(side="left", padx=20)
        
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
