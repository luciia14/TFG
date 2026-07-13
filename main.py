import time
import cv2
import threading
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_feedback import generate_feedback
from packs import exercise_packs
from app_gui import AppGUI
from voice_engine import locutor
# Importaciones necesarias para las nuevas funciones
from calculo_error import MetricsEngine 
from database import guardar_sesion_completa

# Tiempo que se debe mantener la postura correcta
HOLD_TIME = 5

def bucle_ejercicios(app):
    """
    Controlador lógico principal con gestión de tiempos, persistencia, voz y métricas.
    """
    # 1. Instanciamos el motor de métricas
    engine = MetricsEngine()
    
    while True:
        # Esperar a que el usuario confirme la selección en la GUI
        while not app.confirmado:
            time.sleep(0.1)
            if not app.root.winfo_exists():
                return

        # 2. Inicialización de recursos tras confirmación
        pack = exercise_packs[app.selected_pack]
        pose_cam = PoseCamera("pose_landmarker.task")
        
        # Reseteamos métricas al iniciar un pack nuevo
        engine.reset()
        
        try:
            for idx, ejercicio in enumerate(pack):
                # Notificar inicio de ejercicio a la interfaz
                app.root.after(0, lambda i=idx, n=ejercicio["nombre"]: 
                                app.actualizar_interfaz_ejercicio(i, n, len(pack)))

                # --- VARIABLES DE ESTADO POR EJERCICIO ---
                inicio_ejercicio = time.time()
                error_detectado_desde = None
                correcto_detectado_desde = None
                ultimo_mensaje_voz_hora = 0
                mensaje_actual = "¡PREPÁRATE!"
                hold_start = None
                segundos_restantes = HOLD_TIME

                while True:
                    frame, result = pose_cam.read()
                    if frame is None: continue
                    now = time.time()
                    tiempo_transcurrido = now - inicio_ejercicio

                    if result.pose_landmarks:
                        landmarks = result.pose_landmarks[0]
                        angles = get_all_angles(landmarks, frame.shape)
                        correct = ejercicio["funcion"](angles)

                        # --- INTEGRACIÓN DE MÉTRICAS (Añadido) ---
                        # Registramos el error de las articulaciones clave
                        engine.update('hombros', angles.get('right_shoulder', 90), 90)
                        engine.update('codos', angles.get('right_elbow', 90), 90)

                        if correct:
                            # --- LÓGICA DE POSTURA CORRECTA ---
                            error_detectado_desde = None 
                            if correcto_detectado_desde is None: correcto_detectado_desde = now
                            
                            if now - correcto_detectado_desde >= 1.0:
                                if hold_start is None: hold_start = now
                                segundos_restantes = HOLD_TIME - int(now - hold_start)
                                if mensaje_actual != "¡POSTURA CORRECTA!":
                                    mensaje_actual = "¡POSTURA CORRECTA!"
                                    locutor.decir("¡Posición correcta!", es_exito=True)
                                if segundos_restantes <= 0: break 
                        else:
                            # --- LÓGICA DE ERROR ---
                            correcto_detectado_desde = None
                            hold_start = None
                            segundos_restantes = HOLD_TIME
                            
                            if tiempo_transcurrido > 2.0:
                                umbral_error = 1.5 if mensaje_actual == "¡POSTURA CORRECTA!" else 1.0
                                if error_detectado_desde is None: error_detectado_desde = now
                                
                                if now - error_detectado_desde >= umbral_error:
                                    errores = generate_feedback(angles, idx)
                                    if errores:
                                        error_a_decir = errores[0].upper()
                                        if now - ultimo_mensaje_voz_hora > 4.0:
                                            locutor.decir(error_a_decir, es_exito=False)
                                            ultimo_mensaje_voz_hora = now
                                            mensaje_actual = "\n\n".join(errores).upper()
                                    else:
                                        mensaje_actual = "AJUSTA TU POSICIÓN"

                        app.root.after(0, lambda s=segundos_restantes, f=mensaje_actual: 
                                       app.actualizar_datos_tiempo_real(s, f))

                    cv2.imshow("Entrenamiento", frame)
                    if cv2.waitKey(1) & 0xFF == 27: # ESC
                        app.root.after(0, app.salir)
                        return

                locutor.decir("¡Muy bien! Siguiente ejercicio", es_exito=True)
                app.root.after(0, lambda: app.entrenamiento.actualizar_contador("✔"))
                time.sleep(2.0)

            # --- FIN DEL PACK: PERSISTENCIA ---
            usuario_id = getattr(app, 'usuario_actual', 1)
            guardar_sesion_completa(usuario_id, app.selected_pack, engine.magnitudes)
            
            print("\n--- Entrenamiento Finalizado y datos guardados ---")
            app.root.after(0, app.finalizar_entrenamiento_gui)
            pose_cam.release()
            cv2.destroyAllWindows()
            
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
    app = AppGUI()
    hilo_logica = threading.Thread(target=bucle_ejercicios, args=(app,))
    app.root.after(1000, hilo_logica.start)
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR EN MAIN]: {e}")
        input("Presiona Enter para salir...")