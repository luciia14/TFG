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
        # 1. Esperar a que el usuario SELECCIONE y CONFIRME un pack en la GUI
        while not app.confirmado:
            time.sleep(0.1)
            if not app.root.winfo_exists():
                return

        # 2. Inicializar cámara solo tras la confirmación
        print(f"\n--- INICIANDO PACK: {app.selected_pack} ---")
        pack = exercise_packs[app.selected_pack]
        pose_cam = PoseCamera("pose_landmarker.task")
        
        # Variable para mantener el mensaje estable y evitar parpadeos
        mensaje_para_gui = "Iniciando análisis..."

        try:
            for idx, ejercicio in enumerate(pack):
                print(f"\nEJERCICIO {idx + 1}: {ejercicio['nombre']}")
                
                app.root.after(0, lambda i=idx, n=ejercicio["nombre"]: 
                               app.actualizar_interfaz_ejercicio(i, n, len(pack)))

                hold_start = None
                last_feedback_time = 0
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
                            duracion = int(now - hold_start)
                            segundos_restantes = HOLD_TIME - duracion
                            
                            # Actualizamos el mensaje de éxito
                            mensaje_para_gui = "¡Postura Correcta! Mantén la posición."
                            
                            if segundos_restantes <= 0:
                                print(f"✔ {ejercicio['nombre']} completado.")
                                break 
                        else:
                            hold_start = None
                            segundos_restantes = HOLD_TIME
                            
                            # Generar feedback solo cada 0.5 segundos para estabilidad visual
                            if now - last_feedback_time >= 0.5:
                                mensajes = generate_feedback(angles, idx)
                                if mensajes:
                                    mensaje_para_gui = " | ".join(mensajes)
                                else:
                                    mensaje_para_gui = "Ajusta tu posición"
                                
                                print(f"REPORTE: {mensaje_para_gui} (Restante: {segundos_restantes}s)")
                                last_feedback_time = now

                        # ENVIAMOS EL MENSAJE ACTUAL (Sin resetearlo a "Analizando..." cada frame)
                        app.root.after(0, lambda s=segundos_restantes, f=mensaje_para_gui: 
                                       app.actualizar_datos_tiempo_real(s, f))

                    cv2.imshow("Camara de Entrenamiento", frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        app.root.after(0, app.salir)
                        return

                app.root.after(0, lambda: app.entrenamiento.actualizar_contador("✔"))
                time.sleep(1)
                # Resetear mensaje para el siguiente ejercicio
                mensaje_para_gui = "Preparando siguiente ejercicio..."

            print("\n--- TODO EL PACK HA SIDO COMPLETADO ---")
            app.root.after(0, app.finalizar_entrenamiento_gui)
            
            pose_cam.release()
            cv2.destroyAllWindows()
            
            while app.confirmado:
                time.sleep(0.5)
                if not app.root.winfo_exists(): return

        except Exception as e:
            print(f"Error crítico en el bucle de cámara: {e}")
            break
        finally:
            if 'pose_cam' in locals():
                pose_cam.release()
            cv2.destroyAllWindows()

def main():
    app = AppGUI()
    hilo_logica = threading.Thread(target=bucle_ejercicios, args=(app,), daemon=True)
    hilo_logica.start()
    app.run()

if __name__ == "__main__":
    main()