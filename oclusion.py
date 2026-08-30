import time
import cv2
from pose_camera import PoseCamera

# Índices de MediaPipe
NARIZ = 0
HOMBRO_IZQ = 11
HOMBRO_DER = 12
CODO_IZQ = 13
CODO_DER = 14
MUÑECA_IZQ = 15
MUÑECA_DER = 16
CADERA_IZQ = 23
CADERA_DER = 24
RODILLA_IZQ = 25
RODILLA_DER = 26
TOBILLO_IZQ = 27
TOBILLO_DER = 28
PIE_IZQ = 31      
PIE_DER = 32      

# Mapeo de puntos que queremos supervisar
PUNTOS_REQUERIDOS = {
    NARIZ: "Nariz / Cabeza",
    HOMBRO_IZQ: "Hombro Izquierdo",
    HOMBRO_DER: "Hombro Derecho",
    CODO_IZQ: "Codo Izquierdo",
    CODO_DER: "Codo Derecho",
    MUÑECA_IZQ: "Muñeca Izquierda",
    MUÑECA_DER: "Muñeca Derecha",
    CADERA_IZQ: "Cadera Izquierda",
    CADERA_DER: "Cadera Derecha",
    RODILLA_IZQ: "Rodilla Izquierda",
    RODILLA_DER: "Rodilla Derecha",
    TOBILLO_IZQ: "Tobillo Izquierdo",
    TOBILLO_DER: "Tobillo Derecho",
    PIE_IZQ: "Pie Izquierdo",
    PIE_DER: "Pie Derecho"
}

UMBRAL_VISIBILIDAD = 0.55


def verificar_puntos_faltantes(landmarks):
    """Comprueba si alguno de los puntos clave no es visible."""
    faltantes = []
    
    for idx, nombre in PUNTOS_REQUERIDOS.items():
        pt = landmarks[idx]
        
        # 1. Comprobar si las coordenadas están fuera de los márgenes de la imagen [0.0, 1.0]
        fuera_de_marco = pt.x < 0.0 or pt.x > 1.0 or pt.y < 0.0 or pt.y > 1.0
        
        # 2. Comprobar nivel de visibilidad
        visibilidad = getattr(pt, 'visibility', 1.0)
        baja_visibilidad = visibilidad < UMBRAL_VISIBILIDAD if visibilidad is not None else False
        
        if fuera_de_marco or baja_visibilidad:
            faltantes.append(nombre)
            
    return faltantes


def main():
    camara_pose = PoseCamera("pose_landmarker.task")
    ultimo_aviso = 0
    INTERVALO_AVISO = 1.0  # Imprime en terminal cada 1 segundo como máximo para evitar saturación

    print("Iniciando supervisión de puntos corporales...")
    print("Pulsa ESC en la ventana de vídeo para finalizar.\n")

    try:
        while True:
            frame, resultado = camara_pose.read()
            if frame is None:
                continue

            tiempo_actual = time.time()

            if resultado.pose_landmarks:
                lm = resultado.pose_landmarks[0]
                puntos_faltantes = verificar_puntos_faltantes(lm)

                if puntos_faltantes:
                    if tiempo_actual - ultimo_aviso >= INTERVALO_AVISO:
                        print(f"⚠️  [VISIÓN INCOMPLETA] Faltan {len(puntos_faltantes)} puntos por oclusión o encuadre:")
                        for pt in puntos_faltantes:
                            print(f"   • {pt}")
                        print("-" * 50)
                        ultimo_aviso = tiempo_actual
            else:
                if tiempo_actual - ultimo_aviso >= INTERVALO_AVISO:
                    print("⚠️  [VISIÓN INCOMPLETA] Cuerpo no detectado en cámara.")
                    print("-" * 50)
                    ultimo_aviso = tiempo_actual

            # Visualización básica de la cámara
            cv2.imshow("Cámara - Monitor de Puntos", frame)
            
            # Tecla ESC para salir
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        camara_pose.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()