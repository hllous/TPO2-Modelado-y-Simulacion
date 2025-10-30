"""
Ejemplos predefinidos de sistemas dinámicos
Organizados en dos columnas con descripciones útiles
"""

EJEMPLOS_LINEALES = {
    'nodo_estable': {
        'nombre': 'Nodo Estable',
        'matriz': [[-1, 0], [0, -2]],
        'descripcion': 'Ambos autovalores negativos - Las trayectorias convergen al origen',
        'columna': 0
    },
    'nodo_inestable': {
        'nombre': 'Nodo Inestable',
        'matriz': [[1, 0], [0, 2]],
        'descripcion': 'Ambos autovalores positivos - Las trayectorias divergen del origen',
        'columna': 1
    },
    'punto_silla': {
        'nombre': 'Punto Silla',
        'matriz': [[1, 0], [0, -1]],
        'descripcion': 'Autovalores de signos opuestos - Estable en una dirección, inestable en otra',
        'columna': 0
    },
    'espiral_estable': {
        'nombre': 'Espiral Estable',
        'matriz': [[-0.5, 1], [-1, -0.5]],
        'descripcion': 'Autovalores complejos con parte real negativa - Espiral que converge',
        'columna': 1
    },
    'espiral_inestable': {
        'nombre': 'Espiral Inestable',
        'matriz': [[0.5, 1], [-1, 0.5]],
        'descripcion': 'Autovalores complejos con parte real positiva - Espiral que diverge',
        'columna': 0
    },
    'centro': {
        'nombre': 'Centro',
        'matriz': [[0, 1], [-1, 0]],
        'descripcion': 'Autovalores imaginarios puros - Órbitas cerradas (oscilación pura)',
        'columna': 1
    },
    'nodo_degenerado': {
        'nombre': 'Nodo Degenerado',
        'matriz': [[-1, 1], [0, -1]],
        'descripcion': 'Autovalor repetido - Transición entre nodo y espiral',
        'columna': 0
    }
}

EJEMPLOS_NO_LINEALES = {
    'pendulo': {
        'nombre': 'Péndulo Simple',
        'f1': 'x2',
        'f2': '-sin(x1)',
        'descripcion': 'Péndulo no forzado: caos homoclínico y órbitas periódicas',
        'columna': 0
    },
    'van_der_pol': {
        'nombre': 'Van der Pol',
        'f1': 'x2',
        'f2': 'x2*(1-x1**2)-x1',
        'descripcion': 'Oscilador con amortiguación no lineal: ciclo límite atractor',
        'columna': 1
    },
    'lotka_volterra': {
        'nombre': 'Lotka-Volterra',
        'f1': 'x1*(1-x2)',
        'f2': '-x2*(1-x1)',
        'descripcion': 'Modelo depredador-presa: órbitas cerradas, no es atractor',
        'columna': 0
    },
    'duffing': {
        'nombre': 'Duffing',
        'f1': 'x2',
        'f2': 'x1 - x1**3',
        'descripcion': 'Oscilador con rigidez no lineal: dos pozos de potencial',
        'columna': 1
    },
    'logistico': {
        'nombre': 'Sistema Logístico',
        'f1': 'x1*(1-x1)',
        'f2': 'x2*(1-x2)',
        'descripcion': 'Crecimiento limitado: línea de equilibrio estable',
        'columna': 0
    },
    'prey_simple': {
        'nombre': 'Presa Simple',
        'f1': 'x1-x1*x2',
        'f2': '-x2+x1*x2',
        'descripcion': 'Modelo simple presa-depredador: centro con perturbaciones',
        'columna': 1
    }
}

