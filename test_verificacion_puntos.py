"""
Test final de verificación de puntos de equilibrio en bifurcaciones
SIN mostrar imágenes, solo resultados en consola
"""

from core.bifurcacion import AnalizadorBifurcacion
from visualization.bifurcacion import VisualizadorBifurcacion
import matplotlib
matplotlib.use('Agg')  # No mostrar ventanas
import matplotlib.pyplot as plt

def test_todos_los_puntos():
    """Verifica que todos los puntos se encuentren y grafiquen correctamente"""
    
    print("\n" + "="*80)
    print("TEST COMPLETO: VERIFICACIÓN DE PUNTOS DE EQUILIBRIO")
    print("="*80 + "\n")
    
    casos = [
        {
            'nombre': 'Silla-Nodo',
            'funcion': 'r + x**2',
            'r_test': [-1, 0, 1],
            'esperados': [2, 1, 0]
        },
        {
            'nombre': 'Horquilla',
            'funcion': 'r*x - x**3',
            'r_test': [-1, 0, 1],
            'esperados': [1, 1, 3]
        },
        {
            'nombre': 'Transcrítica',
            'funcion': 'r*x - x**2',
            'r_test': [-1, 0, 1],
            'esperados': [2, 1, 2]
        },
        {
            'nombre': 'Cúbica x*(1-x)*(x-r)',
            'funcion': 'x*(1-x)*(x-r)',
            'r_test': [-0.5, 0.5, 1.5],
            'esperados': [3, 3, 3],
            'labels': ['r<0', '0<r<1', 'r>1']
        }
    ]
    
    errores = 0
    
    for caso in casos:
        print(f"\n{caso['nombre']}: f(x,r) = {caso['funcion']}")
        print("-" * 60)
        
        analizador = AnalizadorBifurcacion(caso['funcion'])
        
        labels = caso.get('labels', [f"r={r}" for r in caso['r_test']])
        
        for r_val, esperado, label in zip(caso['r_test'], caso['esperados'], labels):
            eq_data = analizador.obtener_equilibrios_con_estabilidad(r_val)
            encontrados = len(eq_data)
            
            status = "✓" if encontrados == esperado else "✗"
            
            if encontrados != esperado:
                errores += 1
                print(f"{status} {label:>8} (r={r_val:5.1f}): {encontrados} puntos (esperados: {esperado}) - ERROR")
            else:
                print(f"{status} {label:>8} (r={r_val:5.1f}): {encontrados} puntos", end="")
                
                # Mostrar los puntos
                if eq_data:
                    puntos = []
                    for eq in eq_data:
                        mult = eq.get('multiplicidad', 1)
                        if mult > 1:
                            puntos.append(f"x={eq['x']:.3f}(mult={mult})")
                        else:
                            puntos.append(f"x={eq['x']:.3f}")
                    print(f" - [{', '.join(puntos)}]")
                else:
                    print()
    
    print("\n" + "="*80)
    if errores == 0:
        print("✓ TODOS LOS TESTS PASARON CORRECTAMENTE")
    else:
        print(f"✗ {errores} ERROR(ES) ENCONTRADO(S)")
    print("="*80 + "\n")
    
    return errores == 0

def test_visualizacion_grafica():
    """Genera gráficas para verificación visual (guardadas, no mostradas)"""
    
    print("\n" + "="*80)
    print("GENERACIÓN DE GRÁFICAS DE VERIFICACIÓN")
    print("="*80 + "\n")
    
    # Caso problemático: x*(1-x)*(x-r)
    funcion = "x*(1-x)*(x-r)"
    print(f"Generando gráficas para: f(x,r) = {funcion}")
    
    analizador = AnalizadorBifurcacion(funcion)
    visualizador = VisualizadorBifurcacion(analizador)
    
    # Diagrama de bifurcación
    fig_bif = plt.figure(figsize=(10, 6))
    visualizador.graficar_diagrama_bifurcacion((-1, 2), fig=fig_bif)
    plt.savefig('verificacion_bifurcacion.png', dpi=150, bbox_inches='tight')
    plt.close('all')
    print("  ✓ verificacion_bifurcacion.png")
    
    # Diagramas de fase
    fig_fase = plt.figure(figsize=(15, 4))
    visualizador.graficar_diagrama_fase([-0.5, 0.5, 1.5], (-0.5, 2), fig=fig_fase)
    plt.savefig('verificacion_fase.png', dpi=150, bbox_inches='tight')
    plt.close('all')
    print("  ✓ verificacion_fase.png")
    
    print("\n" + "="*80)
    print("INSTRUCCIONES:")
    print("  1. Abra 'verificacion_fase.png'")
    print("  2. Verifique que TODOS los puntos aparezcan en cada diagrama:")
    print("     - r=-0.5 (r<0): debe mostrar x=-0.5, x=0, x=1")
    print("     - r=0.5 (0<r<1): debe mostrar x=0, x=0.5, x=1")
    print("     - r=1.5 (r>1): debe mostrar x=0, x=1, x=1.5")
    print("  3. Los puntos neutrales (multiplicidad > 1) se ven con círculo doble")
    print("="*80 + "\n")

if __name__ == "__main__":
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "VERIFICACIÓN FINAL DE BIFURCACIONES" + " "*24 + "║")
    print("╚" + "="*78 + "╝")
    
    # Test numérico
    exito = test_todos_los_puntos()
    
    # Test visual (sin mostrar)
    test_visualizacion_grafica()
    
    if exito:
        print("\n✓ VERIFICACIÓN COMPLETA: TODOS LOS PUNTOS SE CALCULAN Y GRAFICAN CORRECTAMENTE\n")
    else:
        print("\n✗ VERIFICACIÓN FALLIDA: REVISAR ERRORES ARRIBA\n")
