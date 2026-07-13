import time
import cv2
import threading
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_feedback import generate_feedback
from packs import exercise_packs
from app_gui import AppGUI
from voice_engine import locutor  # Importamos el motor de voz diseñado
# --- NUEVAS IMPORTACIONES PARA MÉTRICAS Y BD ---
from calculo_error import MetricsEngine 
from database import guardar_sesion_completa

# Tiempo que se debe mantener la postura correcta
HOLD_TIME = 5

def bucle_ejercicios(app):
    """
    Controlador lógico principal con gestión de tiempos, persistencia y voz.
    """
    # 1. Instanciamos el motor de métricas
    engine = MetricsEngine()
    
    while True:
        # 1. Esperar a que el usuario confirme la selección en la GUI
        while not app.confirmado:
            time.sleep(0.1)
            if not app.root.winfo_exists():
                return

        # 2. Inicialización de recursos tras confirmación
        pack = exercise_packs[app.selected_pack]
        pose_cam = PoseCamera("pose_landmarker.task")
        
        # Reseteamos métricas al iniciar el pack
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
                frames_correctos_seguidos = 0

                while True:
                    frame, result = pose_cam.read()
                    if frame is None: continue
                    now = time.time()
                    tiempo_transcurrido = now - inicio_ejercicio

                    if result.pose_landmarks:
                        landmarks = result.pose_landmarks[0]
                        angles = get_all_angles(landmarks, frame.shape)
                        correct = ejercicio["funcion"](angles)

                        # --- INTEGRACIÓN DE MÉTRICAS ---
                        # Registramos valores en el motor en cada frame
                        engine.update('hombros', angles.get('right_shoulder', 0), 90)
                        engine.update('codos', angles.get('right_elbow', 0), 90)
                        engine.update('espalda', angles.get('back', 0), 0)
                        engine.update('cadera', angles.get('hip', 0), 0)
                        engine.update('rodillas', angles.get('knee', 0), 0)
                        engine.update('cuello', angles.get('neck', 0), 0)

                        if correct:
                            # --- LÓGICA DE POSTURA CORRECTA ---
                            error_detectado_desde = None # Reset cronómetro error
                            
                            if correcto_detectado_desde is None:
                                correcto_detectado_desde = now
                            
                            # REGLA: 1 segundo estable para confirmar éxito
                            if now - correcto_detectado_desde >= 1.0:
                                if hold_start is None: 
                                    hold_start = now
                                
                                segundos_restantes = HOLD_TIME - int(now - hold_start)
                                
                                # Si es la primera vez que detectamos éxito estable, avisamos por voz
                                if mensaje_actual != "¡POSTURA CORRECTA!":
                                    mensaje_actual = "¡POSTURA CORRECTA!"
                                    locutor.decir("¡Posición correcta!", es_exito=True)
                                
                                if segundos_restantes <= 0: break 
                        else:
                            # --- LÓGICA DE ERROR ---
                            correcto_detectado_desde = None # Reset cronómetro éxito
                            hold_start = None
                            segundos_restantes = HOLD_TIME
                            
                            # REGLA: Silencio inicial de 2 segundos (el usuario se está colocando)
                            if tiempo_transcurrido > 2.0:
                                
                                # REGLA: Persistencia (1.5s si venía de estar bien, 1.0s normal)
                                umbral_error = 1.5 if mensaje_actual == "¡POSTURA CORRECTA!" else 1.0
                                
                                if error_detectado_desde is None:
                                    error_detectado_desde = now
                                
                                if now - error_detectado_desde >= umbral_error:
                                    errores = generate_feedback(angles, idx)
                                    if errores:
                                        # Tomamos el error (generate_feedback ya prioriza)
                                        error_a_decir = errores[0].upper()
                                        
                                        # REGLA: No saturar la voz (mínimo 4s entre frases de error)
                                        if now - ultimo_mensaje_voz_hora > 4.0:
                                            locutor.decir(error_a_decir, es_exito=False)
                                            ultimo_mensaje_voz_hora = now
                                            # Actualizamos GUI con todos los errores detectados
                                            mensaje_actual = "\n\n".join(errores).upper()
                                    else:
                                        mensaje_actual = "AJUSTA TU POSICIÓN"

                        # Actualizar GUI de forma segura
                        app.root.after(0, lambda s=segundos_restantes, f=mensaje_actual: 
                                       app.actualizar_datos_tiempo_real(s, f))

                    cv2.imshow("Entrenamiento", frame)
                    if cv2.waitKey(1) & 0xFF == 27: # ESC
                        app.root.after(0, app.salir)
                        return

                # --- FIN DEL EJERCICIO ---
                locutor.decir("¡Muy bien! Siguiente ejercicio", es_exito=True)
                app.root.after(0, lambda: app.entrenamiento.actualizar_contador("✔"))
                time.sleep(2.0) # Pausa dramática para que el usuario descanse

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
    
    # Quitamos daemon=True para que Windows no cierre el hilo en silencio
    hilo_logica = threading.Thread(target=bucle_ejercicios, args=(app,))
    
    # Le damos 1 segundo de ventaja a la interfaz gráfica para que se estabilice en pantalla
    app.root.after(1000, hilo_logica.start)
    
    # Ejecutar la GUI
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR EN MAIN]: {e}")
        input("Presiona Enter para salir...")