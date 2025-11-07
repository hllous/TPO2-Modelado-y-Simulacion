"""
Configuración centralizada de la aplicación
Elimina duplicación de constantes y configuraciones
"""

from ui.estilos import COLORES, FUENTES, ESPACIOS

# Configuración de ventanas
CONFIG_VENTANAS = {
    'principal': {
        'titulo': 'Sistemas Dinámicos - Aplicación Principal',
        'ancho': 1000,
        'alto': 650,
        'resizable': True
    },
    '2d': {
        'titulo': 'Sistemas Dinámicos 2D - Análisis Completo',
        'ancho': 1400,
        'alto': 800,
        'resizable': True
    },
    '1d': {
        'titulo': 'Sistemas Dinámicos 1D - Análisis No Lineal',
        'ancho': 1400,
        'alto': 800,
        'resizable': True
    },
    'bifurcacion': {
        'titulo': 'Análisis de Bifurcaciones 1D',
        'ancho': 1400,
        'alto': 800,
        'resizable': True
    },
    'hamilton': {
        'titulo': 'Análisis de Sistemas Hamiltonianos',
        'ancho': 1200,
        'alto': 800,
        'resizable': True
    },
    'lotka_volterra': {
        'titulo': 'Lotka-Volterra: Sistema Depredador-Presa',
        'ancho': 1400,
        'alto': 900,
        'resizable': True
    }
}

# Configuración de gráficos
CONFIG_GRAFICOS = {
    'figura_tamano': (8, 6),
    'dpi': 100,
    'estilo': 'default',
    'colores_fondo': '#f0f0f0',
    'colores_linea_default': '#2196F3',
    'colores_puntos': '#ff9800',
    'colores_estable': '#4CAF50',
    'colores_inestable': '#f44336'
}

# Configuración de validación
CONFIG_VALIDACION = {
    'precision_decimal': 6,
    'max_iteraciones': 10000,
    'tolerance_convergencia': 1e-6,
    'min_valor': -1e10,
    'max_valor': 1e10
}

# Mensajes de error estándar
MENSAJES_ERROR = {
    'entrada_vacia': 'Por favor complete todos los campos requeridos',
    'numero_invalido': 'Ingrese un número válido',
    'rango_invalido': 'El valor mínimo debe ser menor que el máximo',
    'matriz_invalida': 'La matriz debe ser 2x2 con valores numéricos',
    'funcion_invalida': 'La expresión de la función no es válida',
    'parametros_invalidos': 'Los parámetros ingresados no son válidos',
    'error_calculo': 'Error durante el cálculo',
    'error_grafico': 'Error al generar la gráfica'
}

# Mensajes de éxito
MENSAJES_EXITO = {
    'analisis_completo': 'Análisis completado con éxito',
    'sistema_actualizado': 'Sistema actualizado correctamente',
    'datos_guardados': 'Datos guardados correctamente',
    'grafica_generada': 'Gráfica generada correctamente'
}

# Rangos por defecto
RANGOS_DEFECTO = {
    '2d_x': (-5, 5),
    '2d_y': (-5, 5),
    '1d': (-5, 5),
    'bifurcacion_r': (-2, 2),
    'bifurcacion_x': (-3, 3),
    'tiempo': (0, 10)
}

# Valores iniciales por defecto
VALORES_INICIALES = {
    'matriz_2d': [[-1, 0], [0, -2]],
    'funcion_1d': '-x + x**3',
    'funcion_bifurcacion': 'r + x**2',
    'funcion_hamilton_u': '-x',
    'funcion_hamilton_v': '-y',
    'lotka_volterra_alpha': 1.0,
    'lotka_volterra_beta': 0.5,
    'lotka_volterra_gamma': 0.5,
    'lotka_volterra_delta': 0.5
}

# Configuración de fuentes para componentes
FUENTES_COMPONENTES = {
    'entrada': FUENTES['monoespaciada_pequena'],
    'etiqueta': FUENTES['normal'],
    'titulo_panel': FUENTES['titulo_seccion'],
    'resultado': FUENTES['monoespaciada'],
    'botones': FUENTES['normal_bold']
}

def obtener_config_ventana(tipo):
    """Obtiene configuración de ventana por tipo"""
    return CONFIG_VENTANAS.get(tipo, CONFIG_VENTANAS['principal'])

def obtener_mensaje_error(clave):
    """Obtiene mensaje de error estándar"""
    return MENSAJES_ERROR.get(clave, 'Error desconocido')

def obtener_mensaje_exito(clave):
    """Obtiene mensaje de éxito estándar"""
    return MENSAJES_EXITO.get(clave, 'Operación completada')
