"""
Núcleo matemático para análisis de sistemas no lineales 1D
"""

import numpy as np
import sympy as sp
from scipy.integrate import odeint
from scipy.optimize import fsolve
from typing import List, Tuple, Dict, Optional


class SistemaDinamico1D:
    """Representa un sistema dinámico 1D no lineal general"""
    
    def __init__(self, funcion_str: str):
        """
        Inicializa el sistema 1D
        
        Parámetros:
        - funcion_str: expresión de dx/dt (ej: "-x + x**3")
        """
        self.x = sp.Symbol('x', real=True)
        try:
            self.f = sp.sympify(funcion_str, locals={'x': self.x})
        except Exception as e:
            raise ValueError(f"Error al parsear la función: {e}")
        
        self.df_dx = sp.diff(self.f, self.x)
        self.f_lambda = sp.lambdify(self.x, self.f, 'numpy')
        self.df_lambda = sp.lambdify(self.x, self.df_dx, 'numpy')
    
    def evaluar_funcion(self, x_vals: np.ndarray) -> np.ndarray:
        """Evalúa f(x) para array de valores"""
        return self.f_lambda(x_vals)
    
    def evaluar_derivada(self, x_vals: np.ndarray) -> np.ndarray:
        """Evalúa f'(x) para array de valores"""
        return self.df_lambda(x_vals)
    
    def encontrar_equilibrios(self, xlim: Tuple[float, float] = (-10, 10),
                              tolerancia: float = 1e-6) -> List[float]:
        """Encuentra puntos de equilibrio"""
        puntos_equilibrio = []
        
        # Generar puntos iniciales
        x_init = np.linspace(xlim[0], xlim[1], 50)
        
        for x0 in x_init:
            try:
                sol = fsolve(self.f_lambda, x0, full_output=True)
                x_eq = sol[0][0]
                info = sol[1]
                
                if xlim[0] <= x_eq <= xlim[1] and info['fvec'][0]**2 < tolerancia**2:
                    if not any(abs(x_eq - p) < tolerancia for p in puntos_equilibrio):
                        puntos_equilibrio.append(x_eq)
            except:
                continue
        
        return sorted(puntos_equilibrio)
    
    def clasificar_estabilidad(self, x_eq: float) -> str:
        """Clasifica estabilidad del punto de equilibrio"""
        derivada = self.df_lambda(x_eq)
        
        if abs(derivada) < 1e-10:
            return "neutral"
        elif derivada < 0:
            return "estable"
        else:
            return "inestable"
    
    def integrar_trayectoria(self, x0: float, t_span: Tuple[float, float],
                            num_puntos: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Integra una trayectoria numéricamente"""
        t = np.linspace(t_span[0], t_span[1], num_puntos)
        
        def sistema(x, t):
            return self.f_lambda(x)
        
        try:
            x_trajectory = odeint(sistema, x0, t)
            return t, x_trajectory.flatten()
        except:
            return t, np.full_like(t, x0)
    
    def resolver_analitico_lineal(self) -> Optional[str]:
        """Intenta resolver analíticamente si es lineal"""
        try:
            # Verificar si es de la forma dx/dt = -ax^n
            coeff = sp.solve(self.f - (-self.x), self.x)
            if len(coeff) == 0:
                return None
            return str(self.f)
        except:
            return None
