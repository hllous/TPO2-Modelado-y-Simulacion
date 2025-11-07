"""
Utilidades compartidas para el sistema dinámico
"""

import numpy as np
import sympy as sp


def normalizar_funciones(expresion):
    """
    Normaliza nombres de funciones matemáticas
    
    Parámetros:
    - expresion: string con la expresión a normalizar
    
    Retorna: expresión normalizada
    """
    return expresion.replace('sen', 'sin')


# Diccionario de funciones matemáticas para evaluación con numpy
FUNCIONES_NUMPY = {
    'np': np,
    'sin': np.sin,
    'sen': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'exp': np.exp,
    'log': np.log,
    'sqrt': np.sqrt,
    'abs': np.abs,
    'pi': np.pi,
    'e': np.e
}


# Diccionario de funciones matemáticas para sympify
FUNCIONES_SYMPY = {
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'exp': sp.exp,
    'log': sp.log,
    'sqrt': sp.sqrt,
    'pi': sp.pi,
    'e': sp.E
}


def crear_diccionario_variables_evaluacion(x1, x2, t, parametros=None):
    """
    Crea diccionario completo de variables para evaluar expresiones
    
    Parámetros:
    - x1, x2: variables de estado
    - t: tiempo
    - parametros: dict opcional con parámetros adicionales
    
    Retorna: diccionario con todas las variables disponibles
    """
    variables = {
        'x1': x1, 'x2': x2, 't': t,
        'x': x1, 'y': x2,
        **FUNCIONES_NUMPY
    }
    
    if parametros:
        variables.update(parametros)
    
    return variables
