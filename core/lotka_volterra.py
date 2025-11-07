"""
Sistema Depredador-Presa Lotka-Volterra
Núcleo matemático del modelo dinámico
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve


class SistemaLotkaVolterra:
    """Implementa el modelo Lotka-Volterra de depredador-presa"""
    
    PARAMS_DEFECTO = {'alpha': 1.0, 'beta': 0.1, 'gamma': 0.1, 'delta': 0.5}
    
    def __init__(self, alpha=None, beta=None, gamma=None, delta=None):
        """Inicializa el sistema: dx/dt = α·x - β·x·y, dy/dt = γ·x·y - δ·y"""
        self.alpha = alpha or self.PARAMS_DEFECTO['alpha']
        self.beta = beta or self.PARAMS_DEFECTO['beta']
        self.gamma = gamma or self.PARAMS_DEFECTO['gamma']
        self.delta = delta or self.PARAMS_DEFECTO['delta']
        
        self.equilibrio_trivial = (0, 0)
        self.equilibrio_interior = (self.delta / self.gamma, self.alpha / self.beta)
    
    def ecuaciones(self, estado, t):
        """Ecuaciones diferenciales: retorna [dx/dt, dy/dt]"""
        x, y = estado
        return [
            self.alpha * x - self.beta * x * y,
            self.gamma * x * y - self.delta * y
        ]
    
    def integrar_trayectoria(self, estado_inicial, t_final, n_puntos=1000):
        """Integra una trayectoria: retorna (t, trayectoria)"""
        t = np.linspace(0, t_final, n_puntos)
        return t, odeint(self.ecuaciones, estado_inicial, t)
    
    def calcular_jacobiano(self, punto):
        """Retorna matriz jacobiana en punto (x, y)"""
        x, y = punto
        return np.array([
            [self.alpha - self.beta * y, -self.beta * x],
            [self.gamma * y, self.gamma * x - self.delta]
        ], dtype=float)
    
    def analizar_estabilidad(self, punto=None):
        """Analiza estabilidad de un punto de equilibrio"""
        punto = punto or self.equilibrio_interior
        J = self.calcular_jacobiano(punto)
        autovalores = np.linalg.eigvals(J)
        
        return {
            'punto': punto,
            'jacobiano': J,
            'autovalores': autovalores,
            'traza': np.trace(J),
            'determinante': np.linalg.det(J),
            'es_estable': np.all(np.real(autovalores) <= 0),
            'es_centro': np.allclose(np.real(autovalores), 0)
        }
    
    def calcular_ciclo_periodico(self):
        """Retorna propiedades del ciclo periódico"""
        eq = self.equilibrio_interior
        return {
            'equilibrio': eq,
            'presas_equilibrio': eq[0],
            'depredadores_equilibrio': eq[1],
            'periodo_aproximado': 2 * np.pi / np.sqrt(self.alpha * self.delta)
        }
    
    def campo_vectorial(self, X, Y):
        """Calcula el campo vectorial en malla de puntos"""
        return (
            self.alpha * X - self.beta * X * Y,
            self.gamma * X * Y - self.delta * Y
        )
    
    def obtener_resumen_parametros(self):
        """Retorna dict con parámetros y propiedades actuales"""
        return {
            'alpha': self.alpha,
            'beta': self.beta,
            'gamma': self.gamma,
            'delta': self.delta,
            'equilibrio_interior': self.equilibrio_interior,
            'periodo_aproximado': 2 * np.pi / np.sqrt(self.alpha * self.delta)
        }
