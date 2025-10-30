"""
Ejemplos predefinidos de sistemas dinámicos
"""

EJEMPLOS_LINEALES = {
    'nodo_estable': {
        'nombre': 'Nodo Estable',
        'matriz': [[-1, 0], [0, -2]],
        'descripcion': 'Ambos autovalores negativos'
    },
    'nodo_inestable': {
        'nombre': 'Nodo Inestable',
        'matriz': [[1, 0], [0, 2]],
        'descripcion': 'Ambos autovalores positivos'
    },
    'punto_silla': {
        'nombre': 'Punto Silla',
        'matriz': [[1, 0], [0, -1]],
        'descripcion': 'Autovalores de signos opuestos'
    },
    'espiral_estable': {
        'nombre': 'Espiral Estable',
        'matriz': [[-0.5, 1], [-1, -0.5]],
        'descripcion': 'Autovalores complejos, parte real negativa'
    },
    'espiral_inestable': {
        'nombre': 'Espiral Inestable',
        'matriz': [[0.5, 1], [-1, 0.5]],
        'descripcion': 'Autovalores complejos, parte real positiva'
    },
    'centro': {
        'nombre': 'Centro',
        'matriz': [[0, 1], [-1, 0]],
        'descripcion': 'Autovalores imaginarios puros'
    },
    'nodo_degenerado': {
        'nombre': 'Nodo Degenerado',
        'matriz': [[-1, 1], [0, -1]],
        'descripcion': 'Autovalor repetido'
    }
}

EJEMPLOS_NO_LINEALES = {
    'pendulo': {
        'nombre': 'Péndulo',
        'f1': 'y',
        'f2': '-sin(x)',
        'descripcion': 'Péndulo no forzado'
    },
    'van_der_pol': {
        'nombre': 'Van der Pol',
        'f1': 'y',
        'f2': 'y*(1-x**2)-x',
        'descripcion': 'Oscilador con amortiguación no lineal'
    },
    'lotka_volterra': {
        'nombre': 'Lotka-Volterra',
        'f1': 'x*(1-y)',
        'f2': '-y*(1-x)',
        'descripcion': 'Modelo depredador-presa'
    },
    'duffing': {
        'nombre': 'Duffing',
        'f1': 'y',
        'f2': 'x - x**3',
        'descripcion': 'Oscilador con rigidez no lineal'
    }
}


def get_ejemplo(clave, tipo='lineal'):
    """
    Obtiene un ejemplo predefinido
    
    Parámetros:
    - clave: identificador del ejemplo
    - tipo: 'lineal' o 'no_lineal'
    
    Retorna: dict con datos del ejemplo o None si no existe
    """
    ejemplos = EJEMPLOS_LINEALES if tipo == 'lineal' else EJEMPLOS_NO_LINEALES
    return ejemplos.get(clave)


def listar_ejemplos(tipo='lineal'):
    """
    Lista todos los ejemplos disponibles
    
    Retorna: lista de (clave, nombre)
    """
    ejemplos = EJEMPLOS_LINEALES if tipo == 'lineal' else EJEMPLOS_NO_LINEALES
    return [(clave, datos['nombre']) for clave, datos in ejemplos.items()]
