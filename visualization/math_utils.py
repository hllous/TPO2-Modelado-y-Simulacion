"""
Utilidades compartidas para cálculos matemáticos en visualización
Aplicación de principio DRY
"""

import numpy as np
from scipy.integrate import odeint


def calcular_campo_vectorial(sistema, X, Y):
    """
    Calcula derivadas para sistemas (personalizado o lineal)
    Patrón centralizado evitando duplicación
    
    Args:
        sistema: SistemaDinamico2D
        X, Y: malla de puntos (numpy arrays)
    
    Returns:
        (U, V): componentes del campo
    """
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if sistema.funcion_personalizada:
                derivadas = sistema.sistema_ecuaciones([X[i,j], Y[i,j]], 0)
            else:
                # Sistema lineal: dx/dt = Ax
                estado = np.array([X[i,j], Y[i,j]])
                derivadas = sistema.A @ estado
            
            U[i,j] = derivadas[0]
            V[i,j] = derivadas[1]
    
    return U, V


def normalizar_vectores(U, V):
    """
    Normaliza componentes vectoriales para visualización
    
    Returns:
        (U_norm, V_norm, M): magnitud normalizada
    """
    M = np.sqrt(U**2 + V**2)
    M[M == 0] = 1
    U_norm = U / M
    V_norm = V / M
    return U_norm, V_norm, M


def integrar_trayectoria(sistema, condicion_inicial, t_max=10, t_puntos=1000):
    """
    Integra una trayectoria del sistema
    
    Args:
        sistema: SistemaDinamico2D
        condicion_inicial: [x0, y0]
        t_max: tiempo máximo
        t_puntos: puntos de discretización
    
    Returns:
        solución integrada
    """
    t = np.linspace(0, t_max, t_puntos)
    return odeint(sistema.sistema_ecuaciones, condicion_inicial, t)


def encontrar_limites_automaticos(sistema, rango_busqueda=(-10, 10)):
    """
    Calcula límites automáticos basados en puntos de equilibrio
    Patrón centralizado
    
    Args:
        sistema: SistemaDinamico2D
        rango_busqueda: tupla (min, max) para búsqueda
    
    Returns:
        (xlim, ylim)
    """
    puntos_eq = sistema.encontrar_puntos_equilibrio(
        (rango_busqueda[0], rango_busqueda[1]), 
        (rango_busqueda[0], rango_busqueda[1])
    )
    
    if puntos_eq and len(puntos_eq) > 0:
        xs = [p[0] for p in puntos_eq]
        ys = [p[1] for p in puntos_eq]
        
        x_center = np.mean(xs)
        y_center = np.mean(ys)
        
        # Calcular rango basado en dispersión de puntos
        if len(puntos_eq) > 1:
            x_spread = max(xs) - min(xs)
            y_spread = max(ys) - min(ys)
        else:
            # Para un solo punto, usar su distancia al origen como referencia
            x_spread = abs(xs[0])
            y_spread = abs(ys[0])
        
        # Asegurar un rango mínimo razonable
        x_range = max(x_spread, 3) * 1.5
        y_range = max(y_spread, 3) * 1.5
        
        xlim = (x_center - x_range, x_center + x_range)
        ylim = (y_center - y_range, y_center + y_range)
    else:
        xlim = (rango_busqueda[0], -rango_busqueda[0])
        ylim = (rango_busqueda[0], -rango_busqueda[0])
    
    return xlim, ylim


def agregar_flechas_trayectoria(ax, trayectoria, color='b', num_flechas=5):
    """
    Agrega flechas direccionales a una trayectoria
    
    Args:
        ax: eje de matplotlib
        trayectoria: array de puntos
        color: color de las flechas
        num_flechas: cantidad de flechas
    """
    if len(trayectoria) < 10:
        return
    
    num_flechas = min(num_flechas, len(trayectoria) // 20)
    if num_flechas < 1:
        num_flechas = 1
    
    indices = np.linspace(10, len(trayectoria)-10, num_flechas, dtype=int)
    
    for idx in indices:
        if idx < len(trayectoria) - 1:
            x_start, y_start = trayectoria[idx]
            x_end, y_end = trayectoria[idx + 1]
            
            ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                       arrowprops=dict(arrowstyle='->', color=color, lw=2, alpha=0.8))
