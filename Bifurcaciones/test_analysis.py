"""
Tests para verificar la funcionalidad del análisis de bifurcaciones
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import BifurcationAnalyzer
from src.visualization import BifurcationVisualizer
import numpy as np

def test_saddle_node():
    """Test bifurcación Silla-Nodo: r + x**2"""
    print("\n" + "="*60)
    print("TEST 1: Bifurcación Silla-Nodo (r + x**2)")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r + x**2")
    
    # Test para r = -1 (debe tener 2 equilibrios)
    print("\nPara r = -1:")
    equilibria = analyzer.find_equilibria(-1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(-1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 0 (debe tener 1 equilibrio)
    print("\nPara r = 0:")
    equilibria = analyzer.find_equilibria(0)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(0)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 1 (no debe tener equilibrios reales)
    print("\nPara r = 1:")
    equilibria = analyzer.find_equilibria(1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test de datos de bifurcación
    print("\nGenerando datos de bifurcación...")
    bif_data = analyzer.generate_bifurcation_data((-2, 2), num_points=100)
    print(f"  Puntos estables: {len(bif_data['stable']['r'])}")
    print(f"  Puntos inestables: {len(bif_data['unstable']['r'])}")
    
    return analyzer

def test_pitchfork_supercritical():
    """Test bifurcación Tridente Supercrítica: r*x - x**3"""
    print("\n" + "="*60)
    print("TEST 2: Bifurcación Tridente Supercrítica (r*x - x**3)")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r*x - x**3")
    
    # Test para r = -1 (debe tener 1 equilibrio estable en x=0)
    print("\nPara r = -1:")
    equilibria = analyzer.find_equilibria(-1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(-1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 0 (debe tener 1 equilibrio en x=0)
    print("\nPara r = 0:")
    equilibria = analyzer.find_equilibria(0)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(0)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 1 (debe tener 3 equilibrios: 0 inestable, ±1 estables)
    print("\nPara r = 1:")
    equilibria = analyzer.find_equilibria(1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test de datos de bifurcación
    print("\nGenerando datos de bifurcación...")
    bif_data = analyzer.generate_bifurcation_data((-2, 2), num_points=100)
    print(f"  Puntos estables: {len(bif_data['stable']['r'])}")
    print(f"  Puntos inestables: {len(bif_data['unstable']['r'])}")
    
    return analyzer

def test_pitchfork_subcritical():
    """Test bifurcación Tridente Subcrítica: r*x + x**3"""
    print("\n" + "="*60)
    print("TEST 3: Bifurcación Tridente Subcrítica (r*x + x**3)")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r*x + x**3")
    
    # Test para r = -1 (debe tener 3 equilibrios)
    print("\nPara r = -1:")
    equilibria = analyzer.find_equilibria(-1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(-1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 0 (debe tener 1 equilibrio en x=0)
    print("\nPara r = 0:")
    equilibria = analyzer.find_equilibria(0)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(0)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 1 (debe tener 1 equilibrio inestable en x=0)
    print("\nPara r = 1:")
    equilibria = analyzer.find_equilibria(1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test de datos de bifurcación
    print("\nGenerando datos de bifurcación...")
    bif_data = analyzer.generate_bifurcation_data((-2, 2), num_points=100)
    print(f"  Puntos estables: {len(bif_data['stable']['r'])}")
    print(f"  Puntos inestables: {len(bif_data['unstable']['r'])}")
    
    return analyzer

def test_transcritical():
    """Test bifurcación Transcrítica: r*x - x**2"""
    print("\n" + "="*60)
    print("TEST 4: Bifurcación Transcrítica (r*x - x**2)")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r*x - x**2")
    
    # Test para r = -1
    print("\nPara r = -1:")
    equilibria = analyzer.find_equilibria(-1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(-1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 0
    print("\nPara r = 0:")
    equilibria = analyzer.find_equilibria(0)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(0)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test para r = 1
    print("\nPara r = 1:")
    equilibria = analyzer.find_equilibria(1)
    print(f"  Equilibrios encontrados: {equilibria}")
    eq_data = analyzer.get_equilibria_with_stability(1)
    print(f"  Con estabilidad: {eq_data}")
    
    # Test de datos de bifurcación
    print("\nGenerando datos de bifurcación...")
    bif_data = analyzer.generate_bifurcation_data((-2, 2), num_points=100)
    print(f"  Puntos estables: {len(bif_data['stable']['r'])}")
    print(f"  Puntos inestables: {len(bif_data['unstable']['r'])}")
    
    return analyzer

def test_function_evaluation():
    """Test evaluación de función"""
    print("\n" + "="*60)
    print("TEST 5: Evaluación de Función")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r*x - x**3")
    
    x_vals = np.array([-2, -1, 0, 1, 2])
    r_val = 1
    
    print(f"\nEvaluando f(x, r) = r*x - x**3 para r = {r_val}")
    print(f"x valores: {x_vals}")
    
    f_vals = analyzer.evaluate_function(x_vals, r_val)
    print(f"f(x) valores: {f_vals}")
    
    # Verificar manualmente
    expected = r_val * x_vals - x_vals**3
    print(f"Esperado: {expected}")
    print(f"¿Coinciden? {np.allclose(f_vals, expected)}")

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("  SUITE DE TESTS - ANÁLISIS DE BIFURCACIONES")
    print("#"*60)
    
    try:
        test_saddle_node()
        test_pitchfork_supercritical()
        test_pitchfork_subcritical()
        test_transcritical()
        test_function_evaluation()
        
        print("\n" + "#"*60)
        print("  TESTS COMPLETADOS")
        print("#"*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR EN TESTS: {e}")
        import traceback
        traceback.print_exc()
