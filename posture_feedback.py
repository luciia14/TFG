# posture_feedback.py

def feedback_joint(angle, target_angle, joint_name, joint_type, engine, tolerance=6):
    """
    Calcula el feedback de una articulación según la diferencia con el ángulo objetivo.
    """
    diff = target_angle - angle

    if joint_type == "hombro":
        llave_motor = "hombros"
    elif joint_type == "codo":
        llave_motor = "codos"
    elif joint_type in ["rodilla", "apertura", "cadera"]:
        llave_motor = "piernas"
    else:
        llave_motor = "general"
        
    if hasattr(engine, "update"):
        engine.update(llave_motor, diff)

    if abs(diff) < tolerance:
        return None

    band_high = tolerance + 18

    if joint_type == "hombro":
        if tolerance <= diff < band_high:
            return f"Sube un poco más el {joint_name}"
        elif diff >= band_high:
            return f"Sube bastante el {joint_name}"
        elif -band_high < diff <= -tolerance:
            return f"Baja un poco el {joint_name}"
        elif diff <= -band_high:
            return f"Baja bastante el {joint_name}"

    elif joint_type == "codo":
        if tolerance <= diff < band_high:
            return f"Abre un poco el {joint_name}"
        elif diff >= band_high:
            return f"Abre bastante el {joint_name}"
        elif -band_high < diff <= -tolerance:
            return f"Cierra un poco el {joint_name}"
        elif diff <= -band_high:
            return f"Cierra bastante el {joint_name}"

    elif joint_type == "rodilla":
        if tolerance <= diff < band_high:
            return f"Extiende un poco más la {joint_name}"
        elif diff >= band_high:
            return f"Extiende bastante la {joint_name}"
        elif -band_high < diff <= -tolerance:
            return f"Flexiona un poco la {joint_name}"
        elif diff <= -band_high:
            return f"Flexiona bastante la {joint_name}"

    elif joint_type == "apertura":
        if tolerance <= diff < band_high:
            return "Abre un poco las piernas"
        elif diff >= band_high:
            return "Abre bastante las piernas"
        elif -band_high < diff <= -tolerance:
            return "Cierra un poco las piernas"
        elif diff <= -band_high:
            return "Cierra bastante las piernas"

    elif joint_type == "cadera":
        if tolerance <= diff < band_high:
            return f"Sube un poco la {joint_name}"
        elif diff >= band_high:
            return f"Sube bastante la {joint_name}"
        elif -band_high < diff <= -tolerance:
            return f"Baja un poco la {joint_name}"
        elif diff <= -band_high:
            return f"Baja bastante la {joint_name}"

    elif joint_type == "tronco":
        if tolerance <= diff < band_high:
            return f"Inclina un poco más el {joint_name}"
        elif diff >= band_high:
            return f"Inclina bastante más el {joint_name}"
        elif -band_high < diff <= -tolerance:
            return f"Endereza un poco el {joint_name}"
        elif diff <= -band_high:
            return f"Endereza bastante el {joint_name}"

    elif joint_type == "cuello":
        if tolerance <= diff < band_high:
            return f"Alinea un poco más el {joint_name}"
        elif diff >= band_high:
            return f"Alinea bastante el {joint_name}"
        elif -band_high < diff <= -tolerance:
            return f"Flexiona un poco el {joint_name}"
        elif diff <= -band_high:
            return f"Flexiona bastante el {joint_name}"


def generate_feedback(angles, state, engine, landmarks=None):
    """
    Genera feedback postural y verifica visibilidad de landmarks.
    """
    feedbacks = []

    # Mapeo de articulaciones y métricas a índices de MediaPipe
    joint_to_landmark_idx = {
        "right_shoulder": [12],
        "left_shoulder": [11],
        "right_elbow": [14],
        "left_elbow": [13],
        "right_hip": [24],
        "left_hip": [23],
        "right_knee": [25],
        "left_knee": [26],
        "neck": [0, 11, 12],
        "trunk": [11, 12, 23, 24],
        "leg_opening": [23, 24, 25, 26]
    }

    # Objetivos y tolerancias según el estado
    if state == 0:  # Brazos estirados
        targets = {
            "right_shoulder": 90,
            "right_elbow": 180,
            "left_shoulder": 90,
            "left_elbow": 180
        }
        tolerance = 6
    elif state == 3:  # Sentadilla lateral de perfil con brazos estirados
        targets = {
            "trunk": 35,
            "right_hip": 110,
            "right_knee": 120,
            "right_shoulder": 90,
            "right_elbow": 180
        }
        tolerance = 15
    elif state == 2:  # Posición de estrella
        targets = {
            "right_shoulder": 180,
            "left_shoulder": 180,
            "right_elbow": 180,
            "left_elbow": 180,
            "right_knee": 165,
            "left_knee": 165,
            "leg_opening": 68
        }
        tolerance = 6
    elif state == 1:  # Brazos doblados a 90°
        targets = {
            "right_shoulder": 90,
            "right_elbow": 90,
            "left_shoulder": 90,
            "left_elbow": 90
        }
        tolerance = 6
    elif state == 4:  # Posición en T (t_pose)
        targets = {
            "right_shoulder": 90,
            "left_shoulder": 90,
            "right_elbow": 175,
            "left_elbow": 175
        }
        tolerance = 6
    elif state == 5:  # Zancada (lunge_position)
        targets = {
            "right_knee": 90,
            "left_knee": 175,
            "right_hip": 120,
            "left_hip": 170
        }
        tolerance = 15
    elif state == 6:  # Alineación de cuerpo completo (full_body_alignment_position)
        targets = {
            "neck": 170,
            "trunk": 45,
            "right_shoulder": 90,
            "left_shoulder": 90,
            "right_elbow": 175,
            "left_elbow": 175,
            "right_hip": 120,
            "left_hip": 120,
            "right_knee": 130,
            "left_knee": 130
        }
        tolerance = 15
    else:
        targets = {}
        tolerance = 6

    nombres_castellano = {
        "right_shoulder": "brazo derecho",
        "left_shoulder": "brazo izquierdo",
        "right_elbow": "codo derecho",
        "left_elbow": "codo izquierdo",
        "right_knee": "rodilla derecha",
        "left_knee": "rodilla izquierda",
        "right_hip": "cadera derecha",
        "left_hip": "cadera izquierda",
        "leg_opening": "apertura",
        "trunk": "tronco",
        "neck": "cuello"
    }

    tipos_articulacion = {
        "right_shoulder": "hombro",
        "left_shoulder": "hombro",
        "right_elbow": "codo",
        "left_elbow": "codo",
        "right_knee": "rodilla",
        "left_knee": "rodilla",
        "right_hip": "cadera",
        "left_hip": "cadera",
        "leg_opening": "apertura",
        "trunk": "tronco",
        "neck": "cuello"
    }

    # Comprobación de oclusión global
    if landmarks is not None:
        for joint in targets.keys():
            if joint in joint_to_landmark_idx:
                indices = joint_to_landmark_idx[joint]
                for idx in indices:
                    if idx < len(landmarks):
                        if hasattr(landmarks[idx], 'visibility') and landmarks[idx].visibility < 0.5:
                            nombre_art = nombres_castellano.get(joint, joint)
                            feedbacks.append(f"Oclusión en pantalla: {nombre_art} no visible")
                            break
            if feedbacks:
                break

        if feedbacks:
            return feedbacks

    # Cálculo de feedback si los puntos son visibles
    for joint, target_angle in targets.items():
        if joint not in angles:
            continue
            
        joint_spanish = nombres_castellano.get(joint, joint)
        joint_type = tipos_articulacion.get(joint, "hombro")
        
        f = feedback_joint(angles[joint], target_angle, joint_spanish, joint_type, engine, tolerance=tolerance)
        if f:
            feedbacks.append(f)

    if not feedbacks:
        feedbacks.append("POSICIÓN CORRECTA")

    return feedbacks