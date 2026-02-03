# main.py
import time
import cv2
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_feedback import generate_feedback
from packs import exercise_packs
from app_gui import AppGUI

HOLD_TIME = 5  # segundos

# Variable global para almacenar el pack seleccionado desde la GUI
pack_seleccionado = None
pack_name_seleccionado = None

def obtener_pack_desde_gui():
    """Lanza la GUI y devuelve el pack seleccionado"""
    global pack_seleccionado, pack_name_seleccionado

    def on_pack_seleccionado(pack_name):
        global pack_seleccionado, pack_name_seleccionado
        pack_seleccionado = exercise_packs[pack_name]
        pack_name_seleccionado = pack_name
        app.root.quit()  # Cierra el loop de mainloop para continuar en main

    app = AppGUI()
    # Reemplazamos la función de selección de pack
    app.inicio.on_pack_seleccionado = on_pack_seleccionado
    app.run()  # Muestra la GUI hasta que el usuario selecciona un pack

def main():
    # Obtener pack desde la GUI
    obtener_pack_desde_gui()
    if pack_seleccionado is None:
        print("No se seleccionó ningún pack. Saliendo...")
        return

    print(f"\nHas seleccionado {pack_name_seleccionado}\n")

    pose_cam = PoseCamera("pose_landmarker.task")

    try:
        for idx, ejercicio in enumerate(pack_seleccionado, 1):
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
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

