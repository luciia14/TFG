import cv2
import sys

print(f"[TEST]: Versión de OpenCV instalada: {cv2.__version__}")
print("[TEST]: Intentando abrir la cámara por defecto (ID 0)...")

# Inicializa la webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("\n[ERROR]: No se pudo acceder a la webcam.")
    print("Verifica que ninguna otra aplicación (como Teams, Zoom o Discord) la esté usando.\n")
    sys.exit()

print("[TEST]: Cámara abierta correctamente. Presiona la tecla 'ESC' en la ventana de vídeo para salir.")

while True:
    # Lee el frame de la cámara
    ret, frame = cap.read()
    
    if not ret:
        print("[ERROR]: No se puede recibir el feed de la cámara (stream vacío).")
        break

    # Muestra el frame en una ventana nativa de OpenCV
    cv2.imshow("Prueba OpenCV Directa", frame)

    # Si presionas la tecla ESC (código 27), se rompe el bucle
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
print("[TEST]: Test finalizado y recursos liberados con éxito.")