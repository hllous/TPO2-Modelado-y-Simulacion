#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para verificar que las soluciones paramétricas usan símbolos matemáticos
"""

import sys
sys.path.append('.')

from core.sistema import SistemaDinamico2D

def test_centro_simbolico():
    """Verifica que un Centro genere soluciones con sqrt(2)/2 en lugar de 0.7071"""
    print("=" * 80)
    print("TEST: Centro con símbolos matemáticos")
    print("=" * 80)
    
    # Sistema: f1 = y, f2 = -x
    # Jacobiano: [[0, 1], [-1, 0]]
    # Autovalores: ±i
    # Autovectores: [1/sqrt(2), ±i/sqrt(2)]
    
    funcion_personalizada = {
        'f1': 'y',
        'f2': '-x',
        'es_lineal': True
    }
    sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    if not resultado['es_valido']:
        print(f"\n❌ ERROR: {resultado.get('mensaje', 'Sin mensaje de error')}")
        return False
    
    print(f"\n✓ Resultado válido: {resultado['es_valido']}")
    print(f"✓ Tipo: {resultado['tipo']}")
    
    latex_x = resultado['latex']['x']
    latex_y = resultado['latex']['y']
    
    print(f"\nLaTeX x(t):")
    print(latex_x)
    print(f"\nLaTeX y(t):")
    print(latex_y)
    
    # Verificaciones
    print("\n" + "=" * 80)
    print("VERIFICACIONES:")
    print("=" * 80)
    
    tiene_sqrt = 'sqrt' in latex_x or '\\sqrt' in latex_x
    tiene_frac = 'frac' in latex_x or '\\frac' in latex_x
    tiene_numerico = '0.7071' in latex_x or '0.7071' in latex_y
    
    print(f"✓ Tiene símbol de raíz (sqrt): {tiene_sqrt}")
    print(f"✓ Tiene fracciones (frac): {tiene_frac}")
    print(f"✗ NO debe tener decimales (0.7071): {not tiene_numerico}")
    
    if tiene_sqrt and not tiene_numerico:
        print("\n✅ ÉXITO: Las expresiones usan símbolos matemáticos correctamente")
        return True
    else:
        print("\n❌ ERROR: Las expresiones aún usan decimales en lugar de símbolos")
        return False

def test_nodo_estable_simbolico():
    """Verifica un nodo estable con raíces"""
    print("\n" + "=" * 80)
    print("TEST: Nodo Estable con símbolos matemáticos")
    print("=" * 80)
    
    # Sistema: f1 = -2x, f2 = -y
    # Jacobiano: [[-2, 0], [0, -1]]
    # Autovalores: -2, -1
    
    funcion_personalizada = {
        'f1': '-2*x',
        'f2': '-y',
        'es_lineal': True
    }
    sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    if not resultado['es_valido']:
        print(f"\n❌ ERROR: {resultado.get('mensaje', 'Sin mensaje de error')}")
        return False
    
    print(f"\n✓ Resultado válido: {resultado['es_valido']}")
    print(f"✓ Tipo: {resultado['tipo']}")
    
    latex_x = resultado['latex']['x']
    latex_y = resultado['latex']['y']
    
    print(f"\nLaTeX x(t):")
    print(latex_x)
    print(f"\nLaTeX y(t):")
    print(latex_y)
    
    return True

if __name__ == '__main__':
    print("\n🧪 PRUEBAS DE SOLUCIONES SIMBÓLICAS\n")
    
    exito_centro = test_centro_simbolico()
    exito_nodo = test_nodo_estable_simbolico()
    
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Centro: {'✅ PASS' if exito_centro else '❌ FAIL'}")
    print(f"Nodo Estable: {'✅ PASS' if exito_nodo else '❌ FAIL'}")
    
    if exito_centro and exito_nodo:
        print("\n✅ TODOS LOS TESTS PASARON")
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
