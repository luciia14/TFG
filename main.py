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
            if not app.root.winfo_exists(): # Si cierran la ventana, matamos el hilo
                return

        # 2. Inicializar cámara solo tras la confirmación
        print(f"\n--- INICIANDO PACK: {app.selected_pack} ---")
        pack = exercise_packs[app.selected_pack]
        pose_cam = PoseCamera("pose_landmarker.task")

        try:
            for idx, ejercicio in enumerate(pack):
                print(f"\nEJERCICIO {idx + 1}: {ejercicio['nombre']}")
                
                # Notificar a la GUI el inicio del ejercicio
                app.root.after(0, lambda i=idx, n=ejercicio["nombre"]: 
                               app.actualizar_interfaz_ejercicio(i, n, len(pack)))

                hold_start = None
                last_feedback_time = 0
                segundos_restantes = HOLD_TIME

                while True:
                    frame, result = pose_cam.read()
                    if frame is None: continue

                    now = time.time()
                    feedback_actual = "Analizando postura..."

                    if result.pose_landmarks:
                        landmarks = result.pose_landmarks[0]
                        angles = get_all_angles(landmarks, frame.shape)
                        correct = ejercicio["funcion"](angles)

                        if correct:
                            if hold_start is None: hold_start = now
                            duracion = int(now - hold_start)
                            segundos_restantes = HOLD_TIME - duracion
                            feedback_actual = "¡Postura Correcta! Mantén la posición."
                            
                            if segundos_restantes <= 0:
                                print(f"✔ {ejercicio['nombre']} completado.")
                                break # Salta al siguiente ejercicio
                        else:
                            hold_start = None
                            segundos_restantes = HOLD_TIME
                            
                            # Generar feedback de errores
                            if now - last_feedback_time >= 0.5:
                                mensajes = generate_feedback(angles, idx)
                                feedback_actual = " | ".join(mensajes) if mensajes else "Ajusta tu posición"
                                
                                # MOSTRAR POR TERMINAL
                                print(f"REPORTE: {feedback_actual} (Restante: {segundos_restantes}s)")
                                
                                last_feedback_time = now

                        # ACTUALIZAR GUI (Seguro entre hilos)
                        app.root.after(0, lambda s=segundos_restantes, f=feedback_actual: 
                                       app.actualizar_datos_tiempo_real(s, f))

                    cv2.imshow("Camara de Entrenamiento", frame)
                    if cv2.waitKey(1) & 0xFF == 27: # ESC para salir
                        app.root.after(0, app.salir)
                        return

                # Pequeña pausa visual al terminar cada ejercicio
                app.root.after(0, lambda: app.entrenamiento.actualizar_contador("✔"))
                time.sleep(1)

            # 3. Finalización del pack completo
            print("\n--- TODO EL PACK HA SIDO COMPLETADO ---")
            app.root.after(0, app.finalizar_entrenamiento_gui)
            
            # Liberar cámara y recursos
            pose_cam.release()
            cv2.destroyAllWindows()
            
            # Esperar a que el usuario decida en la GUI (Reiniciar pone app.confirmado en False)
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
    # Iniciar la aplicación
    app = AppGUI()

    # Hilo de lógica (Daemon)
    hilo_logica = threading.Thread(target=bucle_ejercicios, args=(app,), daemon=True)
    hilo_logica.start()

    # Ejecutar loop de Tkinter
    app.run()

if __name__ == "__main__":
    main()