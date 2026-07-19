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
    
    # 2. Tabla de Sesiones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            pack_name TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # 3. Tabla de Historial Detallado
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
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO sesiones (usuario_id, pack_name) VALUES (?, ?)
    ''', (usuario_id, pack_name))
    
    session_id = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO historial_detallado 
        (session_id, hombros_magnitud, codos_magnitud, espalda_magnitud, cadera_magnitud, rodillas_magnitud, cuello_magnitud)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, magnitudes['hombros'], magnitudes['codos'], magnitudes['espalda'], 
          magnitudes['cadera'], magnitudes['rodillas'], magnitudes['cuello']))
    
    conn.commit()
    conn.close()

# --- NUEVAS FUNCIONES PARA EL DASHBOARD ---

def obtener_lista_sesiones(usuario_id):
    """Devuelve fecha y nombre de pack para el panel izquierdo (Treeview)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fecha, pack_name FROM sesiones 
        WHERE usuario_id = ? ORDER BY fecha DESC
    ''', (usuario_id,))
    filas = cursor.fetchall()
    conn.close()
    return [{"fecha": f[0], "pack": f[1]} for f in filas]

def obtener_magnitudes_para_graficos(usuario_id):
    """Devuelve solo los valores de error para los gráficos del panel derecho."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.hombros_magnitud, h.codos_magnitud, h.espalda_magnitud, 
               h.cadera_magnitud, h.rodillas_magnitud, h.cuello_magnitud
        FROM historial_detallado h
        JOIN sesiones s ON h.session_id = s.id
        WHERE s.usuario_id = ?
        ORDER BY s.id ASC
    ''', (usuario_id,))
    filas = cursor.fetchall()
    conn.close()
    return [{
        'hombros': f[0], 'codos': f[1], 'espalda': f[2],
        'cadera': f[3], 'rodillas': f[4], 'cuello': f[5]
    } for f in filas]

def obtener_recomendacion_usuario(usuario_id):
    return "🧠 [Estado IA: Sistema Listo] Completa tu entrenamiento para generar tu perfil biomecánico."

# Inicializamos
inicializar_db()