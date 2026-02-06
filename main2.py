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
        # Aquí NO cerramos la GUI, solo permitimos continuar
        app.root.quit()  # Esto hace que main continúe

    app = AppGUI()
    # Conectamos el callback
    app.inicio.on_pack_seleccionado = on_pack_seleccionado
    # Mostramos la GUI hasta que se seleccione un pack
    app.run()

    return app

def main():
    # 1️⃣ Mostrar la GUI y obtener el pack
    app = obtener_pack_desde_gui()

    if pack_seleccionado is None:
        print("No se seleccionó ningún pack. Saliendo...")
        return

    print(f"\nHas seleccionado {pack_name_seleccionado}\n")

    # 2️⃣ Inicializar la cámara
    pose_cam = PoseCamera("pose_landmarker.task")

    try:
        # 3️⃣ Bucle de ejercicios
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

                    if correct:
                        if hold_start is None:
                            hold_start = now

                        remaining = HOLD_TIME - int(now - hold_start)
                        if last_display_second != remaining:
                            print(f"Mantén la postura ({remaining}s)")
                            last_display_second = remaining

                        if now - hold_start >= HOLD_TIME:
                            print(f"\n✔ EJERCICIO {idx} COMPLETADO\n")
                            break
                    else:
                        hold_start = None
                        last_display_second = None

                    if now - last_feedback_time >= 1:
                        feedbacks = generate_feedback(angles, idx-1)
                        print(" | ".join(feedbacks))
                        last_feedback_time = now

                # Mostrar la cámara
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