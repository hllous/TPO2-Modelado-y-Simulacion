"""
Tests para verificar las soluciones paramétricas x(t) e y(t)
"""

import numpy as np
import sympy as sp
from core.sistema import SistemaDinamico2D


def test_centro():
    """Test para un centro (autovalores imaginarios puros)"""
    print("\n" + "="*60)
    print("TEST 1: Centro (autovalores imaginarios puros)")
    print("="*60)
    
    # Matriz del sistema centro
    matriz = [[0, 1], [-1, 0]]
    sistema = SistemaDinamico2D(matriz=matriz)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Matriz A:")
    print(f"  [0   1]")
    print(f"  [-1  0]")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    print(f"\nLaTeX x(t):")
    print(f"  {resultado['latex']['x']}")
    print(f"\nLaTeX y(t):")
    print(f"  {resultado['latex']['y']}")
    
    # Verificar que los autovalores son ±i
    assert abs(resultado['autovalores'][0].imag - 1.0) < 0.01, "Autovalor 1 debería ser i"
    assert abs(resultado['autovalores'][1].imag + 1.0) < 0.01, "Autovalor 2 debería ser -i"
    
    print("\n✓ Test pasado: Centro")
    return True


def test_nodo_estable():
    """Test para un nodo estable (autovalores reales negativos)"""
    print("\n" + "="*60)
    print("TEST 2: Nodo Estable (autovalores reales negativos)")
    print("="*60)
    
    matriz = [[-1, 0], [0, -2]]
    sistema = SistemaDinamico2D(matriz=matriz)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Matriz A:")
    print(f"  [-1  0]")
    print(f"  [0  -2]")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    print(f"\nLaTeX x(t):")
    print(f"  {resultado['latex']['x']}")
    print(f"\nLaTeX y(t):")
    print(f"  {resultado['latex']['y']}")
    
    # Verificar autovalores
    assert resultado['autovalores'][0].real < 0, "Autovalores deben ser negativos"
    assert resultado['autovalores'][1].real < 0, "Autovalores deben ser negativos"
    
    # Verificar que las soluciones contienen exp(-t) y exp(-2t)
    assert 'exp(-1.0*t)' in resultado['solucion_general']['x'] or 'exp(-t)' in resultado['solucion_general']['x']
    
    print("\n✓ Test pasado: Nodo Estable")
    return True


def test_nodo_silla():
    """Test para un nodo silla (un autovalor positivo, uno negativo)"""
    print("\n" + "="*60)
    print("TEST 3: Nodo Silla (autovalores de signos opuestos)")
    print("="*60)
    
    matriz = [[1, 0], [0, -1]]
    sistema = SistemaDinamico2D(matriz=matriz)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Matriz A:")
    print(f"  [1   0]")
    print(f"  [0  -1]")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    print(f"\nLaTeX x(t):")
    print(f"  {resultado['latex']['x']}")
    print(f"\nLaTeX y(t):")
    print(f"  {resultado['latex']['y']}")
    
    # Verificar que uno es positivo y otro negativo
    autoval_real = [resultado['autovalores'][0].real, resultado['autovalores'][1].real]
    assert any(x > 0 for x in autoval_real), "Debe haber un autovalor positivo"
    assert any(x < 0 for x in autoval_real), "Debe haber un autovalor negativo"
    
    print("\n✓ Test pasado: Nodo Silla")
    return True


def test_espiral_estable():
    """Test para una espiral estable (autovalores complejos con parte real negativa)"""
    print("\n" + "="*60)
    print("TEST 4: Espiral Estable (autovalores complejos, Re < 0)")
    print("="*60)
    
    matriz = [[-1, 2], [-2, -1]]
    sistema = SistemaDinamico2D(matriz=matriz)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    print(f"Matriz A:")
    print(f"  [-1  2]")
    print(f"  [-2 -1]")
    print(f"\nAutovalores: {resultado['autovalores']}")
    print(f"Tipo: {resultado['tipo']}")
    print(f"\nSolución x(t):")
    print(f"  {resultado['solucion_general']['x']}")
    print(f"\nSolución y(t):")
    print(f"  {resultado['solucion_general']['y']}")
    print(f"\nLaTeX x(t):")
    print(f"  {resultado['latex']['x']}")
    print(f"\nLaTeX y(t):")
    print(f"  {resultado['latex']['y']}")
    
    # Verificar que son complejos conjugados
    λ1, λ2 = resultado['autovalores']
    assert abs(λ1.real - λ2.real) < 0.01, "Deben ser conjugados (misma parte real)"
    assert abs(λ1.imag + λ2.imag) < 0.01, "Deben ser conjugados (parte imaginaria opuesta)"
    assert λ1.real < 0, "Parte real debe ser negativa (estable)"
    
    # Verificar que las soluciones contienen sin y cos
    assert 'sin' in resultado['solucion_general']['x']
    assert 'cos' in resultado['solucion_general']['x']
    
    print("\n✓ Test pasado: Espiral Estable")
    return True


def test_precision_decimales():
    """Test para verificar que los decimales están redondeados a 4 lugares"""
    print("\n" + "="*60)
    print("TEST 5: Precisión de Decimales (4 lugares)")
    print("="*60)
    
    matriz = [[0, 1], [-1, 0]]
    sistema = SistemaDinamico2D(matriz=matriz)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    # Buscar números con más de 4 decimales
    import re
    
    def verificar_decimales(texto):
        """Verifica que no haya números con más de 4 decimales"""
        # Buscar patrones como 0.123456789
        patron = r'\d+\.(\d{5,})'
        matches = re.findall(patron, texto)
        return matches
    
    x_exceso = verificar_decimales(resultado['solucion_general']['x'])
    y_exceso = verificar_decimales(resultado['solucion_general']['y'])
    
    print(f"Solución x(t): {resultado['solucion_general']['x']}")
    print(f"Solución y(t): {resultado['solucion_general']['y']}")
    
    if x_exceso:
        print(f"\n⚠ Advertencia: Encontrados decimales con más de 4 lugares en x(t): {x_exceso}")
    if y_exceso:
        print(f"\n⚠ Advertencia: Encontrados decimales con más de 4 lugares en y(t): {y_exceso}")
    
    if not x_exceso and not y_exceso:
        print("\n✓ Test pasado: Precisión de Decimales")
        return True
    else:
        print("\n✗ Test fallido: Hay números con más de 4 decimales")
        return False


def test_latex_valido():
    """Test para verificar que el LaTeX generado es válido"""
    print("\n" + "="*60)
    print("TEST 6: Validez de LaTeX")
    print("="*60)
    
    matriz = [[-1, 2], [-2, -1]]
    sistema = SistemaDinamico2D(matriz=matriz)
    
    resultado = sistema.obtener_soluciones_parametricas()
    
    latex_x = resultado['latex']['x']
    latex_y = resultado['latex']['y']
    
    print(f"LaTeX x(t):")
    print(f"  {latex_x}")
    print(f"\nLaTeX y(t):")
    print(f"  {latex_y}")
    
    # Verificar elementos comunes de LaTeX
    elementos_esperados = ['c', 't', 'e^{', 'sin', 'cos']
    
    for elemento in elementos_esperados[:3]:  # Verificar al menos algunos elementos
        if elemento in latex_x or elemento in latex_y:
            print(f"✓ Elemento '{elemento}' encontrado")
    
    # Verificar que no hay sintaxis inválida
    invalidos = ['**', '__', 'None', 'NaN']
    for inv in invalidos:
        assert inv not in latex_x, f"LaTeX contiene sintaxis inválida: {inv}"
        assert inv not in latex_y, f"LaTeX contiene sintaxis inválida: {inv}"
    
    print("\n✓ Test pasado: LaTeX Válido")
    return True


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("EJECUTANDO TODOS LOS TESTS DE SOLUCIONES PARAMÉTRICAS")
    print("="*60)
    
    tests = [
        test_centro,
        test_nodo_estable,
        test_nodo_silla,
        test_espiral_estable,
        test_precision_decimales,
        test_latex_valido
    ]
    
    resultados = []
    for test in tests:
        try:
            resultado = test()
            resultados.append((test.__name__, resultado))
        except Exception as e:
            print(f"\n✗ Test {test.__name__} falló con error: {e}")
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
