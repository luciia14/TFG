import time

class MetricsEngine:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Mantenemos tus claves exactas
        self.magnitudes = {
            'hombros': 0.0, 'codos': 0.0, 'espalda': 0.0, 
            'cadera': 0.0, 'rodillas': 0.0, 'cuello': 0.0
        }

    def update(self, joint_type, diff):
        """
        Versión corregida: 
        Eliminamos el cálculo de 'dt' aquí. 
        Al no depender del tiempo entre llamadas, cada articulación 
        acumula su error de forma independiente y equitativa.
        """
        # Si la articulación existe, sumamos el error absoluto (magnitud)
        if joint_type in self.magnitudes:
            # Multiplicamos por un factor pequeño (0.01) para que el crecimiento 
            # sea manejable y consistente frame a frame.
            self.magnitudes[joint_type] += abs(diff) * 0.01

    def get_results(self):
        """Retorna el estado actual de las métricas"""
        return self.magnitudes