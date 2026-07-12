# pantalla_login.py
import tkinter as tk
from tkinter import Label, Entry, Button
from styles import COLOR_TITULO, COLOR_BOTON, COLOR_BOTON_SEC, COLOR_OK
import database as db

class PantallaLogin:
    def __init__(self, root, fuentes, login_exitoso_callback):
        self.root = root
        self.fuentes = fuentes
        self.login_exitoso_callback = login_exitoso_callback

        # ==========================================
        # 1. PANEL DE INICIO DE SESIÓN
        # ==========================================
        self.frame_login = tk.Frame(root, bg="#0D1B2A")
        
        Label(self.frame_login, text="INICIO DE SESIÓN", font=fuentes["titulo"], fg=COLOR_TITULO, bg="#0D1B2A").pack(pady=30)

        Label(self.frame_login, text="Usuario:", font=fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=5)
        self.entry_user = Entry(self.frame_login, font=fuentes["texto"], width=25, justify="center")
        self.entry_user.pack(pady=5)

        Label(self.frame_login, text="Contraseña:", font=fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=5)
        self.entry_pass = Entry(self.frame_login, font=fuentes["texto"], show="*", width=25, justify="center")
        self.entry_pass.pack(pady=5)

        self.error_label_login = Label(self.frame_login, text="", font=fuentes["texto"], fg="#FF5252", bg="#0D1B2A")
        self.error_label_login.pack(pady=15)

        Button(self.frame_login, text="Iniciar Sesión", font=fuentes["boton"], fg="#FFFFFF", bg=COLOR_BOTON, width=15, pady=5, command=self.intentar_login).pack(pady=5)
        Button(self.frame_login, text="Crear una cuenta nueva", font=fuentes["texto"], fg="#FFFFFF", bg=COLOR_BOTON_SEC, width=20, pady=3, command=self.ir_a_registro).pack(pady=5)

        # ==========================================
        # 2. PANEL DE REGISTRO
        # ==========================================
        self.frame_registro = tk.Frame(root, bg="#0D1B2A")

        # Flecha de retorno al login
        Button(self.frame_registro, text="←", font=("Helvetica", 20, "bold"), fg="#80D8FF", bg="#1B3B5F", bd=0, cursor="hand2", command=self.ir_a_login).pack(anchor="w", padx=10, pady=10)

        Label(self.frame_registro, text="FORMULARIO DE REGISTRO", font=fuentes["titulo"], fg=COLOR_TITULO, bg="#0D1B2A").pack(pady=15)

        Label(self.frame_registro, text="Nombre Completo:", font=fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=3)
        self.entry_reg_nombre = Entry(self.frame_registro, font=fuentes["texto"], width=30, justify="center")
        self.entry_reg_nombre.pack(pady=3)

        Label(self.frame_registro, text="Fecha de Nacimiento (DD/MM/AAAA):", font=fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=3)
        self.entry_reg_fecha = Entry(self.frame_registro, font=fuentes["texto"], width=30, justify="center")
        self.entry_reg_fecha.bind("<KeyRelease>", self.format_fecha)
        self.entry_reg_fecha.pack(pady=3)

        Label(self.frame_registro, text="Nombre de usuario:", font=fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=3)
        self.entry_reg_user = Entry(self.frame_registro, font=fuentes["texto"], width=30, justify="center")
        self.entry_reg_user.pack(pady=3)

        Label(self.frame_registro, text="Contraseña:", font=fuentes["texto"], fg="#80D8FF", bg="#0D1B2A").pack(pady=3)
        self.entry_reg_pass = Entry(self.frame_registro, font=fuentes["texto"], show="*", width=30, justify="center")
        self.entry_reg_pass.pack(pady=3)

        self.error_label_reg = Label(self.frame_registro, text="", font=fuentes["texto"], fg="#FF5252", bg="#0D1B2A")
        self.error_label_reg.pack(pady=10)

        Button(self.frame_registro, text="Registrar Perfil", font=fuentes["boton"], fg="#FFFFFF", bg=COLOR_OK, width=18, pady=5, command=self.intentar_registro).pack(pady=10)

    # --- Lógica de la máscara de fecha ---
    def format_fecha(self, event):
        if event.keysym == "BackSpace":
            return
            
        text = self.entry_reg_fecha.get().replace("/", "")
        new_text = ""
        for i, char in enumerate(text):
            if i in [2, 4]: new_text += "/"
            new_text += char
        self.entry_reg_fecha.delete(0, tk.END)
        self.entry_reg_fecha.insert(0, new_text[:10])

    # --- Navegación ---
    def mostrar(self):
        self.frame_registro.place_forget()
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

    def ocultar(self):
        """Oculta completamente los frames de esta vista (Soluciona el error)"""
        self.frame_login.place_forget()
        self.frame_registro.place_forget()

    def ir_a_registro(self):
        self.frame_login.place_forget()
        self.frame_registro.place(relx=0.5, rely=0.5, anchor="center")
        self.error_label_reg.config(text="")

    def ir_a_login(self):
        self.frame_registro.place_forget()
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        self.error_label_reg.config(text="")

    # --- Acciones ---
    def intentar_login(self):
        user = self.entry_user.get().strip()
        passwd = self.entry_pass.get().strip()
        user_id = db.verificar_usuario(user, passwd)
        if user_id:
            self.error_label_login.config(text="¡Acceso concedido!", fg=COLOR_OK)
            self.root.after(1000, lambda: self.login_exitoso_callback(user_id, user))
        else:
            self.error_label_login.config(text="Usuario o contraseña incorrectos.", fg="#FF5252")

    def intentar_registro(self):
        nombre = self.entry_reg_nombre.get().strip()
        fecha = self.entry_reg_fecha.get().strip()
        user = self.entry_reg_user.get().strip()
        passwd = self.entry_reg_pass.get().strip()
        
        if not nombre or len(fecha) < 10 or not user or not passwd:
            self.error_label_reg.config(text="Rellena todos los campos correctamente.", fg="#FF5252")
            return

        if db.registrar_usuario(user, passwd, nombre, fecha):
            # Limpiamos campos
            self.entry_reg_nombre.delete(0, tk.END)
            self.entry_reg_fecha.delete(0, tk.END)
            self.entry_reg_user.delete(0, tk.END)
            self.entry_reg_pass.delete(0, tk.END)
            
            # Volvemos al login y mostramos mensaje
            self.ir_a_login()
            self.error_label_login.config(text="¡Registro exitoso! Ya puedes entrar.", fg=COLOR_OK)
            
            # Limpiamos el mensaje de éxito tras 3 segundos
            self.root.after(3000, lambda: self.error_label_login.config(text=""))
        else:
            self.error_label_reg.config(text="Ese usuario ya existe.", fg="#FF5252")