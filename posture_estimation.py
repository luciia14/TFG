# posture_estimation.py
import math
import numpy as np

# Índexs MediaPipe per al braç dret i esquerre
RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
RIGHT_WRIST = 16

LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15


def compute_angle(a, b, c):
    """Calcula l'angle en graus format pels punts a-b-c"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = math.degrees(math.acos(cosine_angle))
    return angle


def get_arm_angle(landmarks, image_shape, side="right"):
    """
    Retorna l'angle del braç dret o esquerre a partir de landmarks
    landmarks: result.pose_landmarks[0]
    image_shape: shape de l'imatge (h, w)
    side: "right" o "left"
    """
    h, w, _ = image_shape

    if side == "right":
        a = landmarks[RIGHT_SHOULDER]
        b = landmarks[RIGHT_ELBOW]
        c = landmarks[RIGHT_WRIST]
    else:
        a = landmarks[LEFT_SHOULDER]
        b = landmarks[LEFT_ELBOW]
        c = landmarks[LEFT_WRIST]

    point_a = (a.x * w, a.y * h)
    point_b = (b.x * w, b.y * h)
    point_c = (c.x * w, c.y * h)

    return compute_angle(point_a, point_b, point_c)
