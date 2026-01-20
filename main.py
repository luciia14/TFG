# main.py
import time
import cv2
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_definitions import right_arm_stretched, left_arm_stretched

RIGHT_ARM = 0
LEFT_ARM = 1

def main():
    pose_cam = PoseCamera("pose_landmarker.task")

    state = RIGHT_ARM
    posture_start_time = None

    print("Presiona Ctrl+C para salir")
    print("Estado inicial: BRAZO DERECHO")

    try:
        while True:
            frame, result = pose_cam.read()
            if frame is None:
                continue

            if result.pose_landmarks:
                landmarks = result.pose_landmarks[0]
                angles = get_all_angles(landmarks, frame.shape)

                current_time = time.time()

                # =========================
                # ESTADO BRAZO DERECHO
                # =========================
                if state == RIGHT_ARM:
                    if right_arm_stretched(angles):
                        if posture_start_time is None:
                            posture_start_time = current_time
                            print("Brazo derecho correcto, empezando contador...")

                        elapsed = current_time - posture_start_time
                        print(f"Brazo derecho correcto: {elapsed:.1f}s")

                        if elapsed >= 10:
                            print("\n>>> BRAZO DERECHO COMPLETADO <<<")
                            print("Cambia a BRAZO IZQUIERDO\n")
                            state = LEFT_ARM
                            posture_start_time = None
                    else:
                        posture_start_time = None

                # =========================
                # ESTADO BRAZO IZQUIERDO
                # =========================
                elif state == LEFT_ARM:
                    if left_arm_stretched(angles):
                        if posture_start_time is None:
                            posture_start_time = current_time
                            print("Brazo izquierdo correcto, empezando contador...")

                        elapsed = current_time - posture_start_time
                        print(f"Brazo izquierdo correcto: {elapsed:.1f}s")

                        if elapsed >= 10:
                            print("\n>>> BRAZO IZQUIERDO COMPLETADO <<<")
                            print("EJERCICIO FINALIZADO")
                            break
                    else:
                        posture_start_time = None

            cv2.imshow("Pose estimation", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Saliendo...")

    finally:
        pose_cam.release()


if __name__ == "__main__":
    main()
