# styles.py
from tkinter import font

BG_COLOR = "#0D1B2A"
COLOR_TITULO = "#E0F7FA"
COLOR_TEXTO = "#80D8FF"
COLOR_OK = "#00E676"
COLOR_BOTON = "#42A5F5"
COLOR_BOTON_SEC = "#1B3B5F"
COLOR_CONTADOR = "#00B0FF"

def cargar_fuentes(root):
    return {
        "titulo": font.Font(root, family="Helvetica", size=28, weight="bold"),
        "boton": font.Font(root, family="Helvetica", size=20, weight="bold"),
        "contador": font.Font(root, family="Helvetica", size=48, weight="bold"),
        "texto": font.Font(root, family="Helvetica", size=18),
        "feedback": font.Font(root, family="Helvetica", size=20),
    }
