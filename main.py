import time
import cv2
import threading
from pose_camera import PoseCamera
from posture_estimation import get_all_angles
from posture_feedback import generate_feedback
from packs import exercise_packs
from app_gui import AppGUI
from voice_engine import locutor
from calculo_error import MetricsEngine 
from database import guardar_sesion_completa
from robot_controller import RobotController

# Tiempo objetivo de mantenimiento postural
HOLD_TIME = 5

def bucle_ejercicios(app):
    """
    Controlador lógico principal: gestión de tiempos, análisis postural, 
    persistencia de datos, salida por voz y control del robot Dynamixel.
    """
    # Inicialización del motor de métricas y del robot
    engine = MetricsEngine()
    robot = RobotController()
    
    while True:
        # Espera de confirmación en GUI
        while not app.confirmado:
            time.sleep(0.1)
            if not app.root.winfo_exists():
                return

        # Carga de recursos y cámara tras confirmación
        pack = exercise_packs[app.selected_pack]
        pose_cam = PoseCamera("pose_landmarker.task")
        
        # Reinicio de métricas por sesión
        engine.reset()
        
        # Conexión al bus serie del robot y activación de torque
        robot.conectar()
        
        try:
            for idx, ejercicio in enumerate(pack):
                # Notificación a GUI
                app.root.after(0, lambda i=idx, n=ejercicio["nombre"]: 
                               app.actualizar_interfaz_ejercicio(i, n, len(pack)))

                # Posicionamiento físico del robot Dynamixel
                robot.mover_pose(idx, tiempo_espera=0.5)

                # Variables de estado del ejercicio
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

                        # Análisis kinemático
                        if correct:
                            # Validación postural
                            error_detectado_desde = None # Reset tiempo de error
                            
                            if correcto_detectado_desde is None:
                                correcto_detectado_desde = now
                            
                            # Estabilidad temporal requerida (1.0s)
                            if now - correcto_detectado_desde >= 1.0:
                                if hold_start is None: 
                                    hold_start = now
                                
                                segundos_restantes = HOLD_TIME - int(now - hold_start)
                                
                                # Feedback auditivo de éxito
                                if mensaje_actual != "¡POSTURA CORRECTA!":
                                    mensaje_actual = "¡POSTURA CORRECTA!"
                                    locutor.decir("¡Posición correcta!", es_exito=True)
                                
                                if segundos_restantes <= 0: break 
                        else:
                            # Tratamiento de desviaciones
                            correcto_detectado_desde = None # Reset tiempo de éxito
                            hold_start = None
                            segundos_restantes = HOLD_TIME
                            
                            # Tolerancia inicial de posicionamiento
                            if tiempo_transcurrido > 2.0:
                                
                                # Histéresis de error
                                umbral_error = 1.5 if mensaje_actual == "¡POSTURA CORRECTA!" else 1.0
                                
                                if error_detectado_desde is None:
                                    error_detectado_desde = now
                                
                                if now - error_detectado_desde >= umbral_error:
                                    # Diagnóstico de fallos
                                    errores = generate_feedback(angles, idx, engine)
                                    if errores:
                                        # Priorización de error
                                        error_a_decir = errores[0].upper()
                                        
                                        # Frecuencia máxima de voz
                                        if now - ultimo_mensaje_voz_hora > 4.0:
                                            locutor.decir(error_a_decir, es_exito=False)
                                            ultimo_mensaje_voz_hora = now
                                            # Actualización de GUI
                                            mensaje_actual = "\n\n".join(errores).upper()
                                    else:
                                        mensaje_actual = "AJUSTA TU POSICIÓN"

                        # Sincronización con GUI
                        app.root.after(0, lambda s=segundos_restantes, f=mensaje_actual: 
                                       app.actualizar_datos_tiempo_real(s, f))

                    cv2.imshow("Entrenamiento", frame)
                    if cv2.waitKey(1) & 0xFF == 27: # Salida por teclado
                        app.root.after(0, app.salir)
                        return

                # Transición entre ejercicios
                locutor.decir("¡Muy bien! Siguiente ejercicio", es_exito=True)
                app.root.after(0, lambda: app.entrenamiento.actualizar_contador("✔"))
                
                # Reposicionamiento del robot a posición neutra durante el descanso
                robot.ir_a_neutro()
                time.sleep(2.0) # Intervalo de descanso

            # Registro persistente de sesión
            usuario_id = getattr(app, 'usuario_actual', 1)
            guardar_sesion_completa(usuario_id, app.selected_pack, engine.magnitudes)
            
            # Cierre de conexión con el robot
            robot.desconectar()
            
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
            robot.desconectar()
            if 'pose_cam' in locals():
                pose_cam.release()
            cv2.destroyAllWindows()

def main():
    app = AppGUI()
    
    # Gestión del hilo secundario
    hilo_logica = threading.Thread(target=bucle_ejercicios, args=(app,))
    
    # Retardo de estabilización
    app.root.after(1000, hilo_logica.start)
    
    # Bucle principal de eventos GUI
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR EN MAIN]: {e}")
        input("Presiona Enter para salir...")