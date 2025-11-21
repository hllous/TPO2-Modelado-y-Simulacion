"""
Script de prueba para la funcionalidad de soluciones particulares
Demuestra cómo calcular soluciones particulares con condiciones iniciales
"""

import numpy as np
from core.sistema import SistemaDinamico2D


def test_solucion_particular_centro():
    """Prueba solución particular para un centro (f1=y, f2=-x)"""
    print("=" * 80)
    print("TEST 1: Centro (f₁ = y, f₂ = -x)")
    print("=" * 80)
    
    # Crear sistema
    funcion = {
        'f1': 'y',
        'f2': '-x',
        'es_lineal': True
    }
    sistema = SistemaDinamico2D(funcion_personalizada=funcion)
    
    # Calcular solución general
    sol_general = sistema.obtener_soluciones_parametricas()
    print("\n✓ Solución General:")
    print(f"  x(t) = {sol_general['solucion_general']['x']}")
    print(f"  y(t) = {sol_general['solucion_general']['y']}")
    
    # Calcular solución particular con x(0)=1, y(0)=0
    print("\n✓ Condiciones Iniciales: x(0) = 1, y(0) = 0")
    sol_particular = sistema.calcular_solucion_particular(1, 0)
    
    if sol_particular['es_valido']:
        print(f"\n✓ Constantes calculadas:")
        print(f"  c₁ = {sol_particular['c1']:.4f}")
        print(f"  c₂ = {sol_particular['c2']:.4f}")
        
        print(f"\n✓ Solución Particular:")
        print(f"  x(t) = {sol_particular['x_particular']}")
        print(f"  y(t) = {sol_particular['y_particular']}")
        
        # Verificar que la solución cumple las condiciones iniciales
        import sympy as sp
        t = sp.Symbol('t', real=True, positive=True)
        x_expr = sol_particular['sympy_expr']['x']
        y_expr = sol_particular['sympy_expr']['y']
        
        x_en_0 = float(x_expr.subs(t, 0))
        y_en_0 = float(y_expr.subs(t, 0))
        
        print(f"\n✓ Verificación:")
        print(f"  x(0) = {x_en_0:.6f} (esperado: 1.0)")
        print(f"  y(0) = {y_en_0:.6f} (esperado: 0.0)")
        
        if abs(x_en_0 - 1.0) < 1e-6 and abs(y_en_0 - 0.0) < 1e-6:
            print("  ✅ ¡Verificación exitosa!")
        else:
            print("  ❌ Error en la verificación")
    else:
        print(f"❌ Error: {sol_particular['mensaje']}")
    
    print()


def test_solucion_particular_nodo_estable():
    """Prueba solución particular para un nodo estable"""
    print("=" * 80)
    print("TEST 2: Nodo Estable (f₁ = -x, f₂ = -2*y)")
    print("=" * 80)
    
    # Crear sistema
    funcion = {
        'f1': '-x',
        'f2': '-2*y',
        'es_lineal': True
    }
    sistema = SistemaDinamico2D(funcion_personalizada=funcion)
    
    # Calcular solución general
    sol_general = sistema.obtener_soluciones_parametricas()
    print("\n✓ Solución General:")
    print(f"  x(t) = {sol_general['solucion_general']['x']}")
    print(f"  y(t) = {sol_general['solucion_general']['y']}")
    
    # Calcular solución particular con x(0)=2, y(0)=3
    print("\n✓ Condiciones Iniciales: x(0) = 2, y(0) = 3")
    sol_particular = sistema.calcular_solucion_particular(2, 3)
    
    if sol_particular['es_valido']:
        print(f"\n✓ Constantes calculadas:")
        print(f"  c₁ = {sol_particular['c1']:.4f}")
        print(f"  c₂ = {sol_particular['c2']:.4f}")
        
        print(f"\n✓ Solución Particular:")
        print(f"  x(t) = {sol_particular['x_particular']}")
        print(f"  y(t) = {sol_particular['y_particular']}")
        
        # Verificar condiciones iniciales
        import sympy as sp
        t = sp.Symbol('t', real=True, positive=True)
        x_expr = sol_particular['sympy_expr']['x']
        y_expr = sol_particular['sympy_expr']['y']
        
        x_en_0 = float(x_expr.subs(t, 0))
        y_en_0 = float(y_expr.subs(t, 0))
        
        print(f"\n✓ Verificación:")
        print(f"  x(0) = {x_en_0:.6f} (esperado: 2.0)")
        print(f"  y(0) = {y_en_0:.6f} (esperado: 3.0)")
        
        if abs(x_en_0 - 2.0) < 1e-6 and abs(y_en_0 - 3.0) < 1e-6:
            print("  ✅ ¡Verificación exitosa!")
        else:
            print("  ❌ Error en la verificación")
    else:
        print(f"❌ Error: {sol_particular['mensaje']}")
    
    print()


def test_solucion_particular_espiral():
    """Prueba solución particular para una espiral estable"""
    print("=" * 80)
    print("TEST 3: Espiral Estable (f₁ = -x + 2*y, f₂ = -2*x - y)")
    print("=" * 80)
    
    # Crear sistema
    funcion = {
        'f1': '-x + 2*y',
        'f2': '-2*x - y',
        'es_lineal': True
    }
    sistema = SistemaDinamico2D(funcion_personalizada=funcion)
    
    # Calcular solución general
    sol_general = sistema.obtener_soluciones_parametricas()
    print("\n✓ Solución General:")
    print(f"  Tipo: {sol_general['tipo']}")
    print(f"  x(t) = {sol_general['solucion_general']['x']}")
    print(f"  y(t) = {sol_general['solucion_general']['y']}")
    
    # Calcular solución particular con x(0)=1, y(0)=1
    print("\n✓ Condiciones Iniciales: x(0) = 1, y(0) = 1")
    sol_particular = sistema.calcular_solucion_particular(1, 1)
    
    if sol_particular['es_valido']:
        print(f"\n✓ Constantes calculadas:")
        c1 = sol_particular['c1']
        c2 = sol_particular['c2']
        
        if isinstance(c1, complex):
            print(f"  c₁ = {c1.real:.4f} + {c1.imag:.4f}i")
        else:
            print(f"  c₁ = {c1:.4f}")
        
        if isinstance(c2, complex):
            print(f"  c₂ = {c2.real:.4f} + {c2.imag:.4f}i")
        else:
            print(f"  c₂ = {c2:.4f}")
        
        print(f"\n✓ Solución Particular:")
        print(f"  x(t) = {sol_particular['x_particular']}")
        print(f"  y(t) = {sol_particular['y_particular']}")
        
        # Verificar condiciones iniciales
        import sympy as sp
        t = sp.Symbol('t', real=True, positive=True)
        x_expr = sol_particular['sympy_expr']['x']
        y_expr = sol_particular['sympy_expr']['y']
        
        x_en_0 = float(complex(x_expr.subs(t, 0)).real)
        y_en_0 = float(complex(y_expr.subs(t, 0)).real)
        
        print(f"\n✓ Verificación:")
        print(f"  x(0) = {x_en_0:.6f} (esperado: 1.0)")
        print(f"  y(0) = {y_en_0:.6f} (esperado: 1.0)")
        
        if abs(x_en_0 - 1.0) < 1e-6 and abs(y_en_0 - 1.0) < 1e-6:
            print("  ✅ ¡Verificación exitosa!")
        else:
            print("  ❌ Error en la verificación")
    else:
        print(f"❌ Error: {sol_particular['mensaje']}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("PRUEBA DE SOLUCIONES PARTICULARES CON CONDICIONES INICIALES")
    print("=" * 80 + "\n")
    
    test_solucion_particular_centro()
    test_solucion_particular_nodo_estable()
    test_solucion_particular_espiral()
    
    print("=" * 80)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 80)
