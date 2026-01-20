# posture_definitions.py

def right_arm_stretched(angles, tol_shoulder=15, tol_elbow=15):
    return (
        abs(angles["right_shoulder"] - 90) <= tol_shoulder and
        abs(angles["right_elbow"] - 180) <= tol_elbow
    )


def left_arm_stretched(angles, tol_shoulder=15, tol_elbow=15):
    return (
        abs(angles["left_shoulder"] - 90) <= tol_shoulder and
        abs(angles["left_elbow"] - 180) <= tol_elbow
    )

