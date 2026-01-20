# posture_definitions.py

def right_arm_90deg_correct(angles,
                            shoulder_target=90,
                            elbow_target=180,
                            shoulder_tol=15,
                            elbow_tol=15):
    

    shoulder = angles["right_shoulder"]
    elbow = angles["right_elbow"]

    shoulder_ok = abs(shoulder - shoulder_target) <= shoulder_tol
    elbow_ok = abs(elbow - elbow_target) <= elbow_tol

    return shoulder_ok and elbow_ok
