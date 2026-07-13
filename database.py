import sqlite3

DB_NAME = "tfg_entrenamiento.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    """Crea la estructura completa de la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Tabla de Usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre_completo TEXT,
            fecha_nacimiento TEXT
        )
    ''')
    
    # 2. Tabla de Sesiones (Resumen del entrenamiento)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            pack_name TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # 3. Tabla de Historial Detallado (Análisis biomecánico en crudo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_detallado (
            session_id INTEGER PRIMARY KEY,
            hombros_magnitud REAL,
            codos_magnitud REAL,
            espalda_magnitud REAL,
            cadera_magnitud REAL,
            rodillas_magnitud REAL,
            cuello_magnitud REAL,
            FOREIGN KEY(session_id) REFERENCES sesiones(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- FUNCIONES DE USUARIO ---

def registrar_usuario(username, password, nombre_completo, fecha_nacimiento):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (username, password, nombre_completo, fecha_nacimiento) 
            VALUES (?, ?, ?, ?)
        ''', (username, password, nombre_completo, fecha_nacimiento))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verificar_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

# --- FUNCIONES DE ANÁLISIS BIOMECÁNICO ---

def guardar_sesion_completa(usuario_id, pack_name, magnitudes):
    """
    Guarda el resumen de la sesión y los valores en crudo del análisis.
    magnitudes: dict {'hombros': 0.0, 'codos': 0.0, ...}
    """
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Registrar sesión
    cursor.execute('''
        INSERT INTO sesiones (usuario_id, pack_name) VALUES (?, ?)
    ''', (usuario_id, pack_name))
    
    session_id = cursor.lastrowid
    
    # 2. Registrar detalle (valores en crudo)
    cursor.execute('''
        INSERT INTO historial_detallado 
        (session_id, hombros_magnitud, codos_magnitud, espalda_magnitud, cadera_magnitud, rodillas_magnitud, cuello_magnitud)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, magnitudes['hombros'], magnitudes['codos'], magnitudes['espalda'], 
          magnitudes['cadera'], magnitudes['rodillas'], magnitudes['cuello']))
    
    conn.commit()
    conn.close()

def obtener_recomendacion_usuario(usuario_id):
    """
    En el futuro, aquí consultaremos los datos de 'historial_detallado' 
    para sugerir el pack que más necesite el usuario.
    """
    return "🧠 [Estado IA: Sistema Listo] Completa tu entrenamiento para generar tu perfil biomecánico."

# Inicializamos la base de datos al importar el módulo
inicializar_db()