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
from posture_feedback import generate_feedback

HOLD_TIME = 5  # segundos

def main():
    pose_cam = PoseCamera("pose_landmarker.task")

    state = 0  # 0 = brazos estirados, 1 = brazos doblados 90°
    hold_start = None
    last_feedback_time = 0
    feedback_interval = 1  # 1 segundo

    print("Presiona Ctrl+C para salir")
    print("FASE 1 → ESTIRA LOS DOS BRAZOS")

    try:
        while True:
            frame, result = pose_cam.read()
            if frame is None:
                continue

            now = time.time()

            if result.pose_landmarks:
                landmarks = result.pose_landmarks[0]
                angles = get_all_angles(landmarks, frame.shape)

                # Evaluar la postura correcta según la fase
                if state == 0:
                    correct = right_arm_stretched(angles) and left_arm_stretched(angles)
                else:
                    correct = right_arm_bent_90(angles) and left_arm_bent_90(angles)

                # Control del tiempo de mantener la postura
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

                # Mostrar feedback cada 1 segundo
                if now - last_feedback_time >= feedback_interval:
                    feedbacks = generate_feedback(angles, state)
                    print(" | ".join(feedbacks))
                    last_feedback_time = now

            cv2.imshow("Pose estimation", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
                break

    except KeyboardInterrupt:
        print("Saliendo...")

    finally:
        pose_cam.release()


if __name__ == "__main__":
    main()
