"""
Funciones auxiliares para trayectorias (simplificado con DRY)
calculate_vector_field se reemplazó con math_utils.calcular_campo_vectorial
"""

import numpy as np
from scipy.integrate import odeint


def integrate_trajectory_limited(sistema, condicion_inicial, max_distance=100, 
                                min_distance=0.01, max_steps=1000, direccion=1):
    """
    Integra trayectoria con límites para evitar inestabilidades numéricas
    Parámetro simplificado: dirección es solo 1 o -1
    """
    puntos = []
    t_actual = 0
    estado = np.array(condicion_inicial, dtype=float)
    dt = 0.01 * direccion
    
    for _ in range(max_steps):
        distancia = np.sqrt(estado[0]**2 + estado[1]**2)
        
        if distancia > max_distance or distancia < min_distance:
            break
        
        puntos.append(estado.copy())
        
        try:
            derivada = sistema.sistema_ecuaciones(estado, t_actual)
            estado = estado + dt * derivada
            t_actual += dt
        except:
            break
    
    return np.array(puntos) if puntos else np.array([condicion_inicial])
