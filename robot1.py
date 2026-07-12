import os
import time
from dynamixel_sdk import * # Importa la librería oficial

# --- CONFIGURACIÓN DEL ROBOTIS MINI ---
ADDR_TORQUE_ENABLE       = 24    # Dirección para encender el torque
ADDR_GOAL_POSITION       = 30    # Dirección para la posición
BAUDRATE                 = 1000000 # Velocidad de comunicación del Mini
PROTOCOL_VERSION         = 2.0   # ¡Importante! El Mini usa 2.0
DEVICENAME               = 'COM5' # Tu puerto detectado

# IDs de los motores (El Mini suele tener del 1 al 16)
DXL_ID                   = 1     
TORQUE_ENABLE            = 1     # Valor para encender
TORQUE_DISABLE           = 0     # Valor para apagar

# Inicializar manejadores
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 1. Abrir Puerto
if portHandler.openPort():
    print("Puerto abierto con éxito")
else:
    print("Error abriendo el puerto")
    quit()

# 2. Configurar Baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Velocidad configurada a 1Mbps")
else:
    print("Error configurando velocidad")
    quit()

# 3. ENCENDER TORQUE (Si no se enciende, el motor no se mueve)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print(f"Error de comunicación: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"Error de motor: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print(f"Torque del motor {DXL_ID} encendido.")

# 4. MOVER MOTOR (Prueba de 3 posiciones)
posiciones = [512, 300, 700, 512] # Centro, derecha, izquierda, centro

try:
    for pos in posiciones:
        print(f"Moviendo a posición: {pos}")
        # Escribimos 2 bytes (la posición del XL-320 va de 0 a 1023)
        packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, pos)
        time.sleep(1.5) # Pausa para que el robot llegue a la posición

finally:
    # 5. APAGAR TORQUE Y CERRAR (Para que el robot se relaje y no gaste batería)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    portHandler.closePort()
    print("Puerto cerrado y motor relajado.")