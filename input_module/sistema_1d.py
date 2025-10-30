"""
Módulo de entrada de datos para sistemas 1D
"""

EJEMPLOS_1D = {
    "Decaimiento Exponencial": {
        "funcion": "-x",
        "descripcion": "Sistema lineal simple: dx/dt = -x",
        "xlim": (-3, 3),
        "t_span": (0, 5),
        "x0_iniciales": [-2, -1, 0, 1, 2]
    },
    "Crecimiento Logístico": {
        "funcion": "x*(1-x)",
        "descripcion": "Modelo logístico: dx/dt = x(1-x)",
        "xlim": (-0.5, 1.5),
        "t_span": (0, 10),
        "x0_iniciales": [-0.5, 0.2, 0.5, 0.8, 1.5]
    },
    "Bistabilidad (Pitchfork)": {
        "funcion": "x - x**3",
        "descripcion": "Sistema con bifurcación pitchfork: dx/dt = x - x³",
        "xlim": (-2, 2),
        "t_span": (0, 10),
        "x0_iniciales": [-1.5, -0.5, 0, 0.5, 1.5]
    },
    "Oscilador Amortiguado": {
        "funcion": "-x - 0.5*x**3",
        "descripcion": "Amortiguamiento no lineal: dx/dt = -x - 0.5x³",
        "xlim": (-3, 3),
        "t_span": (0, 10),
        "x0_iniciales": [-2.5, -1, 0, 1, 2.5]
    },
    "Modelo de von Bertalanffy": {
        "funcion": "x**(2/3) - x",
        "descripcion": "Crecimiento biológico: dx/dt = x^(2/3) - x",
        "xlim": (-0.5, 2),
        "t_span": (0, 10),
        "x0_iniciales": [0.1, 0.5, 1, 1.5]
    },
    "Sistema Cúbico Simétrico": {
        "funcion": "-x**3",
        "descripcion": "Amortiguamiento cúbico puro: dx/dt = -x³",
        "xlim": (-2, 2),
        "t_span": (0, 10),
        "x0_iniciales": [-1.5, -0.5, 0.5, 1.5]
    }
}


def obtener_nombres_ejemplos_1d() -> list:
    """Retorna lista de nombres de ejemplos disponibles"""
    return list(EJEMPLOS_1D.keys())


def obtener_ejemplo_1d(nombre: str) -> dict:
    """Retorna un ejemplo específico"""
    return EJEMPLOS_1D.get(nombre)


def validar_funcion_entrada(entrada: str) -> bool:
    """Valida que la entrada sea una expresión válida"""
    try:
        import sympy as sp
        x = sp.Symbol('x')
        sp.sympify(entrada, locals={'x': x})
        return True
    except:
        return False
