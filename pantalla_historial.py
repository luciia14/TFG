import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database
import threading 

class PantallaHistorial:
    def __init__(self, root, fuentes, cb_volver):
        self.root = root
        self.fuentes = fuentes
        self.frame = tk.Frame(root, bg="#0D1B2A")
        
        # --- Encabezado ---
        header = tk.Frame(self.frame, bg="#0D1B2A")
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(header, text="⬅ ", command=cb_volver, font=fuentes["boton"], 
                  bg="#1B3B5F", fg="white", bd=0, cursor="hand2").pack(side="left")
        tk.Label(header, text="HISTORIAL Y ANÁLISIS", font=fuentes["titulo"], 
                 fg="#E0F7FA", bg="#0D1B2A").pack(side="left", padx=20)

        # --- Contenedor Principal (Grid) ---
        container = tk.Frame(self.frame, bg="#0D1B2A")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Configuración de pesos para control total de dimensiones
        container.grid_columnconfigure(0, weight=0) # Historial estático
        container.grid_columnconfigure(1, weight=1) # Gráficos expandibles
        container.grid_rowconfigure(0, weight=1)    # Fila superior se expande
        container.grid_rowconfigure(1, weight=0)    # Fila de IA fija

        # --- Estilos Treeview ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0D1B2A", foreground="white", 
                        fieldbackground="#0D1B2A", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), 
                        background="#1B3B5F", foreground="white")
        style.map("Treeview", background=[('selected', '#1B3B5F')])

        # Columna 0: Historial
        self.tree = ttk.Treeview(container, columns=("fecha", "pack"), show="headings", height=11)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("pack", text="Ejercicio")
        self.tree.column("fecha", width=180, anchor="center")
        self.tree.column("pack", width=80, anchor="center")
        self.tree.grid(row=0, column=0, sticky="n", padx=(0, 20))

        # Columna 1: Gráficos
        self.frame_graficos = tk.Frame(container, bg="#0D1B2A")
        self.frame_graficos.grid(row=0, column=1, sticky="nsew")

        # --- Área de Recomendaciones (Altura fija) ---
        self.frame_reco_container = tk.Frame(container, bg="#0D1B2A")
        self.frame_reco_container.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        # AJUSTA ESTE HEIGHT PARA CAMBIAR EL TAMAÑO VERTICAL
        self.frame_reco = tk.Frame(self.frame_reco_container, bg="#1B3B5F", height=120)
        self.frame_reco.pack(fill=tk.X)
        self.frame_reco.pack_propagate(False) 

        # TEXTO DINÁMICO: wraplength=0 permite que se modifique dinámicamente
        self.lbl_reco = tk.Label(self.frame_reco, text="🧠 Analizando tus resultados con IA...", 
                                 font=fuentes["texto"], fg="#80D8FF", bg="#1B3B5F", 
                                 wraplength=0, justify="left", anchor="nw")
        self.lbl_reco.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Evento para reajustar el corte de línea al redimensionar la ventana o el frame
        self.lbl_reco.bind('<Configure>', lambda e: self.lbl_reco.config(wraplength=e.width - 40))

    def mostrar(self, usuario_id):
        self.frame.pack(fill=tk.BOTH, expand=True)
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        
        sesiones = database.obtener_lista_sesiones(usuario_id)
        if sesiones:
            for s in sesiones:
                self.tree.insert("", "end", values=(str(s['fecha'])[:16], s['pack']))
        
        self.lbl_reco.config(text="🧠 Analizando tus resultados con IA...")
        
        def tarea_ia():
            consejo = database.obtener_recomendacion_usuario(usuario_id)
            self.lbl_reco.after(0, lambda: self.lbl_reco.config(text=consejo))
            
        threading.Thread(target=tarea_ia, daemon=True).start()
        
        self.dibujar_graficos(usuario_id)

    def dibujar_graficos(self, usuario_id):
        for widget in self.frame_graficos.winfo_children(): 
            widget.destroy()

        datos = database.obtener_magnitudes_para_graficos(usuario_id)
        if not datos: 
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), facecolor="#0D1B2A")
        titulos = ["Análisis Tren Superior", "Análisis Tren Inferior"]
        axes = [ax1, ax2]
        
        for i, ax in enumerate(axes):
            ax.set_facecolor("#0D1B2A")
            ax.tick_params(colors='white')
            ax.set_ylim(0, 1000)
            ax.set_xlim(1, 12)
            ax.set_title(titulos[i], color='white', fontsize=11, pad=10)
            ax.set_ylabel("Error", color='white', fontsize=9)
            for spine in ax.spines.values(): spine.set_color('white')

        art_sets = [['hombros', 'codos', 'espalda'], ['cadera', 'rodillas', 'cuello']]
        for i, grupo in enumerate(art_sets):
            for art in grupo:
                x_art = [idx + 1 for idx, d in enumerate(datos) if d[art] > 0]
                y_art = [d[art] for d in datos if d[art] > 0]
                if y_art: axes[i].plot(x_art, y_art, 'o-', label=art.capitalize())
            axes[i].legend(loc='upper right', fontsize='x-small', facecolor="#0D1B2A", labelcolor='white')

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def ocultar(self):
        self.frame.pack_forget()