"""
Ejemplos predefinidos de sistemas dinámicos
Organizados en dos columnas
"""

EJEMPLOS_LINEALES = {
    'nodo_estable': {
        'nombre': 'Nodo Estable',
        'matriz': [[-1, 0], [0, -2]],
        'descripcion': 'Ambos autovalores negativos',
        'columna': 0
    },
    'nodo_inestable': {
        'nombre': 'Nodo Inestable',
        'matriz': [[1, 0], [0, 2]],
        'descripcion': 'Ambos autovalores positivos',
        'columna': 1
    },
    'punto_silla': {
        'nombre': 'Punto Silla',
        'matriz': [[1, 0], [0, -1]],
        'descripcion': 'Autovalores de signos opuestos',
        'columna': 0
    },
    'espiral_estable': {
        'nombre': 'Espiral Estable',
        'matriz': [[-0.5, 1], [-1, -0.5]],
        'descripcion': 'Autovalores complejos, parte real negativa',
        'columna': 1
    },
    'espiral_inestable': {
        'nombre': 'Espiral Inestable',
        'matriz': [[0.5, 1], [-1, 0.5]],
        'descripcion': 'Autovalores complejos, parte real positiva',
        'columna': 0
    },
    'centro': {
        'nombre': 'Centro',
        'matriz': [[0, 1], [-1, 0]],
        'descripcion': 'Autovalores imaginarios puros',
        'columna': 1
    },
    'nodo_degenerado': {
        'nombre': 'Nodo Degenerado',
        'matriz': [[-1, 1], [0, -1]],
        'descripcion': 'Autovalor repetido',
        'columna': 0
    }
}

EJEMPLOS_NO_LINEALES = {
    'pendulo': {
        'nombre': 'Péndulo',
        'f1': 'y',
        'f2': '-sin(x)',
        'descripcion': 'Péndulo no forzado',
        'columna': 0
    },
    'van_der_pol': {
        'nombre': 'Van der Pol',
        'f1': 'y',
        'f2': 'y*(1-x**2)-x',
        'descripcion': 'Oscilador con amortiguación no lineal',
        'columna': 1
    },
    'lotka_volterra': {
        'nombre': 'Lotka-Volterra',
        'f1': 'x*(1-y)',
        'f2': '-y*(1-x)',
        'descripcion': 'Modelo depredador-presa',
        'columna': 0
    },
    'duffing': {
        'nombre': 'Duffing',
        'f1': 'y',
        'f2': 'x - x**3',
        'descripcion': 'Oscilador con rigidez no lineal',
        'columna': 1
    }
}

