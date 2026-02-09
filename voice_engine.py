import pyttsx3
import threading

class VoiceEngine:
    def __init__(self):
        self.is_speaking = False

    def decir(self, texto, es_exito=False):
        # Si ya está hablando y NO es un mensaje de éxito, ignoramos para no solapar
        if self.is_speaking and not es_exito:
            return
        
        # Lanzar en un hilo nuevo para no congelar la cámara
        threading.Thread(target=self._ejecutar_voz, args=(texto,), daemon=True).start()

    def _ejecutar_voz(self, texto):
        try:
            self.is_speaking = True
            # CREAMOS EL MOTOR DENTRO DEL HILO (Clave para que no se bloquee)
            engine = pyttsx3.init()
            engine.setProperty('rate', 155)
            
            # Configurar voz en español
            voices = engine.getProperty('voices')
            for voice in voices:
                if "spanish" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.say(texto)
            engine.runAndWait()
            # Forzamos la parada del motor para liberar el recurso
            engine.stop()
        except Exception as e:
            print(f"Error en hilo de voz: {e}")
        finally:
            self.is_speaking = False

# Instancia para el main
locutor = VoiceEngine()