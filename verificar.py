import sqlite3

def verificar_datos_entrenamiento():
    db_name = "tfg_entrenamiento.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    print(f"\n--- Resumen de Sesiones ---")
    cursor.execute("SELECT * FROM sesiones")
    sesiones = cursor.fetchall()
    for s in sesiones:
        print(f"ID Sesión: {s[0]} | Usuario ID: {s[1]} | Pack: {s[2]} | Fecha: {s[3]}")

    print(f"\n--- Detalle Biomecánico (Magnitudes de Error) ---")
    cursor.execute("SELECT * FROM historial_detallado")
    detalles = cursor.fetchall()
    for d in detalles:
        # Imprimimos las magnitudes detectadas para esa sesión
        print(f"Sesión ID: {d[0]} | Hombros: {d[1]:.2f} | Codos: {d[2]:.2f} | Espalda: {d[3]:.2f} | Cadera: {d[4]:.2f} | Rodillas: {d[5]:.2f} | Cuello: {d[6]:.2f}")

    conn.close()

if __name__ == "__main__":
    verificar_datos_entrenamiento()