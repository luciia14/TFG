# posture_definitions.py

def right_arm_stretched(angles, tol=15):
    return (
        abs(angles["right_shoulder"] - 90) <= tol and
        abs(angles["right_elbow"] - 177) <= tol
    )


def left_arm_stretched(angles, tol=15):
    return (
        abs(angles["left_shoulder"] - 90) <= tol and
        abs(angles["left_elbow"] - 177) <= tol
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
