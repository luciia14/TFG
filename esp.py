import cv2
import urllib.request
import numpy as np

# --- CONFIGURACIÓN ---
# Reemplaza con la dirección IP real de tu cámara Tasmota.
IP_CAMARA = '192.168.1.129' 
# Tasmota usa esta URL para el flujo MJPEG
URL_STREAM = f'http://{IP_CAMARA}:81/stream'

print(f"Conectando a la cámara en {URL_STREAM}...")

# Inicializar la captura de vídeo desde la URL
stream = cv2.VideoCapture(URL_STREAM)

# Comprobar si se ha abierto correctamente
if not stream.isOpened():
    print("Error: No se pudo conectar a la transmisión de la cámara.")
    print("Asegúrate de que la cámara esté encendida, el vídeo activado en la web y que la IP sea correcta.")
    exit()

print("Conexión exitosa. Presiona 'q' para salir.")

while True:
    # 1. Capturar el frame (imagen actual)
    ret, frame = stream.read()

    # Si no se pudo leer el frame (ej: la cámara se desconecta), salir
    if not ret:
        print("Error al leer frame de la cámara.")
        break

    # --- PROCESAMIENTO DE IMAGEN (EJEMPLO) ---
    
    # Ejemplo 1: Convertir la imagen a escala de grises
    # (Muy útil para muchos tipos de procesamiento)
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Ejemplo 2: Suavizar la imagen para reducir ruido antes de detectar bordes
    # blurred_frame = cv2.GaussianBlur(processed_frame, (5, 5), 0)

    # Ejemplo 3: Detectar bordes (Canny Edge Detection)
    # Ajusta los umbrales (50, 150) si necesitas más o menos sensibilidad.
    edges_frame = cv2.Canny(processed_frame, 50, 150)

    # --- VISUALIZACIÓN ---
    
    # Mostrar la imagen original (en color)
    cv2.imshow('Tasmota - Original (Color)', frame)
    
    # Mostrar la imagen procesada (bordes)
    cv2.imshow('Tasmota - Procesada (Bordes)', edges_frame)

    # Detectar si se presiona la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- LIMPIEZA ---
stream.release()
cv2.destroyAllWindows()
print("Limpieza completada. Programa finalizado.")