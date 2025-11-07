"""
Módulo core: contiene la lógica matemática del sistema dinámico
"""
from .sistema import SistemaDinamico2D
from .bifurcacion import AnalizadorBifurcacion
from .lotka_volterra import SistemaLotkaVolterra
from .analizador_lv import AnalizadorLotkaVolterra
from .utils import normalizar_funciones, FUNCIONES_NUMPY, FUNCIONES_SYMPY

__all__ = ['SistemaDinamico2D', 'AnalizadorBifurcacion', 'SistemaLotkaVolterra', 'AnalizadorLotkaVolterra',
           'normalizar_funciones', 'FUNCIONES_NUMPY', 'FUNCIONES_SYMPY']
