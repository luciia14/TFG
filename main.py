# main.py
import time
import cv2
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_definitions import (
    right_arm_stretched,
    left_arm_stretched,
    right_arm_bent_90,
    left_arm_bent_90
)

POSTURES = [
    ("BRAÇ DRET ESTIRAT", right_arm_stretched),
    ("BRAÇ ESQUERRE ESTIRAT", left_arm_stretched),
    ("BRAÇ DRET DOBLAT 90°", right_arm_bent_90),
    ("BRAÇ ESQUERRE DOBLAT 90°", left_arm_bent_90),
]

def main():
    pose_cam = PoseCamera("pose_landmarker.task")

    state = 0
    posture_start_time = None
    last_second = None

    print("Presiona Ctrl+C per a eixir")
    print(f"Postura actual: {POSTURES[state][0]}")

    try:
        while True:
            frame, result = pose_cam.read()
            if frame is None:
                continue

            if result.pose_landmarks:
                landmarks = result.pose_landmarks[0]
                angles = get_all_angles(landmarks, frame.shape)

                posture_name, posture_fn = POSTURES[state]

                if posture_fn(angles):
                    now = time.time()

                    if posture_start_time is None:
                        posture_start_time = now
                        last_second = 10
                        print(f"\n{posture_name}")
                        print("Mantín la postura")

                    elapsed = int(now - posture_start_time)
                    remaining = 10 - elapsed

                    if remaining != last_second and remaining >= 0:
                        print(f"{remaining}...")
                        last_second = remaining

                    if remaining <= 0:
                        print(f"\n>>> {posture_name} COMPLETADA <<<\n")
                        state += 1
                        posture_start_time = None

                        if state >= len(POSTURES):
                            print("🎉 EXERCICI FINALITZAT 🎉")
                            break

                        print(f"Postura següent: {POSTURES[state][0]}")

                else:
                    posture_start_time = None
                    last_second = None

            cv2.imshow("Pose estimation", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Eixint...")

    finally:
        pose_cam.release()


if __name__ == "__main__":
    main()
