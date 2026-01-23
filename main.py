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

HOLD_TIME = 5  # segundos

def main():
    pose_cam = PoseCamera("pose_landmarker.task")

    state = 0  # 0 = estirados, 1 = doblados
    hold_start = None

    print("Presiona Ctrl+C para salir")
    print("FASE 1 → ESTIRA LOS DOS BRAZOS")

    try:
        while True:
            frame, result = pose_cam.read()
            if frame is None:
                continue

            if result.pose_landmarks:
                landmarks = result.pose_landmarks[0]
                angles = get_all_angles(landmarks, frame.shape)
                now = time.time()

                if state == 0:
                    correct = (
                        right_arm_stretched(angles) and
                        left_arm_stretched(angles)
                    )

                elif state == 1:
                    correct = (
                        right_arm_bent_90(angles) and
                        left_arm_bent_90(angles)
                    )

                if correct:
                    if hold_start is None:
                        hold_start = now

                    remaining = HOLD_TIME - int(now - hold_start)
                    print(f"Mantén la postura ({remaining}s)")

                    if now - hold_start >= HOLD_TIME:
                        if state == 0:
                            state = 1
                            print("\n✔ FASE 1 COMPLETADA")
                            print("FASE 2 → DOBLA LOS DOS BRAZOS A 90°\n")
                        else:
                            print("\n🎉 POSICIÓN COMPLETA REALIZADA 🎉")
                            break

                        hold_start = None
                else:
                    hold_start = None

            cv2.imshow("Pose estimation", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Saliendo...")

    finally:
        pose_cam.release()

if __name__ == "__main__":
    main()
