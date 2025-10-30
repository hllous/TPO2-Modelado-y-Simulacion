"""
Módulo gui: interfaz gráfica principal
"""
try:
    from .interfaz import InterfazGrafica
    from .bifurcacion import InterfazBifurcacion
except ImportError:
    from interfaz import InterfazGrafica
    from bifurcacion import InterfazBifurcacion

__all__ = ['InterfazGrafica', 'InterfazBifurcacion']
