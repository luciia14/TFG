import serial
import time

def emular_robot(puerto='COM3'):
    try:
        # Abrimos el puerto COM3
        ser = serial.Serial(puerto, 57600, timeout=0.1)
        print(f"--- EMULADOR ACTIVO EN {puerto} ---")
        print("Esperando a que R+ Motion pregunte por el robot...")

        while True:
            # 1. Escuchar si R+ Motion envía algo
            if ser.in_waiting > 0:
                lectura = ser.read(ser.in_waiting)
                
                # 2. Si R+ Motion pregunta "¿Quién eres?" (Ping), respondemos "Soy un robot"
                # El paquete de respuesta estándar para un Ping (0x01) es este:
                if len(lectura) >= 6 and lectura[4] == 0x01: 
                    id_robot = lectura[2]
                    # Respuesta de estado OK
                    respuesta = bytearray([0xFF, 0xFF, id_robot, 0x02, 0x00, 255 - ((id_robot + 2) % 256)])
                    ser.write(respuesta)
                    print(f"¡R+ Motion detectado! Respondiendo al motor ID {id_robot}...")

            # 3. Mientras tanto, enviamos un movimiento leve al ID 1 para que veas algo
            t = time.time()
            pos = int(512 + 100 * (t % 2 - 1)) # Oscilación simple
            p_bajo = pos & 0xFF
            p_alto = (pos >> 8) & 0xFF
            paquete_mov = bytearray([0xFF, 0xFF, 0x01, 0x05, 0x03, 0x1E, p_bajo, p_alto])
            checksum = 255 - (sum(paquete_mov[2:]) % 256)
            paquete_mov.append(checksum)
            
            ser.write(paquete_mov)
            time.sleep(0.01)

    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nDetenido.")
    finally:
        ser.close()

if __name__ == "__main__":
    emular_robot('COM3')