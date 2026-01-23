# posture_feedback.py

def feedback_joint(angle, target_angle, joint_name):
    """
    Calcula el feedback d'una articulació segons la diferència amb l'angle objectiu.
    Retorna None si està dins del marge petit.
    """
    diff = target_angle - angle

    if abs(diff) < 5:
        return None
    elif 5 <= diff < 15:
        return f"Sube un poco {joint_name}"
    elif diff >= 15:
        return f"Sube bastante {joint_name}"
    elif -15 < diff <= -5:
        return f"Baja un poco {joint_name}"
    elif diff <= -15:
        return f"Baja bastante {joint_name}"


def generate_feedback(angles, state):
    """
    Genera feedback segons la fase actual (state) i els angles mesurats.
    state = 0 → braços estirats
    state = 1 → braços doblats 90°
    """
    feedbacks = []

    if state == 0:  # Fase braços estirats
        targets = {
            "right_shoulder": 90,
            "right_elbow": 180,
            "left_shoulder": 90,
            "left_elbow": 180
        }
    elif state == 1:  # Fase braços doblats 90°
        targets = {
            "right_shoulder": 90,
            "right_elbow": 90,
            "left_shoulder": 90,
            "left_elbow": 90
        }
    else:
        targets = {}

    for joint, target_angle in targets.items():
        f = feedback_joint(angles[joint], target_angle, joint.replace("_", " "))
        if f:
            feedbacks.append(f)

    if not feedbacks:
        feedbacks.append("POSICIÓN CORRECTA")

    return feedbacks
