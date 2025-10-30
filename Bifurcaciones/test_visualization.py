"""
Test de visualización para verificar que los gráficos se generan correctamente
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import BifurcationAnalyzer
from src.visualization import BifurcationVisualizer
import matplotlib.pyplot as plt

def test_pitchfork_supercritical_visualization():
    """Test visualización Tridente Supercrítico"""
    print("="*60)
    print("Test Visualización: Tridente Supercrítico (r*x - x**3)")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r*x - x**3")
    visualizer = BifurcationVisualizer(analyzer)
    
    # Crear figura para diagrama de bifurcación
    fig1 = plt.figure(figsize=(10, 6))
    visualizer.plot_bifurcation_diagram((-2, 2), fig1)
    
    # Crear figura para diagramas de fase
    fig2 = plt.figure(figsize=(15, 4))
    visualizer.plot_phase_diagram([-1, 0, 1], (-3, 3), fig2)
    
    # Guardar figuras
    fig1.savefig('test_bifurcation_supercritical.png', dpi=100, bbox_inches='tight')
    fig2.savefig('test_phase_supercritical.png', dpi=100, bbox_inches='tight')
    
    print("✓ Gráficos guardados:")
    print("  - test_bifurcation_supercritical.png")
    print("  - test_phase_supercritical.png")
    
    plt.close('all')

def test_pitchfork_subcritical_visualization():
    """Test visualización Tridente Subcrítico"""
    print("\n" + "="*60)
    print("Test Visualización: Tridente Subcrítico (r*x + x**3)")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r*x + x**3")
    visualizer = BifurcationVisualizer(analyzer)
    
    # Crear figura para diagrama de bifurcación
    fig1 = plt.figure(figsize=(10, 6))
    visualizer.plot_bifurcation_diagram((-2, 2), fig1)
    
    # Crear figura para diagramas de fase
    fig2 = plt.figure(figsize=(15, 4))
    visualizer.plot_phase_diagram([-1, 0, 1], (-3, 3), fig2)
    
    # Guardar figuras
    fig1.savefig('test_bifurcation_subcritical.png', dpi=100, bbox_inches='tight')
    fig2.savefig('test_phase_subcritical.png', dpi=100, bbox_inches='tight')
    
    print("✓ Gráficos guardados:")
    print("  - test_bifurcation_subcritical.png")
    print("  - test_phase_subcritical.png")
    
    plt.close('all')

def test_saddle_node_visualization():
    """Test visualización Silla-Nodo"""
    print("\n" + "="*60)
    print("Test Visualización: Silla-Nodo (r + x**2)")
    print("="*60)
    
    analyzer = BifurcationAnalyzer("r + x**2")
    visualizer = BifurcationVisualizer(analyzer)
    
    # Crear figura para diagrama de bifurcación
    fig1 = plt.figure(figsize=(10, 6))
    visualizer.plot_bifurcation_diagram((-2, 2), fig1)
    
    # Crear figura para diagramas de fase
    fig2 = plt.figure(figsize=(15, 4))
    visualizer.plot_phase_diagram([-1, 0, 1], (-3, 3), fig2)
    
    # Guardar figuras
    fig1.savefig('test_bifurcation_saddle_node.png', dpi=100, bbox_inches='tight')
    fig2.savefig('test_phase_saddle_node.png', dpi=100, bbox_inches='tight')
    
    print("✓ Gráficos guardados:")
    print("  - test_bifurcation_saddle_node.png")
    print("  - test_phase_saddle_node.png")
    
    plt.close('all')

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("  TEST DE VISUALIZACIÓN")
    print("#"*60 + "\n")
    
    try:
        test_pitchfork_supercritical_visualization()
        test_pitchfork_subcritical_visualization()
        test_saddle_node_visualization()
        
        print("\n" + "#"*60)
        print("  ✓ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("#"*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR EN TESTS: {e}")
        import traceback
        traceback.print_exc()
