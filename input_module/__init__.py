"""
Módulo input_module: gestiona ejemplos predefinidos
"""
try:
    from .ejemplos import EJEMPLOS_LINEALES, EJEMPLOS_NO_LINEALES, get_ejemplo
except ImportError:
    from ejemplos import EJEMPLOS_LINEALES, EJEMPLOS_NO_LINEALES, get_ejemplo

__all__ = ['EJEMPLOS_LINEALES', 'EJEMPLOS_NO_LINEALES', 'get_ejemplo']
