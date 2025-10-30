"""
Ejemplos predefinidos de bifurcaciones
"""

EXAMPLES = {
    'Silla-Nodo': {
        'function': 'r + x**2',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': 'Bifurcación Silla-Nodo: Dos equilibrios (uno estable, uno inestable) colisionan y desaparecen.'
    },
    'Tridente Supercrítico': {
        'function': 'r*x - x**3',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': 'Bifurcación Tridente Supercrítica: Un equilibrio estable se vuelve inestable y nacen dos nuevos equilibrios estables.'
    },
    'Tridente Subcrítico': {
        'function': 'r*x + x**3',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': 'Bifurcación Tridente Subcrítica: Un equilibrio estable se vuelve inestable y desaparecen dos equilibrios inestables.'
    },
    'Transcrítica': {
        'function': 'r*x - x**2',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': 'Bifurcación Transcrítica: Dos equilibrios intercambian estabilidad al cruzarse.'
    }
}


def get_example_names():
    """Retorna lista de nombres de ejemplos"""
    return list(EXAMPLES.keys())


def get_example(name: str):
    """Retorna datos de un ejemplo específico"""
    return EXAMPLES.get(name, None)
