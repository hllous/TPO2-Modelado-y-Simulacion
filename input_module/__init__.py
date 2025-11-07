"""
Módulo input_module: gestiona ejemplos predefinidos y entrada de parámetros
"""
from .ejemplos import EJEMPLOS_LINEALES, EJEMPLOS_NO_LINEALES
from .bifurcacion import EJEMPLOS_BIFURCACION, obtener_nombres_ejemplos_bifurcacion, obtener_ejemplo_bifurcacion
from .lotka_volterra import InputLotkaVolterra

__all__ = ['EJEMPLOS_LINEALES', 'EJEMPLOS_NO_LINEALES',
           'EJEMPLOS_BIFURCACION', 'obtener_nombres_ejemplos_bifurcacion', 'obtener_ejemplo_bifurcacion',
           'InputLotkaVolterra']
