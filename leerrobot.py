import time
from dynamixel_sdk import *

# --- CONFIGURACIÓN ---
DEVICENAME = 'COM5'
PROTOCOL_VERSION = 2.0
BAUDRATE = 1000000
ADDR_TORQUE_ENABLE = 24
ADDR_PRESENT_POSITION = 37  # Dirección para LEER la posición actual en XL-320
MOTORES_A_LEER = range(1, 17) # Lee del motor 1 al 16

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort() and portHandler.setBaudRate(BAUDRATE):
    print("--- MODO APRENDIZAJE ACTIVADO ---")
    
    # 1. Apagamos el torque de todos los motores para poder moverlos a mano
    for id_motor in MOTORES_A_LEER:
        packetHandler.write1ByteTxRx(portHandler, id_motor, ADDR_TORQUE_ENABLE, 0)
    
    print("Robot suelto. Colócalo en la posición deseada...")
    for i in range(5, 0, -1):
        print(f"Capturando en {i}...")
        time.sleep(1)

    # 2. Leemos la posición de cada motor
    print("\n--- POSICIÓN CAPTURADA ---")
    print("Copia esto en tu script principal:")
    print("nueva_pose = {")
    
    for id_motor in MOTORES_A_LEER:
        # Leemos 2 bytes de la posición actual
        pos, result, error = packetHandler.read2ByteTxRx(portHandler, id_motor, ADDR_PRESENT_POSITION)
        
        if result == COMM_SUCCESS:
            print(f"    {id_motor}: {pos},")
        else:
            # Si un motor no responde, simplemente lo saltamos
            continue
            
    print("}")

    portHandler.closePort()
else:
    print("No se pudo conectar al COM5")