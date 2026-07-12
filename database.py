# database.py
import sqlite3

DB_NAME = "tfg_entrenamiento.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    """Crea la tabla de usuarios con campos profesionales si no existe."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabla de Usuarios ampliada con Perfil
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre_completo TEXT,
            fecha_nacimiento TEXT
        )
    ''')
    
    # Tabla de Historial vacía por ahora (esquema inicial funcional)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            pack_name TEXT,
            ejercicios_completados INTEGER,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def registrar_usuario(username, password, nombre_completo, fecha_nacimiento):
    """Registra un nuevo usuario con su perfil completo."""
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
        return False  # El nombre de usuario ya existe

def verificar_usuario(username, password):
    """Verifica credenciales. Devuelve el ID del usuario o None si son incorrectas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def obtener_recomendacion_usuario(usuario_id):
    """Función temporal integrada para que no falle app_gui.py"""
    return "🧠 [Estado IA: Sin Historial] ¡Bienvenido! Completa tus primeros packs para analizar tu postura."

# Inicializamos automáticamente al importar
inicializar_db()