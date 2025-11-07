"""
Módulo core: contiene la lógica matemática del sistema dinámico
"""
from .sistema import SistemaDinamico2D
from .bifurcacion import AnalizadorBifurcacion
from .utils import normalizar_funciones, FUNCIONES_NUMPY, FUNCIONES_SYMPY

__all__ = ['SistemaDinamico2D', 'AnalizadorBifurcacion', 
           'normalizar_funciones', 'FUNCIONES_NUMPY', 'FUNCIONES_SYMPY']
