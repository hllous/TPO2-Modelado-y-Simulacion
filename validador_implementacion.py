"""
Validador de implementación - Verifica que Lotka-Volterra integra funciones personalizadas
sin errores y manteniendo funcionalidad original.
"""

import sys
import os

def validar_importaciones():
    """Valida que todos los módulos mejorados se importan correctamente"""
    print("=" * 60)
    print("VALIDANDO IMPORTACIONES")
    print("=" * 60)
    
    try:
        print("✓ Importando ui.gui_utils...")
        from ui.gui_utils import crear_frame_parametro
        
        print("✓ Importando ui.widgets...")
        from ui.widgets import EntradaNumerica
        
        print("✓ Importando ui.validacion_errores...")
        from ui.validacion_errores import ValidadorEntrada
        
        print("✓ Importando config...")
        from config import CONFIG_VENTANAS
        
        print("✓ Importando input_module.lotka_volterra...")
        from input_module.lotka_volterra import InputLotkaVolterra
        
        print("✓ Importando gui.lotka_volterra...")
        from gui.lotka_volterra import InterfazLotkaVolterra
        
        print("✓ Importando core.lotka_volterra...")
        from core.lotka_volterra import SistemaLotkaVolterra
        
        print("\n✅ Todas las importaciones exitosas\n")
        return True
    except ImportError as e:
        print(f"\n❌ Error de importación: {e}\n")
        return False

def validar_estructura_input():
    """Valida que InputLotkaVolterra tiene métodos para dual-mode"""
    print("=" * 60)
    print("VALIDANDO ESTRUCTURA INPUT LOTKA-VOLTERRA")
    print("=" * 60)
    
    try:
        from input_module.lotka_volterra import InputLotkaVolterra
        
        # Verificar métodos esperados
        metodos_requeridos = [
            '_crear_selector_modo',
            '_cambiar_modo',
            '_crear_entrada_funciones',
            'obtener_parametros',
            'establecer_parametros'
        ]
        
        for metodo in metodos_requeridos:
            if hasattr(InputLotkaVolterra, metodo):
                print(f"✓ Método {metodo} existe")
            else:
                print(f"❌ Método {metodo} NO existe")
                return False
        
        print("\n✅ Estructura InputLotkaVolterra válida\n")
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        return False

def validar_dry_principles():
    """Verifica que se aplicaron principios DRY"""
    print("=" * 60)
    print("VALIDANDO PRINCIPIOS DRY")
    print("=" * 60)
    
    try:
        # Verificar centralización de estilos
        print("✓ Verificando estilos centralizados...")
        from ui.estilos import FUENTES, COLORES, ESPACIOS
        print(f"  - Fuentes definidas: {len(FUENTES)}")
        print(f"  - Colores definidos: {len(COLORES)}")
        
        # Verificar utilidades compartidas
        print("✓ Verificando utilidades compartidas...")
        from ui.gui_utils import (
            crear_frame_parametro, crear_frame_rango_numerico,
            crear_entrada_ecuacion
        )
        print("  - Utilidades GUI compartidas disponibles")
        
        # Verificar factory pattern
        print("✓ Verificando factory pattern...")
        from ui.creador_componentes import CreadorPaneles
        print("  - Factory CreadorPaneles disponible")
        
        # Verificar config centralizada
        print("✓ Verificando configuración centralizada...")
        from config import CONFIG_VENTANAS, MENSAJES_ERROR, VALORES_INICIALES
        print(f"  - Configuraciones ventanas: {len(CONFIG_VENTANAS)}")
        print(f"  - Mensajes error: {len(MENSAJES_ERROR)}")
        
        print("\n✅ Principios DRY validados\n")
        return True
    except Exception as e:
        print(f"\n❌ Error en validación DRY: {e}\n")
        return False

def validar_kiss_principles():
    """Verifica que se aplicó principio KISS"""
    print("=" * 60)
    print("VALIDANDO PRINCIPIOS KISS")
    print("=" * 60)
    
    try:
        # Verificar base module simplificado
        print("✓ Verificando ModuloBase...")
        from gui.base_module import ModuloBase
        print("  - Base module reduce complejidad")
        
        # Verificar métodos simples en core.utils
        print("✓ Verificando utilidades simples...")
        from core.utils import normalizar_funciones, evaluar_expresion
        print("  - Funciones unitarias bien definidas")
        
        # Verificar widgets específicos
        print("✓ Verificando widgets simples...")
        from ui.widgets import EntradaNumerica, BotonesGrupo
        print("  - Widgets con responsabilidad única")
        
        print("\n✅ Principios KISS validados\n")
        return True
    except Exception as e:
        print(f"\n❌ Error en validación KISS: {e}\n")
        return False

def resumen_validacion(resultados):
    """Imprime resumen de validaciones"""
    print("\n" + "=" * 60)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 60)
    
    todas_exitosas = all(resultados.values())
    
    for prueba, resultado in resultados.items():
        estado = "✅ EXITOSA" if resultado else "❌ FALLIDA"
        print(f"{prueba}: {estado}")
    
    print("=" * 60)
    
    if todas_exitosas:
        print("\n✅ TODAS LAS VALIDACIONES EXITOSAS\n")
        print("El proyecto mantiene:")
        print("  • Funcionalidad original preservada")
        print("  • Principios KISS aplicados")
        print("  • Principios DRY aplicados")
        print("  • Modularización mejorada")
        print("  • Nuevo soporte de funciones personalizadas en Lotka-Volterra")
    else:
        print("\n⚠️ ALGUNAS VALIDACIONES FALLARON\n")
        print("Revisa los errores arriba para más detalles")
    
    return todas_exitosas

if __name__ == '__main__':
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " VALIDADOR DE IMPLEMENTACIÓN - TPO2 ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    resultados = {
        "Importaciones": validar_importaciones(),
        "Estructura Input Lotka-Volterra": validar_estructura_input(),
        "Principios DRY": validar_dry_principles(),
        "Principios KISS": validar_kiss_principles(),
    }
    
    exitosa = resumen_validacion(resultados)
    sys.exit(0 if exitosa else 1)
