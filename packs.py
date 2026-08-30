# exercise_packs.py

from posture_definitions import (
    right_arm_stretched,
    left_arm_stretched,
    arms_bent_90,
    both_arms_up,
    torso_inclined,
    star_position,
    squat_position,
    lateral_squat_arms_up_position,
    t_pose,
    lunge_position,
    full_body_alignment_position
)

# ---------------- PACK 1: HOMBROS Y CODOS (BÁSICO) ----------------
def ejercicio1_pack1(angles):
    """Ambos brazos extendidos horizontalmente"""
    return right_arm_stretched(angles) and left_arm_stretched(angles)

def ejercicio2_pack1(angles):
    """Ambos brazos flexionados a 90°"""
    return arms_bent_90(angles)

pack1 = [
    {"nombre": "Brazos estirados", "funcion": ejercicio1_pack1},
    {"nombre": "Brazos a 90°", "funcion": ejercicio2_pack1}
]

# ---------------- PACK 2: HOMBROS Y CODOS (INTERMEDIO) ----------------
def ejercicio1_pack2(angles):
    """Apertura horizontal en postura T"""
    return t_pose(angles)

def ejercicio2_pack2(angles):
    """Elevación vertical de brazos sobre la cabeza"""
    return both_arms_up(angles)

pack2 = [
    {"nombre": "Posición en T", "funcion": ejercicio1_pack2},
    {"nombre": "Brazos elevados", "funcion": ejercicio2_pack2}
]

# ---------------- PACK 3: CUELLO, TORSO Y BRAZOS ----------------
def ejercicio1_pack3(angles):
    """Inclinación de tronco con alineación de cuello y brazos"""
    return torso_inclined(angles)

def ejercicio2_pack3(angles):
    """Alineación postural de cuerpo completo"""
    return full_body_alignment_position(angles)

pack3 = [
    {"nombre": "Inclinación de torso", "funcion": ejercicio1_pack3},
    {"nombre": "Alineación corporal completa", "funcion": ejercicio2_pack3}
]

# ---------------- PACK 4: PIERNAS, CUELLO, TORSO Y BRAZOS ----------------
def ejercicio1_pack4(angles):
    """Apertura global en posición de estrella"""
    return star_position(angles)

def ejercicio2_pack4(angles):
    """Sentadilla básica simétrica"""
    return squat_position(angles)

pack4 = [
    {"nombre": "Posición de estrella", "funcion": ejercicio1_pack4},
    {"nombre": "Sentadilla básica", "funcion": ejercicio2_pack4}
]

# ---------------- PACK 5: PIERNAS INTENSO ----------------
def ejercicio1_pack5(angles):
    """Sentadilla lateral con elevación de brazos"""
    return lateral_squat_arms_up_position(angles)

def ejercicio2_pack5(angles):
    """Zancada baja manteniendo alineación de cadera y rodilla"""
    return lunge_position(angles)

pack5 = [
    {"nombre": "Sentadilla lateral con brazos", "funcion": ejercicio1_pack5},
    {"nombre": "Zancada postural", "funcion": ejercicio2_pack5}
]

# Diccionario de selección de rutinas para la interfaz de usuario
exercise_packs = {
    "Pack 1": pack1,
    "Pack 2": pack2,
    "Pack 3": pack3,
    "Pack 4": pack4,
    "Pack 5": pack5
}