# posture_definitions.py

def right_arm_stretched(angles, tol=15):
    return (
        abs(angles["right_shoulder"] - 90) <= tol and
        abs(angles["right_elbow"] - 175) <= tol
    )


def left_arm_stretched(angles, tol=15):
    return (
        abs(angles["left_shoulder"] - 90) <= tol and
        abs(angles["left_elbow"] - 175) <= tol
    )


def right_arm_bent_90(angles, tol=15):
    return (
        abs(angles["right_shoulder"] - 90) <= tol and
        abs(angles["right_elbow"] - 90) <= tol
    )


def left_arm_bent_90(angles, tol=15):
    return (
        abs(angles["left_shoulder"] - 90) <= tol and
        abs(angles["left_elbow"] - 90) <= tol
    )


def star_position(angles, tol=15):
    """Posición de estrella evaluando hombros, codos, caderas, rodillas y apertura de piernas"""
    return (
        abs(angles.get("right_shoulder", 0) - 180) <= tol and
        abs(angles.get("left_shoulder", 0) - 180) <= tol and
        abs(angles.get("right_elbow", 0) - 180) <= tol and
        abs(angles.get("left_elbow", 0) - 180) <= tol and
        abs(angles.get("right_hip", 0) - 155) <= tol and
        abs(angles.get("left_hip", 0) - 155) <= tol and
        abs(angles.get("right_knee", 0) - 175) <= tol and
        abs(angles.get("left_knee", 0) - 175) <= tol and
        abs(angles.get("leg_opening", 0) - 68) <= tol
    )