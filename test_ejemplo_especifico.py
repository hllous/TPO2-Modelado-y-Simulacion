"""
Test específico para verificar x*(1-x)*(x-r)
"""

from core.bifurcacion import AnalizadorBifurcacion
from visualization.bifurcacion import VisualizadorBifurcacion
import matplotlib.pyplot as plt

def test_funcion_cubica():
    """Test para f(x,r) = x*(1-x)*(x-r)"""
    
    print("\n" + "="*80)
    print("TEST: f(x,r) = x*(1-x)*(x-r)")
    print("="*80)
    
    funcion = "x*(1-x)*(x-r)"
    print(f"\nFunción: {funcion}")
    
    analizador = AnalizadorBifurcacion(funcion)
    visualizador = VisualizadorBifurcacion(analizador)
    
    # Valores de r a probar: r<0, 0<r<1, r>1
    r_valores = [-0.5, 0.5, 1.5]
    labels = ['r < 0', '0 < r < 1', 'r > 1']
    
    print("\nPuntos de equilibrio encontrados:")
    print("-" * 80)
    
    for r_val, label in zip(r_valores, labels):
        eq_data = analizador.obtener_equilibrios_con_estabilidad(r_val)
        print(f"\n{label} (r = {r_val}): {len(eq_data)} punto(s)")
        
        if eq_data:
            for i, eq in enumerate(eq_data, 1):
                estab = eq['estabilidad'].upper()
                mult = eq.get('multiplicidad', 1)
                if mult > 1:
                    print(f"  x*_{i} = {eq['x']:8.4f}  -  {estab} (multiplicidad {mult})")
                else:
                    print(f"  x*_{i} = {eq['x']:8.4f}  -  {estab}")
        else:
            print("  No hay puntos de equilibrio reales")
    
    print("\n" + "-" * 80)
    print("\nGenerando diagrama de bifurcación...")
    
    # Diagrama de bifurcación
    fig_bif = plt.figure(figsize=(10, 6))
    visualizador.graficar_diagrama_bifurcacion((-1, 2), fig=fig_bif)
    plt.savefig('test_cubica_bifurcacion.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Diagrama guardado: test_cubica_bifurcacion.png")
    
    print("\nGenerando diagramas de fase...")
    
    # Diagramas de fase
    fig_fase = plt.figure(figsize=(15, 4))
    visualizador.graficar_diagrama_fase([-0.5, 0.5, 1.5], (-0.5, 2), fig=fig_fase)
    plt.savefig('test_cubica_fase.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Diagramas de fase guardados: test_cubica_fase.png")
    
    print("\n" + "="*80)
    print("\nVERIFICACIÓN:")
    print("  1. Los puntos de equilibrio se calculan correctamente")
    print("  2. Verifique las imágenes para asegurar que TODOS los puntos aparecen")
    print("  3. Siempre hay 3 puntos de equilibrio: x=0, x=1, x=r")
    print("  4. Rangos importantes:")
    print("     - r < 0: r está fuera del intervalo [0,1]")
    print("     - 0 < r < 1: r está entre los puntos fijos 0 y 1")
    print("     - r > 1: r está fuera del intervalo [0,1]")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_funcion_cubica()
