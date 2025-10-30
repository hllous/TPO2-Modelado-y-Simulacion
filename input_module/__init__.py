"""
Módulo input_module: gestiona ejemplos predefinidos
"""
try:
    from .ejemplos import EJEMPLOS_LINEALES, EJEMPLOS_NO_LINEALES, get_ejemplo
    from .bifurcacion import EJEMPLOS_BIFURCACION, obtener_nombres_ejemplos_bifurcacion, obtener_ejemplo_bifurcacion
except ImportError:
    from ejemplos import EJEMPLOS_LINEALES, EJEMPLOS_NO_LINEALES, get_ejemplo
    from bifurcacion import EJEMPLOS_BIFURCACION, obtener_nombres_ejemplos_bifurcacion, obtener_ejemplo_bifurcacion

__all__ = ['EJEMPLOS_LINEALES', 'EJEMPLOS_NO_LINEALES', 'get_ejemplo', 
           'EJEMPLOS_BIFURCACION', 'obtener_nombres_ejemplos_bifurcacion', 'obtener_ejemplo_bifurcacion']
