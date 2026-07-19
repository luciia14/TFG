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
        header.pack(fill=tk.X, padx=20, pady=20)
        tk.Button(header, text="⬅ Volver", command=cb_volver, font=fuentes["boton"], bg="#1B3B5F", fg="white", bd=0).pack(side="left")
        tk.Label(header, text="HISTORIAL Y ANÁLISIS", font=fuentes["titulo"], fg="#E0F7FA", bg="#0D1B2A").pack(side="left", padx=20)

        # --- Contenedor Principal (Grid) ---
        container = tk.Frame(self.frame, bg="#0D1B2A")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Columna 0: Historial
        self.tree = ttk.Treeview(container, columns=("fecha", "pack"), show="headings")
        self.tree.heading("fecha", text="Fecha"); self.tree.heading("pack", text="Ejercicio")
        self.tree.column("fecha", width=150, anchor="center"); self.tree.column("pack", width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="ns", padx=(0, 20))

        # Columna 1: Gráficos (El área grande a la derecha)
        self.frame_graficos = tk.Frame(container, bg="#0D1B2A")
        self.frame_graficos.grid(row=0, column=1, sticky="nsew")
        container.grid_columnconfigure(1, weight=1)

        # Recomendaciones
        self.lbl_reco = tk.Label(container, text="", font=fuentes["texto"], fg="#80D8FF", bg="#1B3B5F", wraplength=800, justify="left", padx=10, pady=10)
        self.lbl_reco.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    def mostrar(self, usuario_id):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # Cargar tabla
        for i in self.tree.get_children(): self.tree.delete(i)
        for s in database.obtener_lista_sesiones(usuario_id):
            self.tree.insert("", "end", values=(str(s['fecha'])[:16], s['pack']))
        
        self.lbl_reco.config(text=database.obtener_recomendacion_usuario(usuario_id))
        self.dibujar_graficos(usuario_id)

    def dibujar_graficos(self, usuario_id):
        datos = database.obtener_magnitudes_para_graficos(usuario_id)
        if not datos: return

        # Crear figura
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), facecolor="#0D1B2A")
        
        # Estilo para fondo oscuro
        for ax in [ax1, ax2]:
            ax.set_facecolor("#0D1B2A")
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.yaxis.label.set_color('white')
            ax.xaxis.label.set_color('white')

        # Datos para graficar
        x = range(1, len(datos) + 1)
        # Grafico 1: Hombros, Codos, Espalda
        for art in ['hombros', 'codos', 'espalda']:
            y = [d[art] for d in datos]
            ax1.plot(x, y, 'o-', label=art.capitalize())
        
        # Grafico 2: Cadera, Rodillas, Cuello
        for art in ['cadera', 'rodillas', 'cuello']:
            y = [d[art] for d in datos]
            ax2.plot(x, y, 'o-', label=art.capitalize())

        ax1.legend(loc='upper right', fontsize='small')
        ax2.legend(loc='upper right', fontsize='small')

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def ocultar(self):
        self.frame.pack_forget()