"""
Test final simplificado para verificar funcionalidad
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import BifurcationAnalyzer
from src.visualization import BifurcationVisualizer
from src.examples import EXAMPLES

def test_all_examples():
    """Test todos los ejemplos predefinidos"""
    print("="*70)
    print("  TEST FINAL - VERIFICACIÓN DE TODOS LOS EJEMPLOS")
    print("="*70)
    
    for name, example in EXAMPLES.items():
        print(f"\n{'='*70}")
        print(f"Ejemplo: {name}")
        print(f"Función: {example['function']}")
        print(f"{'='*70}")
        
        try:
            # Crear analizador
            analyzer = BifurcationAnalyzer(example['function'])
            
            # Probar con los tres valores de r
            for r_val, label in zip(example['r_values'], ['r < 0', 'r = 0', 'r > 0']):
                eq_data = analyzer.get_equilibria_with_stability(r_val)
                
                print(f"\n{label} (r = {r_val}):")
                if eq_data:
                    for i, eq in enumerate(eq_data, 1):
                        status = "ESTABLE" if eq['stability'] == 'stable' else "INESTABLE"
                        print(f"  x*_{i} = {eq['x']:7.4f}  ({status})")
                else:
                    print("  Sin equilibrios reales")
            
            # Test de datos de bifurcación (solo 30 puntos para velocidad)
            print(f"\nGenerando diagrama de bifurcación (30 puntos)...")
            bif_data = analyzer.generate_bifurcation_data(example['r_range'], num_points=30)
            print(f"  ✓ Puntos estables:    {len(bif_data['stable']['r'])}")
            print(f"  ✓ Puntos inestables:  {len(bif_data['unstable']['r'])}")
            
            print(f"\n✓ Ejemplo '{name}' verificado correctamente")
            
        except Exception as e:
            print(f"\n✗ ERROR en ejemplo '{name}': {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    print("\n" + "#"*70)
    print("  SUITE DE TESTS FINAL")
    print("#"*70 + "\n")
    
    success = test_all_examples()
    
    print("\n" + "#"*70)
    if success:
        print("  ✓✓✓ TODOS LOS TESTS PASARON EXITOSAMENTE ✓✓✓")
        print("\n  El programa está listo para usarse!")
        print("  Ejecuta: python main.py")
    else:
        print("  ✗✗✗ ALGUNOS TESTS FALLARON ✗✗✗")
    print("#"*70 + "\n")
