import pyttsx3
import threading
import socket
import wave
import time
import os

class VoiceEngine:
    def __init__(self, esp_ip="192.168.1.100", udp_port=8888):
        self.is_speaking = False
        self.esp_ip = esp_ip
        self.udp_port = udp_port

    def decir(self, texto, es_exito=False):
        # Evita la superposición de mensajes de voz, priorizando las confirmaciones de éxito
        if self.is_speaking and not es_exito:
            return
        
        # hilo secundario para no bloquear el hilo de inferencia visual
        threading.Thread(target=self._ejecutar_voz, args=(texto,), daemon=True).start()

    def _ejecutar_voz(self, texto):
        archivo_temp = "temp_voz.wav"
        try:
            self.is_speaking = True
            
            # Generación del audio mediante síntesis de voz
            engine = pyttsx3.init()
            engine.setProperty('rate', 155)
            
            # Configuración del idioma
            voices = engine.getProperty('voices')
            for voice in voices:
                if "spanish" in voice.name.lower() or "es" in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Se guarda el resultado en un archivo temporal
            engine.save_to_file(texto, archivo_temp)
            engine.runAndWait()
            engine.stop()

            #Transmisión del archivo de audio por red a la ESP32
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            with wave.open(archivo_temp, 'rb') as wf:
                sample_rate = wf.getframerate()
                num_channels = wf.getnchannels()
                samp_width = wf.getsampwidth()
                
                # Se fragmenta el audio en paquetes
                chunk_bytes = 1024
                frames_per_chunk = chunk_bytes // (samp_width * num_channels)
                
                data = wf.readframes(frames_per_chunk)
                
                while data:
                    # Envío del paquete a la dirección y puerto configurados
                    sock.sendto(data, (self.esp_ip, self.udp_port))
                    
                    # Cálculo del tiempo de espera para sincronizar el envío con la reproducción
                    frames_read = len(data) // (samp_width * num_channels)
                    sleep_time = frames_read / sample_rate
                    
                    # Factor de ajuste para compensar la latencia
                    time.sleep(sleep_time * 0.9)
                    
                    data = wf.readframes(frames_per_chunk)
                    
        except Exception as e:
            print(f"[Error] Excepción en la transmisión de audio UDP: {e}")
        finally:
            self.is_speaking = False
            
            # Limpieza de recursos
            if os.path.exists(archivo_temp):
                try:
                    os.remove(archivo_temp)
                except OSError:
                    pass

locutor = VoiceEngine(esp_ip="192.168.1.100", udp_port=8888)