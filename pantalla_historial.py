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
        
        tk.Button(header, text="⬅ Volver", command=cb_volver, font=fuentes["boton"], 
                  bg="#1B3B5F", fg="white", bd=0, cursor="hand2").pack(side="left")
        tk.Label(header, text="HISTORIAL Y ANÁLISIS", font=fuentes["titulo"], 
                 fg="#E0F7FA", bg="#0D1B2A").pack(side="left", padx=20)

        # --- Contenedor Principal (Grid) ---
        container = tk.Frame(self.frame, bg="#0D1B2A")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Estilos Treeview ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0D1B2A", foreground="white", 
                        fieldbackground="#0D1B2A", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), 
                        background="#1B3B5F", foreground="white")
        style.map("Treeview", background=[('selected', '#1B3B5F')])

        # Columna 0: Historial
        self.tree = ttk.Treeview(container, columns=("fecha", "pack"), show="headings")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("pack", text="Ejercicio")
        self.tree.column("fecha", width=180, anchor="center")
        self.tree.column("pack", width=80, anchor="center")
        self.tree.grid(row=0, column=0, sticky="ns", padx=(0, 20))

        # Columna 1: Gráficos (Área derecha)
        self.frame_graficos = tk.Frame(container, bg="#0D1B2A")
        self.frame_graficos.grid(row=0, column=1, sticky="nsew")
        container.grid_columnconfigure(1, weight=1)

        # Recomendaciones (Justo debajo)
        self.lbl_reco = tk.Label(container, text="", font=fuentes["texto"], 
                                 fg="#80D8FF", bg="#1B3B5F", wraplength=800, 
                                 justify="left", padx=10, pady=10)
        self.lbl_reco.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    def mostrar(self, usuario_id):
        self.frame.pack(fill=tk.BOTH, expand=True)
        # Cargar tabla
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        for s in database.obtener_lista_sesiones(usuario_id):
            self.tree.insert("", "end", values=(str(s['fecha'])[:16], s['pack']))
        
        self.lbl_reco.config(text=database.obtener_recomendacion_usuario(usuario_id))
        self.dibujar_graficos(usuario_id)

    def dibujar_graficos(self, usuario_id):
        # Limpiar gráfico anterior para evitar solapamientos
        for widget in self.frame_graficos.winfo_children():
            widget.destroy()

        datos = database.obtener_magnitudes_para_graficos(usuario_id)
        if not datos: 
            return

        # Crear figura
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), facecolor="#0D1B2A")
        
        # Títulos y ejes específicos
        titulos = ["Análisis Tren Superior (Índice de Corrección)", "Análisis Tren Inferior (Índice de Corrección)"]
        axes = [ax1, ax2]
        
        for i, ax in enumerate(axes):
            ax.set_facecolor("#0D1B2A")
            ax.tick_params(colors='white')
            ax.set_ylim(0, 1000)
            ax.set_xlim(1, 12)
            ax.set_title(titulos[i], color='white', fontsize=11, pad=10)
            ax.set_ylabel("Puntuación de Error", color='white', fontsize=9)
            for spine in ax.spines.values(): 
                spine.set_color('white')

        # Procesar y dibujar gráficas de forma individual por articulación
        art_sets = [['hombros', 'codos', 'espalda'], ['cadera', 'rodillas', 'cuello']]
        
        for i, grupo in enumerate(art_sets):
            for art in grupo:
                # Filtrar solo valores > 0
                x_art = [idx + 1 for idx, d in enumerate(datos) if d[art] > 0]
                y_art = [d[art] for d in datos if d[art] > 0]
                
                # Solo dibujar si hay datos para esta articulación
                if y_art:
                    axes[i].plot(x_art, y_art, 'o-', label=art.capitalize())

            axes[i].legend(loc='upper right', fontsize='x-small', facecolor="#0D1B2A", labelcolor='white')

        plt.tight_layout()

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def ocultar(self):
        self.frame.pack_forget()