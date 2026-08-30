import customtkinter as ctk
from pantalla_final import PantallaFinal

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1000x600")
root.title("Prueba de Pantalla Final")

# Diccionario de fuentes simulado (ajusta las claves o tamaños si tu app usa otros nombres)
fuentes = {
    "titulo": ("Arial", 24, "bold"),
    "boton": ("Arial", 16)
}

# Callbacks vacíos para que los botones no den error al pulsarlos
def dummy_reiniciar():
    print("Botón pulsado: Reiniciar entrenamiento")

def dummy_salir():
    print("Botón pulsado: Salir")
    root.destroy()

# Instanciar la clase PantallaFinal
pantalla_final = PantallaFinal(root, fuentes, dummy_reiniciar, dummy_salir)

# Forzar la visualización inmediata con un mensaje de prueba (o el texto por defecto)
pantalla_final.mostrar(
    "¡Has completado todos los ejercicios del pack!\n\n"
    "¿Deseas realizar otro entrenamiento o salir?"
)

root.mainloop()