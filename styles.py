# styles.py

BG_COLOR = "#0D1B2A"
COLOR_TITULO = "#E0F7FA"
COLOR_TEXTO = "#80D8FF"
COLOR_OK = "#00E676"
COLOR_BOTON = "#42A5F5"
COLOR_BOTON_SEC = "#1B3B5F"
COLOR_CONTADOR = "#00B0FF"

def cargar_fuentes(root):
    return {
        "titulo": ("Helvetica", 28, "bold"),
        "boton": ("Helvetica", 20, "bold"),
        "contador": ("Helvetica", 48, "bold"),
        "texto": ("Helvetica", 18),
        "feedback": ("Helvetica", 20),
    }