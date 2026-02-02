# posture_feedback.py

def feedback_joint(angle, target_angle, joint_name, joint_type):
    """
    Calcula el feedback d'una articulación según la diferencia con el ángulo objetivo.
    joint_type: 'hombro' o 'codo'
    """
    diff = target_angle - angle

    if abs(diff) < 5:
        return None

    # Feedback segons el tipus d'articulació
    if joint_type == "hombro":
        if 5 <= diff < 15:
            return f"Sube un poco más el {joint_name}"
        elif diff >= 15:
            return f"Sube bastante el {joint_name}"
        elif -15 < diff <= -5:
            return f"Baja un poco el {joint_name}"
        elif diff <= -15:
            return f"Baja bastante el {joint_name}"

    elif joint_type == "codo":
        if 5 <= diff < 15:
            return f"Abre un poco el {joint_name}"
        elif diff >= 15:
            return f"Abre bastante el {joint_name}"
        elif -15 < diff <= -5:
            return f"Cierra un poco el {joint_name}"
        elif diff <= -15:
            return f"Cierra bastante el {joint_name}"


def generate_feedback(angles, state):
    """
    Genera feedback según la fase actual (state) y los ángulos medidos.
    state = 0 → brazos estirados
    state = 1 → brazos doblados 90°
    """
    feedbacks = []

    # Mantener las claves en inglés
    if state == 0:  # Fase brazos estirados
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
    else:
        targets = {}

    # Diccionario para traducir nombres al castellano
    nombres_castellano = {
        "right_shoulder": "brazo derecho",
        "left_shoulder": "brazo izquierdo",
        "right_elbow": "codo derecho",
        "left_elbow": "codo izquierdo"
    }

    tipos_articulacion = {
        "right_shoulder": "hombro",
        "left_shoulder": "hombro",
        "right_elbow": "codo",
        "left_elbow": "codo"
    }

    for joint, target_angle in targets.items():
        joint_spanish = nombres_castellano.get(joint, joint)
        joint_type = tipos_articulacion.get(joint, "hombro")
        f = feedback_joint(angles[joint], target_angle, joint_spanish, joint_type)
        if f:
            feedbacks.append(f)

    if not feedbacks:
        feedbacks.append("POSICIÓN CORRECTA")

    return feedbacks
