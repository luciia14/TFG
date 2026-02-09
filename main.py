import time
import cv2
import threading
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_feedback import generate_feedback
from packs import exercise_packs
from app_gui import AppGUI

# Tiempo que se debe mantener la postura correcta
HOLD_TIME = 5

def bucle_ejercicios(app):
    """
    Controlador lógico: Maneja la cámara y envía actualizaciones estables a la GUI.
    """
    while True:
        # 1. Esperar a que el usuario confirme la selección en la GUI
        while not app.confirmado:
            time.sleep(0.1)
            if not app.root.winfo_exists():
                return

        # 2. Inicialización de recursos tras confirmación
        pack = exercise_packs[app.selected_pack]
        pose_cam = PoseCamera("pose_landmarker.task")
        
        # Variables para estabilidad y permanencia de mensajes
        mensaje_actual = "¡PREPÁRATE!"
        last_feedback_time = 0
        TIEMPO_PERSISTENCIA_ERROR = 2.5  # Los errores se quedan 2.5 seg para lectura clara
        frames_correctos_seguidos = 0    # Filtro para evitar saltos rápidos al "Correcto"

        try:
            for idx, ejercicio in enumerate(pack):
                # Notificar inicio de ejercicio a la interfaz
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
                            # Filtro de estabilidad: necesitamos ~10 frames buenos para confirmar
                            frames_correctos_seguidos += 1
                            
                            if frames_correctos_seguidos > 10:
                                if hold_start is None: 
                                    hold_start = now
                                
                                segundos_restantes = HOLD_TIME - int(now - hold_start)
                                mensaje_actual = "¡POSTURA CORRECTA!\nMANTÉN LA POSICIÓN"
                                
                                if segundos_restantes <= 0: 
                                    print(f"✔ Ejercicio {idx+1} completado")
                                    break 
                        else:
                            # Si falla la postura, reseteamos contadores
                            frames_correctos_seguidos = 0
                            hold_start = None
                            segundos_restantes = HOLD_TIME
                            
                            # Solo actualizamos el mensaje de error si ha pasado el tiempo de lectura
                            if now - last_feedback_time >= TIEMPO_PERSISTENCIA_ERROR:
                                errores = generate_feedback(angles, idx)
                                if errores:
                                    # Unimos errores con doble salto de línea para mayor claridad visual
                                    nuevo_feedback = "\n\n".join(errores).upper()
                                    
                                    if nuevo_feedback != mensaje_actual:
                                        mensaje_actual = nuevo_feedback
                                        last_feedback_time = now
                                        print(f"LOG ERROR:\n{mensaje_actual}")
                                else:
                                    mensaje_actual = "AJUSTA TU POSICIÓN"

                        # Enviar datos a la GUI de forma segura entre hilos
                        app.root.after(0, lambda s=segundos_restantes, f=mensaje_actual: 
                                       app.actualizar_datos_tiempo_real(s, f))

                    cv2.imshow("Camara de Entrenamiento", frame)
                    if cv2.waitKey(1) & 0xFF == 27: # Salir con ESC
                        app.root.after(0, app.salir)
                        return

                # Feedback visual de fin de ejercicio
                app.root.after(0, lambda: app.entrenamiento.actualizar_contador("✔"))
                time.sleep(1.5)
                mensaje_actual = "¡BIEN HECHO!\nSIGUIENTE EJERCICIO..."
                frames_correctos_seguidos = 0

            # 3. Pack finalizado
            print("\n--- Entrenamiento Finalizado ---")
            app.root.after(0, app.finalizar_entrenamiento_gui)
            pose_cam.release()
            cv2.destroyAllWindows()
            
            # Quedarse en espera hasta que el usuario decida volver al menú o reiniciar
            while app.confirmado:
                time.sleep(0.5)
                if not app.root.winfo_exists(): return

        except Exception as e:
            print(f"Error crítico: {e}")
            break
        finally:
            if 'pose_cam' in locals():
                pose_cam.release()
            cv2.destroyAllWindows()

def main():
    # Instanciar la aplicación
    app = AppGUI()

    # Lanzar la lógica de visión en un hilo "daemon" para que cierre con la app
    hilo_logica = threading.Thread(target=bucle_ejercicios, args=(app,), daemon=True)
    hilo_logica.start()

    # Iniciar el bucle principal de la GUI (Bloqueante)
    app.run()

if __name__ == "__main__":
    main()