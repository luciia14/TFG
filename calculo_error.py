import time

class MetricsEngine:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Definimos todas las claves posibles desde el inicio
        self.magnitudes = {
            'hombros': 0.0, 
            'codos': 0.0, 
            'espalda': 0.0, 
            'cadera': 0.0, 
            'rodillas': 0.0, 
            'cuello': 0.0
        }
        self.last_time = time.time()

    def update(self, joint_type, angle, target_angle):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        
        error = abs(target_angle - angle)
        
        if error > 5:
            # Usamos .get para que si la articulación no existe, no falle, 
            # o simplemente verificamos si existe antes de sumar:
            if joint_type in self.magnitudes:
                self.magnitudes[joint_type] += (error * dt)
            else:
                # Opcional: imprimir qué articulación desconocida llega
                print(f"[DEBUG] Articulación no registrada: {joint_type}")