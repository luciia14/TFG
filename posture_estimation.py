# posture_estimation.py
import math
import numpy as np

# Índices MediaPipe para brazos, hombros y codos
RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
RIGHT_WRIST = 16
LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15
RIGHT_HIP = 24
LEFT_HIP = 23


def compute_angle(a, b, c):
    """Calcula el ángulo en grados formado por los puntos a-b-c"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
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


def get_all_angles(landmarks, image_shape):
    """Devuelve todos los ángulos en un diccionario"""
    return {
        "right_elbow": right_elbow_angle(landmarks, image_shape),
        "left_elbow": left_elbow_angle(landmarks, image_shape),
        "right_shoulder": right_shoulder_angle(landmarks, image_shape),
        "left_shoulder": left_shoulder_angle(landmarks, image_shape)
    }

