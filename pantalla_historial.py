import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database

class PantallaHistorial:
    def __init__(self, root, fuentes, cb_volver):
        self.root = root
        self.fuentes = fuentes
        self.frame = tk.Frame(root, bg="#0D1B2A")
        
        # --- Encabezado ---
        header = tk.Frame(self.frame, bg="#0D1B2A")
        header.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(header, text="⬅ Volver", command=cb_volver, bg="#1B3B5F", fg="white").pack(side="left")
        tk.Label(header, text="HISTORIAL Y ANÁLISIS", font=fuentes["titulo"], 
                 fg="#E0F7FA", bg="#0D1B2A").pack(side="left", padx=20)

        # --- Contenedor Principal (PanedWindow) ---
        self.paned = tk.PanedWindow(self.frame, orient=tk.HORIZONTAL, bg="#0D1B2A")
        self.paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Panel Izquierdo: Lista
        self.tree = ttk.Treeview(self.paned, columns=("fecha", "pack"), show="headings")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("pack", text="Ejercicio")
        self.paned.add(self.tree, width=250)

        # Panel Derecho: Gráficos y Recomendación
        self.frame_der = tk.Frame(self.paned, bg="#0D1B2A")
        self.paned.add(self.frame_der, width=650)

        self.zona_graficos = tk.Frame(self.frame_der, bg="#0D1B2A")
        self.zona_graficos.pack(fill=tk.BOTH, expand=True)

        self.lbl_reco = tk.Label(self.frame_der, text="", font=fuentes["texto"], 
                                 fg="#80D8FF", bg="#1B3B5F", pady=10)
        self.lbl_reco.pack(fill=tk.X, pady=10)

    def mostrar(self, usuario_id):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # Cargar datos
        sesiones = database.obtener_lista_sesiones(usuario_id)
        for s in sesiones:
            self.tree.insert("", "end", values=(s['fecha'][:16], s['pack']))
        
        # Cargar Recomendación
        reco = database.obtener_recomendacion_usuario(usuario_id)
        self.lbl_reco.config(text=reco)

    def ocultar(self):
        self.frame.pack_forget()