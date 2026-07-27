import time
import cv2
import numpy as np
from pose_camera import PoseCamera
from posture_estimation import compute_angle

# Índices de MediaPipe para tren superior e inferior
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


def inclinacion_tronco(landmarks, image_shape):
    """Calcula la inclinación del tronco respecto a la vertical"""
    h, w, _ = image_shape

    centro_hombros = np.array([
        (landmarks[HOMBRO_IZQ].x + landmarks[HOMBRO_DER].x) * w / 2,
        (landmarks[HOMBRO_IZQ].y + landmarks[HOMBRO_DER].y) * h / 2
    ])

    centro_caderas = np.array([
        (landmarks[CADERA_IZQ].x + landmarks[CADERA_DER].x) * w / 2,
        (landmarks[CADERA_IZQ].y + landmarks[CADERA_DER].y) * h / 2
    ])

    vector_vertical = np.array([0, -1])
    vector_tronco = centro_hombros - centro_caderas
    norma = np.linalg.norm(vector_tronco)
    if norma == 0:
        return 0.0
    vector_tronco = vector_tronco / norma

    angulo = np.degrees(
        np.arccos(np.clip(np.dot(vector_tronco, vector_vertical), -1.0, 1.0))
    )
    return angulo


def angulo_cuello(landmarks, image_shape):
    """Calcula el ángulo del cuello (hombros–cuello–cabeza)"""
    h, w, _ = image_shape

    centro_hombros = (
        (landmarks[HOMBRO_IZQ].x + landmarks[HOMBRO_DER].x) * w / 2,
        (landmarks[HOMBRO_IZQ].y + landmarks[HOMBRO_DER].y) * h / 2
    )

    nariz = (landmarks[NARIZ].x * w, landmarks[NARIZ].y * h)
    referencia_vertical = (centro_hombros[0], centro_hombros[1] - 100)

    return compute_angle(referencia_vertical, centro_hombros, nariz)


def apertura_piernas(landmarks, image_shape):
    """Calcula el ángulo de apertura entre ambas piernas tomando como vértice la cadera"""
    h, w, _ = image_shape
    
    cadera_izq = (landmarks[CADERA_IZQ].x * w, landmarks[CADERA_IZQ].y * h)
    cadera_der = (landmarks[CADERA_DER].x * w, landmarks[CADERA_DER].y * h)
    
    centro_caderas = ((cadera_izq[0] + cadera_der[0]) / 2, (cadera_izq[1] + cadera_der[1]) / 2)
    rodilla_izq = (landmarks[RODILLA_IZQ].x * w, landmarks[RODILLA_IZQ].y * h)
    rodilla_der = (landmarks[RODILLA_DER].x * w, landmarks[RODILLA_DER].y * h)
    
    return compute_angle(rodilla_izq, centro_caderas, rodilla_der)


def main():
    camara_pose = PoseCamera("pose_landmarker.task")
    ultimo_print = 0

    print("Visualizador avanzado de ángulos corporales (Tren Superior e Inferior)")
    print("Pulsa ESC para salir")

    try:
        while True:
            frame, resultado = camara_pose.read()
            if frame is None:
                continue

            tiempo_actual = time.time()

            if resultado.pose_landmarks:
                lm = resultado.pose_landmarks[0]
                h, w, _ = frame.shape

                angulos = {
                    "Hombro der.": compute_angle((lm[CODO_DER].x*w, lm[CODO_DER].y*h), (lm[HOMBRO_DER].x*w, lm[HOMBRO_DER].y*h), (lm[CADERA_DER].x*w, lm[CADERA_DER].y*h)),
                    "Codo der.": compute_angle((lm[HOMBRO_DER].x*w, lm[HOMBRO_DER].y*h), (lm[CODO_DER].x*w, lm[CODO_DER].y*h), (lm[MUÑECA_DER].x*w, lm[MUÑECA_DER].y*h)),
                    "Hombro izq.": compute_angle((lm[CODO_IZQ].x*w, lm[CODO_IZQ].y*h), (lm[HOMBRO_IZQ].x*w, lm[HOMBRO_IZQ].y*h), (lm[CADERA_IZQ].x*w, lm[CADERA_IZQ].y*h)),
                    "Codo izq.": compute_angle((lm[HOMBRO_IZQ].x*w, lm[HOMBRO_IZQ].y*h), (lm[CODO_IZQ].x*w, lm[CODO_IZQ].y*h), (lm[MUÑECA_IZQ].x*w, lm[MUÑECA_IZQ].y*h)),
                    "Cuello": angulo_cuello(lm, frame.shape),
                    "Tronco": inclinacion_tronco(lm, frame.shape),
                    "Cadera der.": compute_angle((lm[HOMBRO_DER].x*w, lm[HOMBRO_DER].y*h), (lm[CADERA_DER].x*w, lm[CADERA_DER].y*h), (lm[RODILLA_DER].x*w, lm[RODILLA_DER].y*h)),
                    "Rodilla der.": compute_angle((lm[CADERA_DER].x*w, lm[CADERA_DER].y*h), (lm[RODILLA_DER].x*w, lm[RODILLA_DER].y*h), (lm[TOBILLO_DER].x*w, lm[TOBILLO_DER].y*h)),
                    "Cadera izq.": compute_angle((lm[HOMBRO_IZQ].x*w, lm[HOMBRO_IZQ].y*h), (lm[CADERA_IZQ].x*w, lm[CADERA_IZQ].y*h), (lm[RODILLA_IZQ].x*w, lm[RODILLA_IZQ].y*h)),
                    "Rodilla izq.": compute_angle((lm[CADERA_IZQ].x*w, lm[CADERA_IZQ].y*h), (lm[RODILLA_IZQ].x*w, lm[RODILLA_IZQ].y*h), (lm[TOBILLO_IZQ].x*w, lm[TOBILLO_IZQ].y*h)),
                    "Apertura piernas": apertura_piernas(lm, frame.shape)
                }

                if tiempo_actual - ultimo_print >= 2:
                    print("\n--- ÁNGULOS ACTUALES ---")
                    for nombre, valor in angulos.items():
                        print(f"{nombre}: {valor:.1f}°")
                    ultimo_print = tiempo_actual

                y = 25
                i = 0
                for nombre, valor in angulos.items():
                    pos_x = 10 if i < 7 else 340
                    if i == 7:
                        y = 25
                        
                    cv2.putText(
                        frame,
                        f"{nombre}: {valor:.1f}°",
                        (pos_x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )
                    y += 22
                    i += 1

            cv2.imshow("Monitor Biomecanico Integral", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        camara_pose.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()