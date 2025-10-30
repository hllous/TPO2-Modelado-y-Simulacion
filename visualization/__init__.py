"""
Módulo visualization: contiene la lógica de graficación
"""
try:
    from .grapher import Grapher
    from .plotter import plot_trajectory, calculate_vector_field
except ImportError:
    from grapher import Grapher
    from plotter import plot_trajectory, calculate_vector_field

__all__ = ['Grapher', 'plot_trajectory', 'calculate_vector_field']
