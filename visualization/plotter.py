"""
Funciones auxiliares para cálculos de trayectorias y campos vectoriales
"""

import numpy as np
from scipy.integrate import odeint


def calculate_vector_field(sistema, X, Y):
    """
    Calcula el campo vectorial en una malla de puntos
    
    Retorna: (U, V) - componentes del campo
    """
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            derivadas = sistema.sistema_ecuaciones([X[i,j], Y[i,j]], 0)
            U[i,j] = derivadas[0]
            V[i,j] = derivadas[1]
    
    return U, V


def plot_trajectory(ax, sistema, condicion_inicial, tiempo_max=10, color='b', alpha=0.8):
    """
    Calcula e dibuja una trayectoria del sistema
    
    Parámetros:
    - ax: eje matplotlib
    - sistema: SistemaDinamico2D
    - condicion_inicial: [x0, y0]
    - tiempo_max: tiempo máximo de integración
    - color: color de la línea
    - alpha: transparencia
    
    Retorna: objeto de línea plotted
    """
    t = np.linspace(0, tiempo_max, 1000)
    
    try:
        solucion = odeint(sistema.sistema_ecuaciones, condicion_inicial, t)
        linea = ax.plot(solucion[:, 0], solucion[:, 1], 
                       color=color, linewidth=2, alpha=alpha)
        ax.plot(condicion_inicial[0], condicion_inicial[1], 'o', 
               color=color, markersize=8, markeredgecolor='darkred', markeredgewidth=2)
        return linea
    except:
        return None


def integrate_trajectory_limited(sistema, condicion_inicial, max_distance=100, 
                                min_distance=0.01, max_steps=1000, direccion=1):
    """
    Integra trayectoria con límites para evitar inestabilidades numéricas
    
    Parámetros:
    - sistema: SistemaDinamico2D
    - condicion_inicial: [x0, y0]
    - max_distance: distancia máxima del origen
    - min_distance: distancia mínima del origen
    - max_steps: máximo número de pasos
    - direccion: 1 para adelante, -1 para atrás
    
    Retorna: array de puntos
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
