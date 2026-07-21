import customtkinter as ctk
import tkinter as tk
from styles import COLOR_TITULO, COLOR_BOTON, COLOR_BOTON_SEC, COLOR_OK
import database as db

class PantallaLogin:
    def __init__(self, root, fuentes, login_exitoso_callback):
        self.root = root
        self.fuentes = fuentes
        self.login_exitoso_callback = login_exitoso_callback

        # Configuración del contenedor principal (ocupa más pantalla: 85% de ancho y alto)
        self.frame_container = ctk.CTkFrame(root, fg_color="#0D1B2A", corner_radius=20)
        self.frame_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.9)

        # ==========================================
        # 1. PANEL DE INICIO DE SESIÓN
        # ==========================================
        self.frame_login = ctk.CTkFrame(self.frame_container, fg_color="transparent")
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)
        
        # Título
        ctk.CTkLabel(self.frame_login, text="INICIO DE SESIÓN", font=fuentes["titulo"], text_color=COLOR_TITULO).pack(pady=(10, 20))

        # Input Usuario (Cuadrado con esquinas redondeadas)
        self.entry_user = ctk.CTkEntry(self.frame_login, font=fuentes["texto"], width=400, height=55,
                                       fg_color="#1B3B5F", border_width=0, corner_radius=25,
                                       placeholder_text="Usuario", placeholder_text_color="#80D8FF", text_color="white", justify="center")
        self.entry_user.pack(pady=10)

        # Input Contraseña
        self.entry_pass = ctk.CTkEntry(self.frame_login, font=fuentes["texto"], show="*", width=400, height=55,
                                       fg_color="#1B3B5F", border_width=0, corner_radius=25,
                                       placeholder_text="Contraseña", placeholder_text_color="#80D8FF", text_color="white", justify="center")
        self.entry_pass.pack(pady=10)

        # Mensajes de error
        self.error_label_login = ctk.CTkLabel(self.frame_login, text="", font=fuentes["texto"], text_color="#FF5252")
        self.error_label_login.pack(pady=10)

        # Botón Principal
        ctk.CTkButton(self.frame_login, text="Iniciar Sesión", font=fuentes["boton"], 
                      fg_color=COLOR_BOTON, corner_radius=25, width=400, height=55, 
                      command=self.intentar_login).pack(pady=10)
        
        # Enlace para registro
        btn_registro = ctk.CTkButton(self.frame_login, text="Crear una cuenta nueva", font=fuentes["texto"], 
                                     fg_color="transparent", hover_color="#0D1B2A", text_color=COLOR_BOTON_SEC, 
                                     command=self.ir_a_registro)
        btn_registro.pack(pady=5)

        # ==========================================
        # 2. PANEL DE REGISTRO
        # ==========================================
        self.frame_registro = ctk.CTkFrame(self.frame_container, fg_color="transparent")

        # Título
        ctk.CTkLabel(self.frame_registro, text="REGISTRO", font=fuentes["titulo"], text_color=COLOR_TITULO).pack(pady=(10, 20))

        # Input Nombre
        self.entry_reg_nombre = ctk.CTkEntry(self.frame_registro, font=fuentes["texto"], width=400, height=50,
                                             fg_color="#1B3B5F", border_width=0, corner_radius=25,
                                             placeholder_text="Nombre Completo", placeholder_text_color="#80D8FF", text_color="white", justify="center")
        self.entry_reg_nombre.pack(pady=8)

        # Input Fecha
        self.entry_reg_fecha = ctk.CTkEntry(self.frame_registro, font=fuentes["texto"], width=400, height=50,
                                            fg_color="#1B3B5F", border_width=0, corner_radius=25,
                                            placeholder_text="Fecha de Nacimiento (DD/MM/AAAA)", placeholder_text_color="#80D8FF", text_color="white", justify="center")
        self.entry_reg_fecha.bind("<KeyRelease>", self.format_fecha)
        self.entry_reg_fecha.pack(pady=8)

        # Input Usuario
        self.entry_reg_user = ctk.CTkEntry(self.frame_registro, font=fuentes["texto"], width=400, height=50,
                                           fg_color="#1B3B5F", border_width=0, corner_radius=25,
                                           placeholder_text="Nombre de usuario", placeholder_text_color="#80D8FF", text_color="white", justify="center")
        self.entry_reg_user.pack(pady=8)

        # Input Contraseña
        self.entry_reg_pass = ctk.CTkEntry(self.frame_registro, font=fuentes["texto"], show="*", width=400, height=50,
                                           fg_color="#1B3B5F", border_width=0, corner_radius=25,
                                           placeholder_text="Contraseña", placeholder_text_color="#80D8FF", text_color="white", justify="center")
        self.entry_reg_pass.pack(pady=8)

        # Mensajes de error
        self.error_label_reg = ctk.CTkLabel(self.frame_registro, text="", font=fuentes["texto"], text_color="#FF5252")
        self.error_label_reg.pack(pady=5)

        # Botón Registrar
        ctk.CTkButton(self.frame_registro, text="Registrar Perfil", font=fuentes["boton"], 
                      fg_color=COLOR_OK, corner_radius=25, width=400, height=55, 
                      command=self.intentar_registro).pack(pady=10)

        # Enlace para volver
        btn_volver = ctk.CTkButton(self.frame_registro, text="Volver al inicio de sesión", font=fuentes["texto"], 
                                   fg_color="transparent", hover_color="#0D1B2A", text_color=COLOR_BOTON_SEC, 
                                   command=self.ir_a_login)
        btn_volver.pack(pady=5)

    # --- Lógica de la máscara de fecha ---
    def format_fecha(self, event):
        if event.keysym == "BackSpace": return
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
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)

    def ocultar(self):
        self.frame_login.place_forget()
        self.frame_registro.place_forget()

    def ir_a_registro(self):
        self.frame_login.place_forget()
        self.frame_registro.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)
        self.error_label_reg.configure(text="")

    def ir_a_login(self):
        self.frame_registro.place_forget()
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)
        self.error_label_login.configure(text="")
    
    def destroy(self):
        self.frame_container.destroy()

    # --- Acciones ---
    def intentar_login(self):
        user = self.entry_user.get().strip()
        passwd = self.entry_pass.get().strip()
        user_id = db.verificar_usuario(user, passwd)
        if user_id:
            self.error_label_login.configure(text="¡Acceso concedido!", text_color=COLOR_OK)
            self.root.after(1000, lambda: self.login_exitoso_callback(user_id, user))
        else:
            self.error_label_login.configure(text="Usuario o contraseña incorrectos.", text_color="#FF5252")

    def intentar_registro(self):
        nombre = self.entry_reg_nombre.get().strip()
        fecha = self.entry_reg_fecha.get().strip()
        user = self.entry_reg_user.get().strip()
        passwd = self.entry_reg_pass.get().strip()
        
        if not nombre or len(fecha) < 10 or not user or not passwd:
            self.error_label_reg.configure(text="Rellena todos los campos correctamente.", text_color="#FF5252")
            return

        if db.registrar_usuario(user, passwd, nombre, fecha):
            self.entry_reg_nombre.delete(0, tk.END)
            self.entry_reg_fecha.delete(0, tk.END)
            self.entry_reg_user.delete(0, tk.END)
            self.entry_reg_pass.delete(0, tk.END)
            self.ir_a_login()
            self.error_label_login.configure(text="¡Registro exitoso! Ya puedes entrar.", text_color=COLOR_OK)
            self.root.after(3000, lambda: self.error_label_login.configure(text=""))
        else:
            self.error_label_reg.configure(text="Ese usuario ya existe.", text_color="#FF5252")