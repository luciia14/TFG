# posture_estimation.py
import math
import numpy as np

# Índices MediaPipe para extremidades, tronco y cabeza
NARIZ = 0
RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
RIGHT_WRIST = 16
LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15
RIGHT_HIP = 24
LEFT_HIP = 23
RIGHT_KNEE = 25
LEFT_KNEE = 26
RIGHT_ANKLE = 27
LEFT_ANKLE = 28


def compute_angle(a, b, c):
    """Calcula el ángulo en grados formado por los puntos a-b-c"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0:
        return 0.0

    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = math.degrees(math.acos(cosine_angle))
    return angle


def right_elbow_angle(landmarks, image_shape):
    """Ángulo codo derecho: hombro-codo-muñeca"""
    h, w, _ = image_shape
    a = landmarks[RIGHT_SHOULDER]
    b = landmarks[RIGHT_ELBOW]
    c = landmarks[RIGHT_WRIST]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def left_elbow_angle(landmarks, image_shape):
    """Ángulo codo izquierdo: hombro-codo-muñeca"""
    h, w, _ = image_shape
    a = landmarks[LEFT_SHOULDER]
    b = landmarks[LEFT_ELBOW]
    c = landmarks[LEFT_WRIST]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def right_shoulder_angle(landmarks, image_shape):
    """Ángulo hombro derecho: codo-hombro-cadera"""
    h, w, _ = image_shape
    a = landmarks[RIGHT_ELBOW]
    b = landmarks[RIGHT_SHOULDER]
    c = landmarks[RIGHT_HIP]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def left_shoulder_angle(landmarks, image_shape):
    """Ángulo hombro izquierdo: codo-hombro-cadera"""
    h, w, _ = image_shape
    a = landmarks[LEFT_ELBOW]
    b = landmarks[LEFT_SHOULDER]
    c = landmarks[LEFT_HIP]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def right_hip_angle(landmarks, image_shape):
    """Ángulo cadera derecha: hombro-cadera-rodilla"""
    h, w, _ = image_shape
    a = landmarks[RIGHT_SHOULDER]
    b = landmarks[RIGHT_HIP]
    c = landmarks[RIGHT_KNEE]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def left_hip_angle(landmarks, image_shape):
    """Ángulo cadera izquierda: hombro-cadera-rodilla"""
    h, w, _ = image_shape
    a = landmarks[LEFT_SHOULDER]
    b = landmarks[LEFT_HIP]
    c = landmarks[LEFT_KNEE]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def right_knee_angle(landmarks, image_shape):
    """Ángulo rodilla derecha: cadera-rodilla-tobillo"""
    h, w, _ = image_shape
    a = landmarks[RIGHT_HIP]
    b = landmarks[RIGHT_KNEE]
    c = landmarks[RIGHT_ANKLE]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def left_knee_angle(landmarks, image_shape):
    """Ángulo rodilla izquierda: cadera-rodilla-tobillo"""
    h, w, _ = image_shape
    a = landmarks[LEFT_HIP]
    b = landmarks[LEFT_KNEE]
    c = landmarks[LEFT_ANKLE]
    return compute_angle((a.x*w, a.y*h), (b.x*w, b.y*h), (c.x*w, c.y*h))


def leg_opening_angle(landmarks, image_shape):
    """Ángulo de apertura de piernas tomando como vértice el punto medio de las caderas"""
    h, w, _ = image_shape
    cadera_izq = (landmarks[LEFT_HIP].x * w, landmarks[LEFT_HIP].y * h)
    cadera_der = (landmarks[RIGHT_HIP].x * w, landmarks[RIGHT_HIP].y * h)
    
    centro_caderas = (
        (cadera_izq[0] + cadera_der[0]) / 2,
        (cadera_izq[1] + cadera_der[1]) / 2
    )
    
    rodilla_izq = (landmarks[LEFT_KNEE].x * w, landmarks[LEFT_KNEE].y * h)
    rodilla_der = (landmarks[RIGHT_KNEE].x * w, landmarks[RIGHT_KNEE].y * h)
    
    return compute_angle(rodilla_izq, centro_caderas, rodilla_der)


def trunk_inclination(landmarks, image_shape):
    """Calcula la inclinación del tronco respecto a la vertical"""
    h, w, _ = image_shape
    centro_hombros = np.array([
        (landmarks[LEFT_SHOULDER].x + landmarks[RIGHT_SHOULDER].x) * w / 2,
        (landmarks[LEFT_SHOULDER].y + landmarks[RIGHT_SHOULDER].y) * h / 2
    ])
    centro_caderas = np.array([
        (landmarks[LEFT_HIP].x + landmarks[RIGHT_HIP].x) * w / 2,
        (landmarks[LEFT_HIP].y + landmarks[RIGHT_HIP].y) * h / 2
    ])
    vector_vertical = np.array([0, -1])
    vector_tronco = centro_hombros - centro_caderas
    norma = np.linalg.norm(vector_tronco)
    if norma == 0:
        return 0.0
    vector_tronco = vector_tronco / norma
    cosine_angle = np.clip(np.dot(vector_tronco, vector_vertical), -1.0, 1.0)
    angle = math.degrees(math.acos(cosine_angle))
    return angle


def get_all_angles(landmarks, image_shape):
    """Devuelve todos los ángulos necesarios en un diccionario"""
    return {
        "right_elbow": right_elbow_angle(landmarks, image_shape),
        "left_elbow": left_elbow_angle(landmarks, image_shape),
        "right_shoulder": right_shoulder_angle(landmarks, image_shape),
        "left_shoulder": left_shoulder_angle(landmarks, image_shape),
        "right_hip": right_hip_angle(landmarks, image_shape),
        "left_hip": left_hip_angle(landmarks, image_shape),
        "right_knee": right_knee_angle(landmarks, image_shape),
        "left_knee": left_knee_angle(landmarks, image_shape),
        "leg_opening": leg_opening_angle(landmarks, image_shape),
        "trunk": trunk_inclination(landmarks, image_shape)
    }