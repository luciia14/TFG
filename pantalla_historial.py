import tkinter as tk
from tkinter import ttk
import database

class PantallaHistorial:
    def __init__(self, root, fuentes, cb_volver):
        self.root = root
        self.fuentes = fuentes
        self.frame = tk.Frame(root, bg="#0D1B2A")
        
        # --- Encabezado ---
        header = tk.Frame(self.frame, bg="#0D1B2A")
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(header, text="⬅ Volver", command=cb_volver, font=fuentes["boton"], 
                  bg="#1B3B5F", fg="white", bd=0).pack(side="left")
        tk.Label(header, text="HISTORIAL Y ANÁLISIS", font=fuentes["titulo"], 
                 fg="#E0F7FA", bg="#0D1B2A").pack(side="left", padx=20)

        # --- Contenedor de contenido (Grid) ---
        container = tk.Frame(self.frame, bg="#0D1B2A")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Configuración del Treeview (Historial)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0D1B2A", foreground="white", 
                        fieldbackground="#0D1B2A", font=("Arial", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        self.tree = ttk.Treeview(container, columns=("fecha", "pack"), show="headings")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("pack", text="Ejercicio")
        # Ajustamos el ancho para que no ocupe demasiado espacio a lo ancho
        self.tree.column("fecha", width=150, anchor="center")
        self.tree.column("pack", width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="ns", padx=(0, 20))

        # --- Recomendaciones (Justo debajo del historial) ---
        self.lbl_reco = tk.Label(container, text="", font=fuentes["texto"], 
                                 fg="#80D8FF", bg="#1B3B5F", wraplength=400, 
                                 justify="left", padx=10, pady=10)
        self.lbl_reco.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        # Configuración de pesos para que el historial crezca hacia abajo
        container.grid_rowconfigure(0, weight=1)

    def mostrar(self, usuario_id):
        self.frame.pack(fill=tk.BOTH, expand=True)
        for i in self.tree.get_children(): self.tree.delete(i)
        
        for s in database.obtener_lista_sesiones(usuario_id):
            # Formato de fecha limpio
            fecha_f = str(s['fecha'])[:16]
            self.tree.insert("", "end", values=(fecha_f, s['pack']))
        
        self.lbl_reco.config(text=database.obtener_recomendacion_usuario(usuario_id))

    def ocultar(self):
        self.frame.pack_forget()