"""
Utilidades compartidas para el sistema dinámico
Centraliza funciones reutilizables
"""

import numpy as np
import sympy as sp
from functools import lru_cache


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
    'e': np.e,
    'sinh': np.sinh,
    'cosh': np.cosh,
    'tanh': np.tanh
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
    'e': sp.E,
    'sinh': sp.sinh,
    'cosh': sp.cosh,
    'tanh': sp.tanh
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


@lru_cache(maxsize=128)
def validar_expresion_matematica(expresion):
    """
    Valida que una expresión sea matemáticamente válida
    
    Parámetros:
    - expresion: string con la expresión
    
    Retorna: (es_valida, mensaje_error)
    """
    try:
        # Normalizar
        expr_norm = normalizar_funciones(expresion)
        
        # Intentar parsear con sympy
        sp.sympify(expr_norm, locals=FUNCIONES_SYMPY)
        return True, None
    except Exception as e:
        return False, str(e)


def evaluar_expresion(expresion, variables):
    """
    Evalúa una expresión matemática de forma segura
    
    Parámetros:
    - expresion: string con la expresión
    - variables: dict con variables disponibles
    
    Retorna: resultado de la evaluación
    """
    try:
        # Crear ambiente seguro
        ambiente = {**FUNCIONES_NUMPY, **variables}
        
        # Evaluar
        return eval(normalizar_funciones(expresion), {"__builtins__": {}}, ambiente)
    except Exception as e:
        raise ValueError(f"Error al evaluar expresión: {str(e)}")


def calcular_jacobiano(funcion_f, funcion_g, punto):
    """
    Calcula jacobiano en un punto
    
    Parámetros:
    - funcion_f, funcion_g: funciones como strings
    - punto: (x, y)
    
    Retorna: matriz jacobiana 2x2
    """
    x, y = punto
    h = 1e-5
    
    # Crear variables
    vars_base = {'x': x, 'y': y, 't': 0}
    
    # Derivada parcial de f respecto a x
    fx = (evaluar_expresion(funcion_f, {**vars_base, 'x': x + h}) - 
          evaluar_expresion(funcion_f, {**vars_base, 'x': x - h})) / (2 * h)
    
    # Derivada parcial de f respecto a y
    fy = (evaluar_expresion(funcion_f, {**vars_base, 'y': y + h}) - 
          evaluar_expresion(funcion_f, {**vars_base, 'y': y - h})) / (2 * h)
    
    # Derivada parcial de g respecto a x
    gx = (evaluar_expresion(funcion_g, {**vars_base, 'x': x + h}) - 
          evaluar_expresion(funcion_g, {**vars_base, 'x': x - h})) / (2 * h)
    
    # Derivada parcial de g respecto a y
    gy = (evaluar_expresion(funcion_g, {**vars_base, 'y': y + h}) - 
          evaluar_expresion(funcion_g, {**vars_base, 'y': y - h})) / (2 * h)
    
    return np.array([[fx, fy], [gx, gy]])


def analizar_estabilidad_punto(jacobiano):
    """
    Analiza estabilidad de punto de equilibrio
    
    Parámetros:
    - jacobiano: matriz jacobiana 2x2
    
    Retorna: dict con análisis de estabilidad
    """
    eigenvalues = np.linalg.eigvals(jacobiano)
    traza = np.trace(jacobiano)
    determinante = np.linalg.det(jacobiano)
    
    # Criterios de estabilidad
    es_estable = all(np.real(e) < 0 for e in eigenvalues)
    
    return {
        'eigenvalores': eigenvalues,
        'traza': traza,
        'determinante': determinante,
        'estable': es_estable,
        'tipo': clasificar_equilibrio(eigenvalues, traza, determinante)
    }


def clasificar_equilibrio(eigenvalues, traza, determinante):
    """
    Clasifica tipo de punto de equilibrio
    
    Retorna: tipo de punto (nodo, foco, silla, etc.)
    """
    e1, e2 = eigenvalues.real, eigenvalues.imag
    
    if determinante < 0:
        return 'silla'
    elif determinante > 0:
        if traza < 0:
            return 'nodo_estable' if e1.imag == 0 else 'foco_estable'
        elif traza > 0:
            return 'nodo_inestable' if e1.imag == 0 else 'foco_inestable'
        else:
            return 'centro'
    else:
        return 'degenerate'


def generar_vector_numerico(expresion_str):
    """
    Convierte vector expresión a numpy array
    
    Parámetros:
    - expresion_str: string del vector
    
    Retorna: numpy array
    """
    try:
        # Reemplazar caracteres especiales
        expr_limpia = expresion_str.replace('[', '').replace(']', '')
        valores = [float(x.strip()) for x in expr_limpia.split(',')]
        return np.array(valores)
    except:
        return None

