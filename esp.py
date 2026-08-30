import cv2
import socket
import threading
import io
import time
from gtts import gTTS
from pydub import AudioSegment
import static_ffmpeg
static_ffmpeg.add_paths()

# --- CONFIGURACIÓN ---
ESP32_IP = '192.168.1.129'  # Pon la IP real de tu ESP32
UDP_PORT = 8888              # Puerto UDP configurado en la ESP32 para el audio

# URL del streaming de vídeo (Servidor básico de ESP32-CAM o Tasmota)
URL_STREAM = f'http://{ESP32_IP}:81/stream'

# Configuración del Socket UDP para enviar audio
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --- FUNCIÓN PARA ENVIAR AUDIO AL ROBOT ---
def enviar_audio(texto):
    """
    Convierte texto a voz y lo transmite vía UDP a la ESP32 / MAX98357A.
    """
    try:
        print(f"Generando audio: '{texto}'...")
        # 1. Convertir texto a MP3 en memoria
        tts = gTTS(text=texto, lang='es')
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        # 2. Convertir a PCM 16kHz, mono, 16-bit (compatible con I2S)
        audio = AudioSegment.from_file(mp3_buffer, format="mp3")
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        raw_data = audio.raw_data

        print("Transmitiendo audio al altavoz...")
        # 3. Enviar en paquetes UDP a la ESP32
        chunk_size = 512
        for i in range(0, len(raw_data), chunk_size):
            chunk = raw_data[i:i + chunk_size]
            sock.sendto(chunk, (ESP32_IP, UDP_PORT))
            time.sleep(0.015)  # Control de flujo para no saturar la red
            
        print("Audio enviado con éxito.")
    except Exception as e:
        print(f"Error al enviar el audio: {e}")

# --- INICIAR EL SALUDO DE BIENVENIDA (En segundo plano) ---
# Se lanza en un hilo paralelo (Thread) para que no bloquee el inicio del vídeo OpenCV
hilo_audio = threading.Thread(target=enviar_audio, args=("Hola, bienvenidos",))
hilo_audio.start()

# --- TRANSMISIÓN DE VÍDEO (OPENCV) ---
print(f"Conectando a la cámara en {URL_STREAM}...")
stream = cv2.VideoCapture(URL_STREAM)

if not stream.isOpened():
    print("Error: No se pudo conectar a la transmisión de la cámara.")
    print("Asegúrate de que la cámara esté encendida y la IP sea correcta.")
    exit()

print("Conexión exitosa. Presiona 'q' para salir.")

while True:
    ret, frame = stream.read()

    if not ret:
        print("Error al leer frame de la cámara.")
        break

    # --- PROCESAMIENTO DE IMAGEN ---
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges_frame = cv2.Canny(processed_frame, 50, 150)

    # --- VISUALIZACIÓN ---
    cv2.imshow('Camara Robot - Color', frame)
    cv2.imshow('Camara Robot - Bordes', edges_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- LIMPIEZA ---
stream.release()
cv2.destroyAllWindows()
sock.close()
print("Limpieza completada. Programa finalizado.")