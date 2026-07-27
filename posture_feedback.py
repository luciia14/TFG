# posture_feedback.py

def feedback_joint(angle, target_angle, joint_name, joint_type, engine):
    """
    Calcula el feedback d'una articulació según la diferencia con el ángulo objetivo.
    joint_type: 'hombro', 'codo', 'rodilla' o 'apertura'
    """
    diff = target_angle - angle

    # --- INTEGRACIÓN: Registramos el error en el motor ---
    if joint_type == "hombro":
        llave_motor = "hombros"
    elif joint_type == "codo":
        llave_motor = "codos"
    elif joint_type in ["rodilla", "apertura"]:
        llave_motor = "piernas"
    else:
        llave_motor = "general"
        
    if hasattr(engine, "update"):
        engine.update(llave_motor, diff)

    if abs(diff) < 5:
        return None

    # Feedback según el tipo de articulación con escala (poco / bastante)
    if joint_type == "hombro":
        if 10 <= diff < 25:
            return f"Sube un poco más el {joint_name}"
        elif diff >= 25:
            return f"Sube bastante el {joint_name}"
        elif -25 < diff <= -5:
            return f"Baja un poco el {joint_name}"
        elif diff <= -25:
            return f"Baja bastante el {joint_name}"

    elif joint_type == "codo":
        if 15 <= diff < 25:
            return f"Abre un poco el {joint_name}"
        elif diff >= 25:
            return f"Abre bastante el {joint_name}"
        elif -25 < diff <= -5:
            return f"Cierra un poco el {joint_name}"
        elif diff <= -25:
            return f"Cierra bastante el {joint_name}"

    elif joint_type == "rodilla":
        if 10 <= diff < 25:
            return f"Extiende un poco más la {joint_name}"
        elif diff >= 25:
            return f"Extiende bastante la {joint_name}"
        elif -25 < diff <= -5:
            return f"Flexiona un poco la {joint_name}"
        elif diff <= -25:
            return f"Flexiona bastante la {joint_name}"

    elif joint_type == "apertura":
        if 10 <= diff < 25:
            return "Abre un poco las piernas"
        elif diff >= 25:
            return "Abre bastante las piernas"
        elif -25 < diff <= -5:
            return "Cierra un poco las piernas"
        elif diff <= -25:
            return "Cierra bastante las piernas"


def generate_feedback(angles, state, engine):
    """
    Genera feedback según la fase actual (state) y los ángulos medidos.
    state = 0 → posición de estrella
    state = 1 → brazos doblados 90°
    state = 2 → brazos estirados
    """
    feedbacks = []

    # Definir objetivos según el estado/ejercicio actual
    if state == 2:  # Fase brazos estirados
        targets = {
            "right_shoulder": 90,
            "right_elbow": 180,
            "left_shoulder": 90,
            "left_elbow": 180
        }
    elif state == 1:  # Fase brazos doblados 90°
        targets = {
            "right_shoulder": 90,
            "right_elbow": 90,
            "left_shoulder": 90,
            "left_elbow": 90
        }
    elif state == 0:  # Posición de estrella (sin caderas)
        targets = {
            "right_shoulder": 180,
            "left_shoulder": 180,
            "right_elbow": 180,
            "left_elbow": 180,
            "right_knee": 175,
            "left_knee": 175,
            "leg_opening": 68
        }
    else:
        targets = {}

    # Diccionario para traducir nombres al castellano
    nombres_castellano = {
        "right_shoulder": "brazo derecho",
        "left_shoulder": "brazo izquierdo",
        "right_elbow": "codo derecho",
        "left_elbow": "codo izquierdo",
        "right_knee": "rodilla derecha",
        "left_knee": "rodilla izquierda",
        "leg_opening": "apertura"
    }

    # Clasificación del tipo de articulación para cada clave
    tipos_articulacion = {
        "right_shoulder": "hombro",
        "left_shoulder": "hombro",
        "right_elbow": "codo",
        "left_elbow": "codo",
        "right_knee": "rodilla",
        "left_knee": "rodilla",
        "leg_opening": "apertura"
    }

    for joint, target_angle in targets.items():
        if joint not in angles:
            continue
            
        joint_spanish = nombres_castellano.get(joint, joint)
        joint_type = tipos_articulacion.get(joint, "hombro")
        
        f = feedback_joint(angles[joint], target_angle, joint_spanish, joint_type, engine)
        if f:
            feedbacks.append(f)

    if not feedbacks:
        feedbacks.append("POSICIÓN CORRECTA")

    return feedbacks