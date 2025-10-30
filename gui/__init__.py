"""
Módulo gui: interfaz gráfica principal
"""
try:
    from .interfaz import InterfazGrafica
except ImportError:
    from interfaz import InterfazGrafica

__all__ = ['InterfazGrafica']
