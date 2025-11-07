"""
Utilidades de refactorización compartida
Consolidación de principios KISS y DRY para todo el proyecto
"""

import numpy as np


class ConfiguracionSistema:
    """Centraliza configuraciones globales reutilizables"""
    
    # Dimensiones por defecto
    TAMAÑO_VENTANA_PRINCIPAL = "1400x900"
    TAMAÑO_VENTANA_ANALISIS = (900, 700)
    
    # Tiempos y límites
    TIEMPO_INTEGRACION_DEFAULT = 100
    PUNTOS_INTEGRACION_DEFAULT = 1000
    
    # Rangos visualización
    RANGO_BUSQUEDA_DEFECTO = (-10, 10)
    
    # Precisión numérica
    TOLERANCIA_EQUILIBRIO = 0.01
    PRECISION_AUTOVALORES = 1e-10


class PatronesDRY:
    """Patrones DRY para evitar duplicación en análisis"""
    
    @staticmethod
    def formatear_seccion(titulo, contenido, nivel=1):
        """Formatea secciones de análisis de forma consistente"""
        separador = '='*50 if nivel == 1 else '-'*50
        return f"{titulo}\n{separador}\n{contenido}\n"
    
    @staticmethod
    def formatear_parametro(nombre, valor, precision=3):
        """Formatea parámetro de forma consistente"""
        if isinstance(valor, (float, np.floating)):
            return f"{nombre}: {valor:.{precision}f}"
        return f"{nombre}: {valor}"
    
    @staticmethod
    def crear_diccionario_equilibrio(punto, tipo, estabilidad):
        """Crea dict consistente para punto de equilibrio"""
        return {
            'punto': punto,
            'tipo': tipo,
            'estabilidad': estabilidad
        }


class ValidadorSistema:
    """Valida parámetros y estados del sistema"""
    
    @staticmethod
    def validar_parametros(params, rangos_esperados):
        """Valida que parámetros estén en rangos esperados"""
        for param, (min_val, max_val) in rangos_esperados.items():
            if param in params:
                valor = params[param]
                if not (min_val <= valor <= max_val):
                    return False, f"{param} fuera de rango [{min_val}, {max_val}]"
        return True, "OK"
    
    @staticmethod
    def validar_estado_inicial(estado, xlim, ylim):
        """Valida que estado inicial esté dentro de límites"""
        x, y = estado
        if not (xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]):
            return False
        return True
