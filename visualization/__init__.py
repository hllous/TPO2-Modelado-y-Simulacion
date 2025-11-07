"""
Módulo visualization: contiene la lógica de graficación
"""
from .grapher import Grapher
from .plotter import plot_trajectory, calculate_vector_field
from .bifurcacion import VisualizadorBifurcacion

__all__ = ['Grapher', 'plot_trajectory', 'calculate_vector_field', 'VisualizadorBifurcacion']
