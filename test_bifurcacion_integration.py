"""
Tests de integración para bifurcaciones
Verifican que el módulo integrado funciona correctamente
"""

import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.bifurcacion import AnalizadorBifurcacion
from visualization.bifurcacion import VisualizadorBifurcacion
from input_module.bifurcacion import obtener_ejemplo_bifurcacion
import numpy as np


def test_silla_nodo():
    """Test bifurcación Silla-Nodo: r + x**2"""
    print("\n" + "="*60)
    print("TEST: Bifurcación Silla-Nodo (r + x**2)")
    print("="*60)
    
    analizador = AnalizadorBifurcacion("r + x**2")
    
    print("\nPara r = -1:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(-1)
    print(f"  Equilibrios: {eq_data}")
    assert len(eq_data) == 2, "Debe haber 2 equilibrios en r=-1"
    
    print("\nPara r = 0:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(0)
    print(f"  Equilibrios: {eq_data}")
    assert len(eq_data) == 1, "Debe haber 1 equilibrio en r=0"
    
    print("\nPara r = 1:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(1)
    print(f"  Equilibrios: {eq_data}")
    assert len(eq_data) == 0, "No debe haber equilibrios reales en r=1"
    
    print("\n✓ Test Silla-Nodo PASÓ")
    return analizador


def test_tridente_supercritico():
    """Test bifurcación Tridente Supercrítica: r*x - x**3"""
    print("\n" + "="*60)
    print("TEST: Bifurcación Tridente Supercrítica (r*x - x**3)")
    print("="*60)
    
    analizador = AnalizadorBifurcacion("r*x - x**3")
    
    print("\nPara r = -1:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(-1)
    print(f"  Equilibrios: {eq_data}")
    assert len(eq_data) == 1, "Debe haber 1 equilibrio en r=-1"
    
    print("\nPara r = 0:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(0)
    print(f"  Equilibrios: {eq_data}")
    assert len(eq_data) == 1, "Debe haber 1 equilibrio en r=0"
    
    print("\nPara r = 1:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(1)
    print(f"  Equilibrios: {eq_data}")
    assert len(eq_data) == 3, "Debe haber 3 equilibrios en r=1"
    
    print("\n✓ Test Tridente Supercrítico PASÓ")
    return analizador


def test_transcrities():
    """Test bifurcación Transcrítica: r*x - x**2"""
    print("\n" + "="*60)
    print("TEST: Bifurcación Transcrítica (r*x - x**2)")
    print("="*60)
    
    analizador = AnalizadorBifurcacion("r*x - x**2")
    
    print("\nPara r = -1:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(-1)
    print(f"  Equilibrios: {eq_data}")
    
    print("\nPara r = 0:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(0)
    print(f"  Equilibrios: {eq_data}")
    
    print("\nPara r = 1:")
    eq_data = analizador.obtener_equilibrios_con_estabilidad(1)
    print(f"  Equilibrios: {eq_data}")
    
    print("\n✓ Test Transcrítica PASÓ")
    return analizador


def test_ejemplos():
    """Test que los ejemplos se cargan correctamente"""
    print("\n" + "="*60)
    print("TEST: Carga de ejemplos predefinidos")
    print("="*60)
    
    ejemplos = [
        'Silla-Nodo',
        'Tridente Supercrítico',
        'Tridente Subcrítico',
        'Transcrítica'
    ]
    
    for nombre in ejemplos:
        ejemplo = obtener_ejemplo_bifurcacion(nombre)
        assert ejemplo is not None, f"No se encontró el ejemplo {nombre}"
        print(f"\n✓ Ejemplo '{nombre}' cargado correctamente")
        print(f"  Función: {ejemplo['funcion']}")
        print(f"  Descripción: {ejemplo['descripcion']}")
    
    print("\n✓ Test de ejemplos PASÓ")


def test_visualizacion():
    """Test que la visualización se genera correctamente"""
    print("\n" + "="*60)
    print("TEST: Generación de datos de visualización")
    print("="*60)
    
    analizador = AnalizadorBifurcacion("r + x**2")
    visualizador = VisualizadorBifurcacion(analizador)
    
    # Generar datos de bifurcación
    data = analizador.generar_datos_bifurcacion((-2, 2), num_points=50)
    print(f"\n✓ Datos de bifurcación generados")
    print(f"  Puntos estables: {len(data['estable']['r'])}")
    print(f"  Puntos inestables: {len(data['inestable']['r'])}")
    
    # Evaluar función
    x_vals = np.linspace(-3, 3, 100)
    f_vals = analizador.evaluar_funcion(x_vals, 0.5)
    print(f"\n✓ Función evaluada en {len(x_vals)} puntos")
    print(f"  Rango de valores: [{np.min(f_vals):.4f}, {np.max(f_vals):.4f}]")
    
    print("\n✓ Test de visualización PASÓ")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# PRUEBAS DE INTEGRACIÓN - BIFURCACIONES")
    print("#"*60)
    
    try:
        test_silla_nodo()
        test_tridente_supercritico()
        test_transcrities()
        test_ejemplos()
        test_visualizacion()
        
        print("\n" + "#"*60)
        print("# TODOS LOS TESTS PASARON ✓")
        print("#"*60)
        
    except Exception as e:
        print(f"\n✗ ERROR EN TESTS: {e}")
        import traceback
        traceback.print_exc()
