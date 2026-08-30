import time

class MetricsEngine:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Mantenemos claves exactas
        self.magnitudes = {
            'hombros': 0.0, 'codos': 0.0, 'espalda': 0.0, 
            'cadera': 0.0, 'rodillas': 0.0, 'cuello': 0.0
        }

    def update(self, joint_type, diff):
 
        # Si la articulación existe, sumamos el error absoluto
        if joint_type in self.magnitudes:
            self.magnitudes[joint_type] += abs(diff) * 0.01

    def get_results(self):
        return self.magnitudes