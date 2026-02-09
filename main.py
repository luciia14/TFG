import time
import cv2
import threading
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_feedback import generate_feedback
from packs import exercise_packs
from app_gui import AppGUI

HOLD_TIME = 5

def bucle_ejercicios(app):
    """
    Controlador lógico: Maneja la cámara y envía actualizaciones a la GUI y terminal.
    """
    while True:
        # 1. Esperar a que el usuario confirme en la GUI
        while not app.confirmado:
            time.sleep(0.1)
            if not app.root.winfo_exists(): return

        # 2. Inicialización de recursos
        pack = exercise_packs[app.selected_pack]
        pose_cam = PoseCamera("pose_landmarker.task")
        
        # Variables de estabilidad para la visualización
        mensaje_actual = "¡PREPÁRATE!"
        last_feedback_time = 0
        TIEMPO_MINIMO_MENSAJE = 1.2  # Segundos que un mensaje de error se queda fijo

        try:
            for idx, ejercicio in enumerate(pack):
                # Notificar inicio de ejercicio a la GUI
                app.root.after(0, lambda i=idx, n=ejercicio["nombre"]: 
                               app.actualizar_interfaz_ejercicio(i, n, len(pack)))

                hold_start = None
                segundos_restantes = HOLD_TIME

                while True:
                    frame, result = pose_cam.read()
                    if frame is None: continue
                    now = time.time()

                    if result.pose_landmarks:
                        landmarks = result.pose_landmarks[0]
                        angles = get_all_angles(landmarks, frame.shape)
                        correct = ejercicio["funcion"](angles)

                        if correct:
                            if hold_start is None: hold_start = now
                            segundos_restantes = HOLD_TIME - int(now - hold_start)
                            
                            # Si es correcto, el mensaje cambia a éxito inmediatamente
                            mensaje_actual = "¡POSTURA CORRECTA!\nMANTÉN LA POSICIÓN"
                            
                            if segundos_restantes <= 0: break 
                        else:
                            hold_start = None
                            segundos_restantes = HOLD_TIME
                            
                            # Control de estabilidad para no agobiar al usuario con cambios rápidos
                            if now - last_feedback_time >= TIEMPO_MINIMO_MENSAJE:
                                errores = generate_feedback(angles, idx)
                                if errores:
                                    # --- CAMBIO CLAVE: Unimos con \n para saltos de línea ---
                                    nuevo_feedback = "\n".join(errores).upper()
                                    
                                    if nuevo_feedback != mensaje_actual:
                                        mensaje_actual = nuevo_feedback
                                        last_feedback_time = now
                                        print(f"TERMINAL:\n{mensaje_actual}")
                                else:
                                    mensaje_actual = "AJUSTA TU POSICIÓN"

                        # Actualizar la GUI
                        app.root.after(0, lambda s=segundos_restantes, f=mensaje_actual: 
                                       app.actualizar_datos_tiempo_real(s, f))

                    cv2.imshow("Camara de Entrenamiento", frame)
                    if cv2.waitKey(1) & 0xFF == 27: # ESC para salir
                        app.root.after(0, app.salir)
                        return

                # Pausa entre ejercicios
                app.root.after(0, lambda: app.entrenamiento.actualizar_contador("✔"))
                time.sleep(1.5)
                mensaje_actual = "¡SIGUIENTE EJERCICIO!"

            # Finalización
            app.root.after(0, app.finalizar_entrenamiento_gui)
            pose_cam.release()
            cv2.destroyAllWindows()
            
            # Esperar a que se reinicie el flujo desde la GUI
            while app.confirmado:
                time.sleep(0.5)
                if not app.root.winfo_exists(): return

        except Exception as e:
            print(f"Error en el bucle: {e}")
            break
        finally:
            if 'pose_cam' in locals(): pose_cam.release()
            cv2.destroyAllWindows()

def main():
    app = AppGUI()
    # Ejecutamos la lógica en un hilo separado para no bloquear la ventana
    hilo_logica = threading.Thread(target=bucle_ejercicios, args=(app,), daemon=True)
    hilo_logica.start()
    app.run()

if __name__ == "__main__":
    main()