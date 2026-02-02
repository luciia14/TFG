import time
import cv2
import numpy as np
from pose_camera import PoseCamera
from posture_estimation import compute_angle

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
    vector_tronco = vector_tronco / np.linalg.norm(vector_tronco)

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


def main():
    camara_pose = PoseCamera("pose_landmarker.task")
    ultimo_print = 0

    print("Visualizador de ángulos corporales")
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
                    "Hombro derecho": compute_angle(
                        (lm[CODO_DER].x*w, lm[CODO_DER].y*h),
                        (lm[HOMBRO_DER].x*w, lm[HOMBRO_DER].y*h),
                        (lm[CADERA_DER].x*w, lm[CADERA_DER].y*h)
                    ),
                    "Codo derecho": compute_angle(
                        (lm[HOMBRO_DER].x*w, lm[HOMBRO_DER].y*h),
                        (lm[CODO_DER].x*w, lm[CODO_DER].y*h),
                        (lm[MUÑECA_DER].x*w, lm[MUÑECA_DER].y*h)
                    ),
                    "Hombro izquierdo": compute_angle(
                        (lm[CODO_IZQ].x*w, lm[CODO_IZQ].y*h),
                        (lm[HOMBRO_IZQ].x*w, lm[HOMBRO_IZQ].y*h),
                        (lm[CADERA_IZQ].x*w, lm[CADERA_IZQ].y*h)
                    ),
                    "Codo izquierdo": compute_angle(
                        (lm[HOMBRO_IZQ].x*w, lm[HOMBRO_IZQ].y*h),
                        (lm[CODO_IZQ].x*w, lm[CODO_IZQ].y*h),
                        (lm[MUÑECA_IZQ].x*w, lm[MUÑECA_IZQ].y*h)
                    ),
                    "Cuello": angulo_cuello(lm, frame.shape),
                    "Inclinación del tronco": inclinacion_tronco(lm, frame.shape)
                }

                # Mostrar por terminal cada 2 segundos
                if tiempo_actual - ultimo_print >= 2:
                    print("\nÁNGULOS ACTUALES:")
                    for nombre, valor in angulos.items():
                        print(f"{nombre}: {valor:.1f}°")
                    ultimo_print = tiempo_actual

                # Mostrar en pantalla en tiempo real
                y = 30
                for nombre, valor in angulos.items():
                    cv2.putText(
                        frame,
                        f"{nombre}: {valor:.1f}°",
                        (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )
                    y += 25

            cv2.imshow("Ángulos del cuerpo superior", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        camara_pose.release()


if __name__ == "__main__":
    main()
