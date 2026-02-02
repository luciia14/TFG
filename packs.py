# exercise_packs.py

from posture_definitions import (
    right_arm_stretched,
    left_arm_stretched,
    right_arm_bent_90,
    left_arm_bent_90
)

# Cada exercici és una funció que rep els angles i retorna True si és correcte
# i False si no ho és. També podem afegir un nom descriptiu per a la interfície.

# ---------------- PACK 1 ----------------
def ejercicio1_pack1(angles):
    """Ambdós braços completament estirats"""
    return right_arm_stretched(angles) and left_arm_stretched(angles)

def ejercicio2_pack1(angles):
    """Ambdós braços doblats a 90°"""
    return right_arm_bent_90(angles) and left_arm_bent_90(angles)

pack1 = [
    {"nombre": "Brazos estirados", "funcion": ejercicio1_pack1},
    {"nombre": "Brazos a 90°", "funcion": ejercicio2_pack1}
]

# ---------------- PACK 2 ----------------
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

# Diccionari de tots els packs per facilitar la selecció
exercise_packs = {
    "Pack 1": pack1,
    "Pack 2": pack2
}
