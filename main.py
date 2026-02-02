# main.py
import time
import cv2
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_feedback import generate_feedback
from packs import exercise_packs

HOLD_TIME = 5  # segundos

def seleccionar_pack():
    print("Selecciona un pack de ejercicios:")
    for i, pack_name in enumerate(exercise_packs.keys(), 1):
        print(f"{i}. {pack_name}")
    while True:
        opcion = input("Introduce el número del pack: ")
        if opcion in ["1", "2"]:
            pack_name = list(exercise_packs.keys())[int(opcion)-1]
            return exercise_packs[pack_name], pack_name
        else:
            print("Opción no válida, inténtalo de nuevo.")

def main():
    # Selección del pack
    pack, pack_name = seleccionar_pack()
    print(f"\nHas seleccionado {pack_name}\n")

    pose_cam = PoseCamera("pose_landmarker.task")

    try:
        for idx, ejercicio in enumerate(pack, 1):
            print(f"EMPEZANDO EJERCICIO {idx} → {ejercicio['nombre']}")
            hold_start = None
            last_feedback_time = 0
            last_display_second = None

            while True:
                frame, result = pose_cam.read()
                if frame is None:
                    continue

                now = time.time()

                if result.pose_landmarks:
                    landmarks = result.pose_landmarks[0]
                    angles = get_all_angles(landmarks, frame.shape)

                    # Comprobar postura
                    correct = ejercicio["funcion"](angles)

                    # Control del tiempo de mantener la postura
                    if correct:
                        if hold_start is None:
                            hold_start = now

                        remaining = HOLD_TIME - int(now - hold_start)
                        # Mostrar solo cuando cambie el segundo
                        if last_display_second != remaining:
                            print(f"Mantén la postura ({remaining}s)")
                            last_display_second = remaining

                        if now - hold_start >= HOLD_TIME:
                            print(f"\n✔ EJERCICIO {idx} COMPLETADO\n")
                            break
                    else:
                        hold_start = None
                        last_display_second = None

                    # Feedback cada segundo
                    if now - last_feedback_time >= 1:
                        feedbacks = generate_feedback(angles, idx-1)  # idx-1 como estado
                        print(" | ".join(feedbacks))
                        last_feedback_time = now

                cv2.imshow("Pose estimation", frame)
                if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
                    raise KeyboardInterrupt

        print("🎉 TODOS LOS EJERCICIOS DEL PACK COMPLETADOS 🎉")

    except KeyboardInterrupt:
        print("\nSaliendo...")

    finally:
        pose_cam.release()


if __name__ == "__main__":
    main()
