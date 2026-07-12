import time
from dynamixel_sdk import *

# --- CONFIGURACIÓN ---
DEVICENAME          = 'COM5'
PROTOCOL_VERSION    = 2.0
BAUDRATE            = 1000000
ADDR_TORQUE_ENABLE  = 24
ADDR_GOAL_POSITION  = 30

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

def mover_suave(id_motor, posicion):
    packetHandler.write2ByteTxRx(portHandler, id_motor, ADDR_GOAL_POSITION, posicion)

try:
    if portHandler.openPort() and portHandler.setBaudRate(BAUDRATE):
        print("--- INICIANDO TEST DE ESTRÉS (ID 1, 2, 3) ---")
        
        # Activar Torque
        for i in [1, 2, 3]:
            packetHandler.write1ByteTxRx(portHandler, i, ADDR_TORQUE_ENABLE, 1)

        # Definimos los puntos del movimiento (Extremo A, Extremo B, Centro)
        puntos = [200, 800, 512]
        repeticiones = 3

        for motor in [1, 2, 3]:
            print(f"\nProbando Motor ID: {motor}")
            for r in range(repeticiones):
                print(f"  Repetición {r+1}/{repeticiones}")
                for p in puntos:
                    mover_suave(motor, p)
                    time.sleep(0.8) # Tiempo para que complete el recorrido

        print("\nTest finalizado con éxito.")

    else:
        print("Error: No se pudo abrir el puerto.")

finally:
    # Relajar motores
    for i in [1, 2, 3]:
        packetHandler.write1ByteTxRx(portHandler, i, ADDR_TORQUE_ENABLE, 0)
    portHandler.closePort()
    print("Motores liberados.")