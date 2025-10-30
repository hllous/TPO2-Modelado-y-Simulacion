"""
Análisis de bifurcaciones en sistemas dinámicos 1D
Calcula puntos de equilibrio y estabilidad usando SymPy
"""

import sympy as sp
import numpy as np
from typing import List, Tuple, Dict


class AnalizadorBifurcacion:
    """Clase para analizar bifurcaciones de sistemas dinámicos 1D"""
    
    def __init__(self, function_str: str):
        """
        Inicializa el analizador con una función f(x, r)
        
        Args:
            function_str: String de la función, ej: "r + x - x**3"
        """
        self.x = sp.Symbol('x', real=True)
        self.r = sp.Symbol('r', real=True)
        
        try:
            local_dict = {'x': self.x, 'r': self.r}
            self.f = sp.sympify(function_str, locals=local_dict)
        except Exception as e:
            raise ValueError(f"Error al parsear la función: {e}")
        
        self.df_dx = sp.diff(self.f, self.x)
        
    def encontrar_equilibrios(self, r_value: float = None) -> List[sp.Expr]:
        """
        Encuentra puntos de equilibrio resolviendo f(x, r) = 0
        
        Args:
            r_value: Valor específico de r, o None para solución simbólica
            
        Returns:
            Lista de puntos de equilibrio
        """
        if r_value is not None:
            r_rational = sp.Rational(r_value).limit_denominator(1000)
            eq = self.f.subs(self.r, r_rational)
        else:
            eq = self.f
            
        equilibria = sp.solve(eq, self.x, rational=False, simplify=False)
        return equilibria
    
    def estabilidad(self, x_eq: float, r_value: float) -> str:
        """
        Determina la estabilidad de un punto de equilibrio
        
        Args:
            x_eq: Punto de equilibrio
            r_value: Valor del parámetro r
            
        Returns:
            'estable' si df/dx < 0, 'inestable' si df/dx > 0, 'neutral' si df/dx = 0
        """
        derivative = float(self.df_dx.subs([(self.x, x_eq), (self.r, r_value)]))
        
        if abs(derivative) < 1e-10:
            return 'neutral'
        elif derivative < 0:
            return 'estable'
        else:
            return 'inestable'
    
    def obtener_equilibrios_con_estabilidad(self, r_value: float) -> List[Dict]:
        """
        Obtiene puntos de equilibrio con su estabilidad
        
        Args:
            r_value: Valor del parámetro r
            
        Returns:
            Lista de diccionarios con 'x' y 'estabilidad'
        """
        equilibria = self.encontrar_equilibrios(r_value)
        results = []
        
        for eq in equilibria:
            try:
                x_val = complex(eq)
                if abs(x_val.imag) < 1e-10:
                    x_float = float(x_val.real)
                    estab = self.estabilidad(x_float, r_value)
                    results.append({'x': x_float, 'estabilidad': estab})
            except (TypeError, ValueError):
                pass
                
        return results
    
    def generar_datos_bifurcacion(self, r_range: Tuple[float, float], 
                                  num_points: int = 500) -> Dict:
        """
        Genera datos para el diagrama de bifurcación
        
        Args:
            r_range: Rango de valores de r (r_min, r_max)
            num_points: Número de puntos a evaluar
            
        Returns:
            Diccionario con arrays de r, x, y estabilidad
        """
        r_min, r_max = r_range
        r_values = np.linspace(r_min, r_max, num_points)
        
        stable_r = []
        stable_x = []
        unstable_r = []
        unstable_x = []
        
        for r_val in r_values:
            eq_data = self.obtener_equilibrios_con_estabilidad(r_val)
            
            for eq in eq_data:
                if eq['estabilidad'] == 'estable':
                    stable_r.append(r_val)
                    stable_x.append(eq['x'])
                elif eq['estabilidad'] == 'inestable':
                    unstable_r.append(r_val)
                    unstable_x.append(eq['x'])
        
        return {
            'estable': {'r': np.array(stable_r), 'x': np.array(stable_x)},
            'inestable': {'r': np.array(unstable_r), 'x': np.array(unstable_x)}
        }
    
    def evaluar_funcion(self, x_vals: np.ndarray, r_value: float) -> np.ndarray:
        """
        Evalúa la función f(x, r) para un array de valores x
        
        Args:
            x_vals: Array de valores de x
            r_value: Valor del parámetro r
            
        Returns:
            Array de valores f(x, r)
        """
        f_lambda = sp.lambdify((self.x, self.r), self.f, 'numpy')
        return f_lambda(x_vals, r_value)
