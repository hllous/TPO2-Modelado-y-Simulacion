"""
Módulo para modelos de combate y epidemiología
Incluye: virus-paciente, zombie-humanos, etc.
"""

import numpy as np
from scipy.integrate import odeint
import sympy as sp


class ModeloVirusInfeccion:
    """
    Modelo de infección viral: dP/dt = K*P*(N-P)
    
    Variables:
    - P(t): Población infectada en el tiempo t
    - K: Constante de infección
    - N: Máximo de población (población total)
    - P(0): Población inicial infectada
    """
    
    def __init__(self, K, N, P0):
        """
        Inicializa el modelo de infección
        
        Parámetros:
        - K: constante de infección (tasa de contagio)
        - N: población máxima/total
        - P0: población inicial infectada en t=0
        """
        self.K = float(K)
        self.N = float(N)
        self.P0 = float(P0)
        
        # Validaciones
        if self.K <= 0:
            raise ValueError("K (constante de infección) debe ser positiva")
        if self.N <= 0:
            raise ValueError("N (población máxima) debe ser positiva")
        if self.P0 < 0 or self.P0 > self.N:
            raise ValueError(f"P0 debe estar entre 0 y N={self.N}")
    
    def ecuacion_diferencial(self, P, t):
        """
        Ecuación diferencial: dP/dt = K*P*(N-P)
        
        Parámetros:
        - P: población infectada actual
        - t: tiempo
        
        Retorna: dP/dt
        """
        return self.K * P * (self.N - P)
    
    def resolver(self, t_max=100, puntos=1000):
        """
        Resuelve la ecuación diferencial numéricamente
        
        Parámetros:
        - t_max: tiempo máximo de simulación
        - puntos: número de puntos de discretización
        
        Retorna: (t, P) arrays de tiempo y población
        """
        t = np.linspace(0, t_max, puntos)
        P = odeint(self.ecuacion_diferencial, self.P0, t)
        return t, P.flatten()
    
    def evaluar_en_tiempo(self, t):
        """
        Evalúa P(t) - población infectada en un tiempo específico
        
        Parámetros:
        - t: tiempo a evaluar
        
        Retorna: P(t) - población infectada en ese tiempo
        """
        if t < 0:
            raise ValueError("El tiempo debe ser no negativo")
        
        # Resolver hasta ese tiempo con alta precisión
        t_array = np.linspace(0, t, max(int(t * 10), 100))
        P = odeint(self.ecuacion_diferencial, self.P0, t_array)
        return float(P[-1, 0])
    
    def solucion_analitica(self, t):
        """
        Solución analítica exacta del modelo logístico
        P(t) = N / (1 + ((N - P0) / P0) * exp(-K*N*t))
        
        Parámetros:
        - t: tiempo o array de tiempos
        
        Retorna: P(t) población infectada
        """
        if self.P0 == 0:
            return 0
        
        A = (self.N - self.P0) / self.P0
        return self.N / (1 + A * np.exp(-self.K * self.N * t))
    
    def tiempo_hasta_porcentaje(self, porcentaje):
        """
        Calcula el tiempo necesario para alcanzar un porcentaje de la población
        
        Parámetros:
        - porcentaje: porcentaje de la población total (0-100)
        
        Retorna: tiempo en que se alcanza ese porcentaje
        """
        if porcentaje <= 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        
        P_objetivo = self.N * (porcentaje / 100)
        
        if self.P0 >= P_objetivo:
            return 0
        
        # Fórmula analítica: t = -ln((N - P) / (P - 0)) / (K*N) - ln((N - P0) / P0) / (K*N)
        # Simplificado: t = (1/(K*N)) * ln((P/P0) * ((N-P0)/(N-P)))
        if P_objetivo >= self.N:
            return float('inf')
        
        t = (1 / (self.K * self.N)) * np.log((P_objetivo / self.P0) * ((self.N - self.P0) / (self.N - P_objetivo)))
        return t
    
    def punto_inflexion(self):
        """
        Calcula el punto de inflexión (máxima tasa de infección)
        
        Retorna: (t_inflexion, P_inflexion)
        """
        # El punto de inflexión ocurre cuando P = N/2
        P_inflexion = self.N / 2
        
        if self.P0 >= P_inflexion:
            return 0, self.P0
        
        t_inflexion = self.tiempo_hasta_porcentaje(50)
        return t_inflexion, P_inflexion
    
    def estadisticas(self):
        """
        Calcula estadísticas del modelo
        
        Retorna: diccionario con información relevante
        """
        t_infl, P_infl = self.punto_inflexion()
        t_50 = self.tiempo_hasta_porcentaje(50)
        t_90 = self.tiempo_hasta_porcentaje(90)
        t_99 = self.tiempo_hasta_porcentaje(99)
        
        return {
            'poblacion_inicial': self.P0,
            'poblacion_maxima': self.N,
            'constante_infeccion': self.K,
            'punto_inflexion_tiempo': t_infl,
            'punto_inflexion_poblacion': P_infl,
            'tiempo_50_porciento': t_50,
            'tiempo_90_porciento': t_90,
            'tiempo_99_porciento': t_99,
            'tasa_maxima_infeccion': self.K * P_infl * (self.N - P_infl)
        }
    
    def __str__(self):
        """Representación en string del modelo"""
        return (f"Modelo de Infección Viral\n"
                f"  Ecuación: dP/dt = {self.K}*P*({self.N}-P)\n"
                f"  P(0) = {self.P0}\n"
                f"  N (población máxima) = {self.N}\n"
                f"  K (tasa de infección) = {self.K}")

