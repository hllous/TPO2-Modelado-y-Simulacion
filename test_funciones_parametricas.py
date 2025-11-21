"""
Test para verificar que las soluciones paramétricas funcionan con entrada de funciones
"""

from core.sistema import SistemaDinamico2D


def test_centro_con_funciones():
    """Test de centro usando funciones en vez de matriz"""
    print("\n" + "="*60)
    print("TEST: Centro con funciones (f₁=y, f₂=-x)")
    print("="*60)
    
    # Crear sistema con funciones
    funcion_personalizada = {
        'f1': 'y',
        'f2': '-x',
        'es_lineal': True
    }
    
    sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Funciones:")
    print(f"  f₁(x,y) = y")
    print(f"  f₂(x,y) = -x")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    
    assert resultado['es_valido'], "Resultado debe ser válido"
    assert 'cos' in resultado['solucion_general']['x'], "Debe contener cos"
    assert 'sin' in resultado['solucion_general']['y'], "Debe contener sin"
    
    print("\n✓ Test pasado: Centro con funciones")
    return True


def test_nodo_estable_con_funciones():
    """Test de nodo estable usando funciones"""
    print("\n" + "="*60)
    print("TEST: Nodo Estable con funciones (f₁=-x, f₂=-2*y)")
    print("="*60)
    
    funcion_personalizada = {
        'f1': '-x',
        'f2': '-2*y',
        'es_lineal': True
    }
    
    sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Funciones:")
    print(f"  f₁(x,y) = -x")
    print(f"  f₂(x,y) = -2*y")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    
    assert resultado['es_valido'], "Resultado debe ser válido"
    assert 'exp(-t)' in resultado['solucion_general']['x'] or 'exp(-1.0*t)' in resultado['solucion_general']['x'], "x(t) debe tener exp(-t)"
    assert 'exp(-2.0*t)' in resultado['solucion_general']['y'] or 'exp(-2*t)' in resultado['solucion_general']['y'], "y(t) debe tener exp(-2t)"
    
    print("\n✓ Test pasado: Nodo Estable con funciones")
    return True


def test_espiral_con_funciones():
    """Test de espiral usando funciones acopladas"""
    print("\n" + "="*60)
    print("TEST: Espiral con funciones (f₁=-x+2*y, f₂=-2*x-y)")
    print("="*60)
    
    funcion_personalizada = {
        'f1': '-x + 2*y',
        'f2': '-2*x - y',
        'es_lineal': True
    }
    
    sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Funciones:")
    print(f"  f₁(x,y) = -x + 2*y")
    print(f"  f₂(x,y) = -2*x - y")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    
    assert resultado['es_valido'], "Resultado debe ser válido"
    assert resultado['tipo'] == 'Autovalores complejos conjugados', "Debe ser espiral"
    assert 'sin' in resultado['solucion_general']['x'], "Debe contener sin"
    assert 'cos' in resultado['solucion_general']['x'], "Debe contener cos"
    
    print("\n✓ Test pasado: Espiral con funciones")
    return True


def test_nodo_silla_con_funciones():
    """Test de nodo silla usando funciones"""
    print("\n" + "="*60)
    print("TEST: Nodo Silla con funciones (f₁=x, f₂=-y)")
    print("="*60)
    
    funcion_personalizada = {
        'f1': 'x',
        'f2': '-y',
        'es_lineal': True
    }
    
    sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Funciones:")
    print(f"  f₁(x,y) = x")
    print(f"  f₂(x,y) = -y")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    
    assert resultado['es_valido'], "Resultado debe ser válido"
    assert 'exp(t)' in resultado['solucion_general']['x'] or 'exp(1.0*t)' in resultado['solucion_general']['x'], "x(t) debe tener exp(t)"
    assert 'exp(-t)' in resultado['solucion_general']['y'] or 'exp(-1.0*t)' in resultado['solucion_general']['y'], "y(t) debe tener exp(-t)"
    
    print("\n✓ Test pasado: Nodo Silla con funciones")
    return True


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("TESTS DE SOLUCIONES PARAMÉTRICAS CON FUNCIONES")
    print("="*60)
    
    tests = [
        test_centro_con_funciones,
        test_nodo_estable_con_funciones,
        test_espiral_con_funciones,
        test_nodo_silla_con_funciones
    ]
    
    resultados = []
    for test in tests:
        try:
            resultado = test()
            resultados.append((test.__name__, resultado))
        except Exception as e:
            print(f"\n✗ Test {test.__name__} falló con error: {e}")
            import traceback
            traceback.print_exc()
            resultados.append((test.__name__, False))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE TESTS")
    print("="*60)
    
    pasados = sum(1 for _, r in resultados if r)
    totales = len(resultados)
    
    for nombre, resultado in resultados:
        simbolo = "✓" if resultado else "✗"
        print(f"{simbolo} {nombre}")
    
    print(f"\n{pasados}/{totales} tests pasados")
    
    if pasados == totales:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print(f"\n⚠️  {totales - pasados} test(s) fallaron")
    
    return pasados == totales


if __name__ == "__main__":
    run_all_tests()
