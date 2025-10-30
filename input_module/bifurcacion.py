"""
Ejemplos predefinidos de bifurcaciones
"""

EJEMPLOS_BIFURCACION = {
    'Silla-Nodo': {
        'funcion': 'r + x**2',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_valores': [-1, 0, 1],
        'descripcion': 'Silla-Nodo: Dos equilibrios colisionan y desaparecen.'
    },
    'Tridente Supercrítico': {
        'funcion': 'r*x - x**3',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_valores': [-1, 0, 1],
        'descripcion': 'Tridente Supercrítico: Equilibrio estable se vuelve inestable y nacen dos nuevos estables.'
    },
    'Tridente Subcrítico': {
        'funcion': 'r*x + x**3',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_valores': [-1, 0, 1],
        'descripcion': 'Tridente Subcrítico: Equilibrio estable se vuelve inestable y desaparecen dos inestables.'
    },
    'Transcrítica': {
        'funcion': 'r*x - x**2',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_valores': [-1, 0, 1],
        'descripcion': 'Transcrítica: Dos equilibrios intercambian estabilidad.'
    }
}


def obtener_nombres_ejemplos_bifurcacion():
    """Retorna lista de nombres de ejemplos"""
    return list(EJEMPLOS_BIFURCACION.keys())


def obtener_ejemplo_bifurcacion(nombre: str):
    """Retorna datos de un ejemplo específico"""
    return EJEMPLOS_BIFURCACION.get(nombre, None)
