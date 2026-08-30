import time
from dynamixel_sdk import *

DEVICENAME          = 'COM5'
PROTOCOL_VERSION    = 2.0
BAUDRATE            = 1000000
ADDR_TORQUE_ENABLE  = 24
ADDR_GOAL_POSITION  = 30

#DICCIONARIOS DE POSICIONES PARA LOS 16 MOTORES

NEUTRAL_POSE = {i: 512 for i in range(1, 17)}

T_POSE = {i: 512 for i in range(1, 17)}

ARMS_BENT_90_POSE = {
    1: 512, 2: 512, 3: 512, 4: 512,
    5: 300, 6: 724,
    7: 512, 8: 512, 9: 512, 10: 512, 11: 512, 12: 512, 13: 512, 14: 512, 15: 512, 16: 512
}

BOTH_ARMS_UP_POSE = {
    1: 205, 2: 819,
    3: 512, 4: 512, 5: 512, 6: 512,
    7: 512, 8: 512, 9: 512, 10: 512, 11: 512, 12: 512, 13: 512, 14: 512, 15: 512, 16: 512
}

TORSO_INCLINED_POSE = {
    1: 512, 2: 512, 3: 512, 4: 512, 5: 512, 6: 512,
    7: 512, 8: 512,
    9: 600, 10: 600,
    11: 512, 12: 512,
    13: 420, 14: 420,
    15: 512, 16: 512
}

STAR_POSE = {
    1: 205, 2: 819,
    3: 512, 4: 512, 5: 512, 6: 512,
    7: 412, 8: 612,
    9: 512, 10: 512, 11: 512, 12: 512, 13: 512, 14: 512,
    15: 412, 16: 612
}

SQUAT_POSE = {
    1: 512, 2: 512, 3: 512, 4: 512, 5: 512, 6: 512,
    7: 512, 8: 512,
    9: 620, 10: 620,
    11: 380, 12: 380,
    13: 600, 14: 600,
    15: 512, 16: 512
}

LATERAL_SQUAT_POSE = {
    1: 205, 2: 512,
    3: 512, 4: 512, 5: 512, 6: 512,
    7: 450, 8: 570,
    9: 610, 10: 512,
    11: 390, 12: 512,
    13: 580, 14: 512, 15: 450, 16: 512
}

LUNGE_POSE = {
    1: 512, 2: 512, 3: 512, 4: 512, 5: 512, 6: 512,
    7: 512, 8: 512,
    9: 630, 10: 410,
    11: 380, 12: 640,
    13: 580, 14: 450,
    15: 512, 16: 512
}

FULL_BODY_POSE = {
    1: 612, 2: 412,
    3: 512, 4: 512, 5: 512, 6: 512,
    7: 512, 8: 512,
    9: 580, 10: 580,
    11: 440, 12: 440,
    13: 550, 14: 550,
    15: 512, 16: 512
}


# Mapeo por nombre de la postura
POSICIONES = {
    "NEUTRAL": NEUTRAL_POSE,
    "T_POSE": T_POSE,
    "ARMS_BENT_90": ARMS_BENT_90_POSE,
    "BOTH_ARMS_UP": BOTH_ARMS_UP_POSE,
    "TORSO_INCLINED": TORSO_INCLINED_POSE,
    "STAR_POSE": STAR_POSE,
    "SQUAT_POSE": SQUAT_POSE,
    "LATERAL_SQUAT": LATERAL_SQUAT_POSE,
    "LUNGE_POSE": LUNGE_POSE,
    "FULL_BODY": FULL_BODY_POSE
}

# Mapeo por número de estado
POSICIONES_POR_ESTADO = {
    0: T_POSE,
    1: ARMS_BENT_90_POSE,
    2: STAR_POSE,
    3: LATERAL_SQUAT_POSE,
    4: T_POSE,
    5: LUNGE_POSE,
    6: FULL_BODY_POSE
}


class RobotController:
    def __init__(self, port=DEVICENAME, baudrate=BAUDRATE):
        self.portHandler = PortHandler(port)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        self.baudrate = baudrate

    def conectar(self):
        if self.portHandler.openPort() and self.portHandler.setBaudRate(self.baudrate):
            self.set_torque(True)
            return True
        return False

    def set_torque(self, estado):
        valor = 1 if estado else 0
        for i in range(1, 17):
            self.packetHandler.write1ByteTxRx(self.portHandler, i, ADDR_TORQUE_ENABLE, valor)

    def mover_pose(self, pose_target, tiempo_espera=0.5):

        if isinstance(pose_target, str) and pose_target in POSICIONES:
            pose_dict = POSICIONES[pose_target]
        elif isinstance(pose_target, int) and pose_target in POSICIONES_POR_ESTADO:
            pose_dict = POSICIONES_POR_ESTADO[pose_target]
        elif isinstance(pose_target, dict):
            pose_dict = pose_target
        else:
            print(f"[ERROR RobotController]: Postura '{pose_target}' no reconocida.")
            return

        for id_motor, posicion in pose_dict.items():
            self.packetHandler.write2ByteTxRx(self.portHandler, id_motor, ADDR_GOAL_POSITION, posicion)
        
        if tiempo_espera > 0:
            time.sleep(tiempo_espera)

    def ir_a_neutro(self):
        self.mover_pose(NEUTRAL_POSE, tiempo_espera=1.0)

    def desconectar(self):
        self.ir_a_neutro()
        self.set_torque(False)
        self.portHandler.closePort()