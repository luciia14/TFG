# exercise_packs.py

from posture_definitions import (
    right_arm_stretched,
    left_arm_stretched,
    right_arm_bent_90,
    left_arm_bent_90,
    star_position
)

# ---------------- PACK 1: BÁSICO DE BRAZOS ----------------
def ejercicio1_pack1(angles):
    """Ambos brazos completamente estirados"""
    return right_arm_stretched(angles) and left_arm_stretched(angles)

def ejercicio2_pack1(angles):
    """Ambos brazos doblados a 90°"""
    return right_arm_bent_90(angles) and left_arm_bent_90(angles)

pack1 = [
    {"nombre": "Brazos estirados", "funcion": ejercicio1_pack1},
    {"nombre": "Brazos a 90°", "funcion": ejercicio2_pack1}
]

# ---------------- PACK 2: POSTURAS CRUZADAS ----------------
def ejercicio1_pack2(angles):
    """Brazo derecho a 90°, brazo izquierdo estirado"""
    return right_arm_bent_90(angles) and left_arm_stretched(angles)

def ejercicio2_pack2(angles):
    """Brazo derecho estirado, brazo izquierdo a 90°"""
    return right_arm_stretched(angles) and left_arm_bent_90(angles)

pack2 = [
    {"nombre": "Brazo derecho 90°, izquierdo estirado", "funcion": ejercicio1_pack2},
    {"nombre": "Brazo derecho estirado, izquierdo 90°", "funcion": ejercicio2_pack2}
]

# ---------------- PACK 3: ESTRELLA Y FOCALIZADO DERECHO ----------------
def ejercicio1_pack3(angles):
    """Posición de estrella"""
    return star_position(angles)

def ejercicio2_pack3(angles):
    """Brazo derecho estirado"""
    return right_arm_stretched(angles)

pack3 = [
    {"nombre": "Posición de estrella", "funcion": ejercicio1_pack3},
    {"nombre": "Brazo derecho estirado", "funcion": ejercicio2_pack3}
]

# ---------------- PACK 4: FOCALIZADO IZQUIERDO ----------------
def ejercicio1_pack4(angles):
    """Brazo izquierdo estirado"""
    return left_arm_stretched(angles)

def ejercicio2_pack4(angles):
    """Brazo izquierdo doblado a 90°"""
    return left_arm_bent_90(angles)

pack4 = [
    {"nombre": "Brazo izquierdo estirado", "funcion": ejercicio1_pack4},
    {"nombre": "Brazo izquierdo a 90°", "funcion": ejercicio2_pack4}
]

# ---------------- PACK 5: CIRCUITO COMPLETO ----------------
def ejercicio1_pack5(angles):
    """Ambos brazos estirados"""
    return right_arm_stretched(angles) and left_arm_stretched(angles)

def ejercicio2_pack5(angles):
    """Brazo derecho a 90°, izquierdo estirado"""
    return right_arm_bent_90(angles) and left_arm_stretched(angles)

def ejercicio3_pack5(angles):
    """Ambos brazos a 90°"""
    return right_arm_bent_90(angles) and left_arm_bent_90(angles)

def ejercicio4_pack5(angles):
    """Brazo derecho estirado, izquierdo a 90°"""
    return right_arm_stretched(angles) and left_arm_bent_90(angles)

pack5 = [
    {"nombre": "1. Ambos estirados", "funcion": ejercicio1_pack5},
    {"nombre": "2. Derecho 90°, izquierdo estirado", "funcion": ejercicio2_pack5},
    {"nombre": "3. Ambos a 90°", "funcion": ejercicio3_pack5},
    {"nombre": "4. Derecho estirado, izquierdo 90°", "funcion": ejercicio4_pack5}
]

# Diccionario de todos los packs para la selección automática en la interfaz
exercise_packs = {
    "Pack 1": pack1,
    "Pack 2": pack2,
    "Pack 3": pack3,
    "Pack 4": pack4,
    "Pack 5": pack5
}