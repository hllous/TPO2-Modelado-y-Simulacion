"""
Funciones auxiliares para trayectorias (simplificado con DRY)
calculate_vector_field se reemplazó con math_utils.calcular_campo_vectorial
"""

import numpy as np
from scipy.integrate import odeint


def integrate_trajectory_limited(sistema, condicion_inicial, max_distance=100, 
                                min_distance=0.01, max_steps=1000, direccion=1,
                                xlim=None, ylim=None):
    """
    Integra trayectoria con límites para evitar inestabilidades numéricas
    
    Parámetros:
    - sistema: SistemaDinamico2D
    - condicion_inicial: [x0, y0]
    - max_distance: distancia máxima desde el origen (si no hay xlim/ylim)
    - min_distance: distancia mínima al origen
    - max_steps: número máximo de pasos
    - direccion: 1 (adelante) o -1 (atrás)
    - xlim, ylim: límites de la vista actual (opcional, pero recomendado)
    """
    puntos = []
    t_actual = 0
    estado = np.array(condicion_inicial, dtype=float)
    dt = 0.01 * direccion
    
    # Determinar límites efectivos
    if xlim and ylim:
        # Usar los límites de la vista actual con un margen generoso
        # Margen de 1.0 = 100% extra de cada lado (3x el área visible)
        margen = 1.0
        rango_x = xlim[1] - xlim[0]
        rango_y = ylim[1] - ylim[0]
        
        x_min = xlim[0] - margen * rango_x
        x_max = xlim[1] + margen * rango_x
        y_min = ylim[0] - margen * rango_y
        y_max = ylim[1] + margen * rango_y
        usar_limites_vista = True
    else:
        usar_limites_vista = False
    
    for _ in range(max_steps):
        # Verificar si está fuera de los límites
        if usar_limites_vista:
            # Verificar límites de la vista
            if (estado[0] < x_min or estado[0] > x_max or 
                estado[1] < y_min or estado[1] > y_max):
                break
        else:
            # Usar distancia desde origen (comportamiento original)
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
