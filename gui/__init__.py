"""
Módulo gui: interfaz gráfica principal
"""
try:
    from .interfaz import InterfazGrafica
    from .bifurcacion import InterfazBifurcacion
    from .lotka_volterra import InterfazLotkaVolterra
except ImportError:
    from interfaz import InterfazGrafica
    from bifurcacion import InterfazBifurcacion
    from lotka_volterra import InterfazLotkaVolterra

__all__ = ['InterfazGrafica', 'InterfazBifurcacion', 'InterfazLotkaVolterra']
