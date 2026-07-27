import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "tfg_entrenamiento.db"

def poblar_20_sesiones_con_criterio():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Crear o recuperar un usuario de prueba exclusivo para esto
    username = "Elenaa11"
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if row:
        usuario_id = row[0]
        print(f"Usando usuario existente '{username}' (ID: {usuario_id})")
    else:
        cursor.execute('''
            INSERT INTO usuarios (username, password, nombre_completo, fecha_nacimiento)
            VALUES (?, ?, ?, ?)
        ''', (username, "1234", "Demostración 20 Sesiones", "10/10/1995"))
        conn.commit()
        usuario_id = cursor.lastrowid
        print(f"Creado nuevo usuario '{username}' con ID {usuario_id}")

    packs = ["Pack 1", "Pack 2", "Pack 3", "Pack 4", "Pack 5"]
    
    print("Generando 20 sesiones en los últimos 4 días con horarios diurnos y errores ajustados...")

    ahora = datetime.now()
    total_sesiones = 20

    for i in range(total_sesiones):
        # -------------------------------------------------------------
        # 1. GENERACIÓN DE FECHA Y HORA (Evitando madrugadas)
        # Distribuimos 5 sesiones por día a lo largo de 4 días (09:30 a 20:30)
        # -------------------------------------------------------------
        dia_offset = 3 - (i // 5)  # Días atrás: 3, 2, 1, 0 (hoy)
        sesion_del_dia = i % 5      # Sesión 0 a 4 dentro de cada día
        
        # Hora base entre las 09:30 y las 19:30 + variación aleatoria de minutos
        hora_base = 9 + (sesion_del_dia * 2.5)  # 9.0, 11.5, 14.0, 16.5, 19.0
        minutos_var = random.randint(0, 45)
        
        fecha_base = (ahora - timedelta(days=dia_offset)).replace(hour=int(hora_base), minute=0, second=0, microsecond=0)
        tiempo_sesion = fecha_base + timedelta(minutes=minutos_var)
        fecha_str = tiempo_sesion.strftime("%Y-%m-%d %H:%M:%S")

        # Seleccionar el pack en orden rotativo
        pack_name = packs[i % len(packs)]

        # Insertar cabecera de sesión
        cursor.execute('''
            INSERT INTO sesiones (usuario_id, pack_name, fecha)
            VALUES (?, ?, ?)
        ''', (usuario_id, pack_name, fecha_str))
        session_id = cursor.lastrowid

        # Tendencia general a la baja (mejora progresiva del usuario)
        factor_mejora = 1.0 - (i / total_sesiones) * 0.75 

        # Función auxiliar para calcular magnitudes
        def calcular_magnitud(multiplicador_pack):
            valor = (850 * factor_mejora * multiplicador_pack) + random.randint(-60, 60)
            return float(min(1000, max(0, int(valor))))

        # -------------------------------------------------------------
        # 2. VALORES POR DEFECTO Y SEGÚN PACK
        # Espalda y Cadera ajustadas a niveles moderados-bajos (0.25 - 0.60)
        # -------------------------------------------------------------
        hombros = calcular_magnitud(0.4)
        codos = calcular_magnitud(0.4)
        rodillas = calcular_magnitud(0.4)
        
        # Espalda y cadera por defecto más bajas
        espalda = calcular_magnitud(0.25)
        cadera = calcular_magnitud(0.25)
        
        # Cuello con los valores más bajos de la aplicación (20 - 120)
        cuello = float(min(120, max(0, int((80 * factor_mejora) + random.randint(-15, 15)))))

        # Asignar lógica de errores según el pack entrenado:
        if pack_name == "Pack 1":
            # Enfocado en Hombros y Codos
            hombros = calcular_magnitud(0.95)
            codos = calcular_magnitud(0.90)

        elif pack_name == "Pack 2":
            # Enfocado en Hombros y MÁS Codos
            hombros = calcular_magnitud(0.85)
            codos = calcular_magnitud(0.98)

        elif pack_name == "Pack 3":
            # Torso/Espalda moderado y un poco de Brazos
            espalda = calcular_magnitud(0.58)  # Moderado (más bajo que antes pero superior al cuello)
            cuello = float(min(150, max(0, int((110 * factor_mejora) + random.randint(-15, 15)))))
            hombros = calcular_magnitud(0.5)
            codos = calcular_magnitud(0.5)

        elif pack_name == "Pack 4":
            # Piernas, Cadera y Espalda
            rodillas = calcular_magnitud(0.80)
            cadera = calcular_magnitud(0.50)   # Moderado-bajo
            espalda = calcular_magnitud(0.48)  # Moderado-bajo
            hombros = calcular_magnitud(0.5)
            codos = calcular_magnitud(0.5)

        elif pack_name == "Pack 5":
            # Piernas intenso (fuerte) -> Rodillas alto, cadera moderado
            rodillas = calcular_magnitud(0.99)
            cadera = calcular_magnitud(0.55)   # Reducido de 0.95 a 0.55
            espalda = calcular_magnitud(0.30)
            hombros = calcular_magnitud(0.3)
            codos = calcular_magnitud(0.3)

        # Insertar los datos detallados de las articulaciones
        cursor.execute('''
            INSERT INTO historial_detallado 
            (session_id, hombros_magnitud, codos_magnitud, espalda_magnitud, cadera_magnitud, rodillas_magnitud, cuello_magnitud)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, hombros, codos, espalda, cadera, rodillas, cuello))

    conn.commit()
    conn.close()
    print("¡Se han insertado con éxito las 20 sesiones en horarios diurnos y con errores progresivos adecuados!")

if __name__ == "__main__":
    poblar_20_sesiones_con_criterio()