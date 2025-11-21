#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test específico para el sistema que preguntó el usuario
"""

import sys
sys.path.append('.')

from core.sistema import SistemaDinamico2D

def test_sistema_usuario():
    """Test del sistema f₁ = -x, f₂ = -2*y"""
    print("="*80)
    print("TEST: Sistema f₁ = -x, f₂ = -2*y")
    print("="*80)
    
    funcion_personalizada = {
        'f1': '-x',
        'f2': '-2*y',
        'es_lineal': True
    }
    
    sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"\nSistema:")
    print(f"  f₁(x,y) = -x")
    print(f"  f₂(x,y) = -2*y")
    
    print(f"\nResultado válido: {resultado['es_valido']}")
    
    if not resultado['es_valido']:
        print(f"ERROR: {resultado.get('mensaje', 'Sin mensaje')}")
        return
    
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Autovectores: {resultado['autovectores']}")
    
    print(f"\nSolución x(t):")
    print(f"  Expresión: {resultado['solucion_general']['x']}")
    print(f"  LaTeX:     {resultado['latex']['x']}")
    
    print(f"\nSolución y(t):")
    print(f"  Expresión: {resultado['solucion_general']['y']}")
    print(f"  LaTeX:     {resultado['latex']['y']}")
    
    # Verificación
    print("\n" + "="*80)
    print("VERIFICACIÓN")
    print("="*80)
    
    x_correcto = 'exp(-1' in resultado['solucion_general']['x'] or 'exp(-t)' in resultado['solucion_general']['x']
    y_correcto = 'exp(-2' in resultado['solucion_general']['y'] or 'exp(-2*t)' in resultado['solucion_general']['y']
    
    print(f"x(t) contiene e^(-t): {x_correcto}")
    print(f"y(t) contiene e^(-2t): {y_correcto}")
    
    if x_correcto and y_correcto:
        print("\n✅ SOLUCIONES CORRECTAS")
    else:
        print("\n❌ ERROR EN LAS SOLUCIONES")
        if not x_correcto:
            print("   x(t) debería ser c₁·e^(-t)")
        if not y_correcto:
            print("   y(t) debería ser c₂·e^(-2t)")

if __name__ == '__main__':
    test_sistema_usuario()
