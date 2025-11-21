"""
Test para verificar la detección y visualización de ciclos límite
"""

import numpy as np
import matplotlib.pyplot as plt
from core.sistema import SistemaDinamico2D
from visualization.grapher import Grapher

def test_ciclo_limite():
    """Prueba el sistema con ciclo límite: x*(1-x²-y²), y*(1-x²-y²)"""
    
    print("="*60)
    print("TEST: DETECCIÓN Y VISUALIZACIÓN DE CICLO LÍMITE")
    print("="*60)
    
    # Crear sistema con ciclo límite
    print("\n1. Creando sistema: dx/dt = x*(1-x²-y²), dy/dt = y*(1-x²-y²)")
    sistema = SistemaDinamico2D(
        funcion_personalizada={
            'f1': 'x*(1 - x**2 - y**2)',
            'f2': 'y*(1 - x**2 - y**2)',
            'es_lineal': False
        }
    )
    
    # Buscar puntos de equilibrio
    print("\n2. Buscando puntos de equilibrio...")
    puntos_eq = sistema.encontrar_puntos_equilibrio(xlim=(-2, 2), ylim=(-2, 2))
    print(f"   Puntos encontrados: {len(puntos_eq)}")
    for i, (x, y) in enumerate(puntos_eq, 1):
        print(f"   Punto {i}: ({x:.4f}, {y:.4f})")
    
    # Verificar detección de ciclo límite
    print("\n3. Verificando detección de ciclo límite...")
    if hasattr(sistema, 'ciclo_limite') and sistema.ciclo_limite:
        print("   ✓ Ciclo límite detectado!")
        print(f"   Tipo: {sistema.ciclo_limite['tipo']}")
        print(f"   Radio: {sistema.ciclo_limite['radio']:.4f}")
        print(f"   Ecuación: {sistema.ciclo_limite['ecuacion']}")
    else:
        print("   ✗ No se detectó ciclo límite")
    
    # Crear visualización
    print("\n4. Creando visualización...")
    fig, ax = plt.subplots(figsize=(10, 10))
    
    grapher = Grapher(sistema)
    grapher.crear_grafica(ax, xlim=(-2, 2), ylim=(-2, 2))
    
    # Agregar título descriptivo
    ax.set_title('Sistema con Ciclo Límite\ndx/dt = x(1-x²-y²), dy/dt = y(1-x²-y²)', 
                fontsize=14, fontweight='bold')
    
    # Agregar algunas trayectorias
    print("\n5. Agregando trayectorias...")
    condiciones_iniciales = [
        (0.3, 0.3),   # Dentro del círculo
        (1.5, 0.5),   # Fuera del círculo
        (0.1, 0.1),   # Cerca del origen
    ]
    
    for x0, y0 in condiciones_iniciales:
        t, trayectoria = sistema.resolver_temporal([x0, y0], t_max=10, num_puntos=1000)
        ax.plot(trayectoria[:, 0], trayectoria[:, 1], 'b-', 
               linewidth=1.5, alpha=0.6)
        ax.plot(x0, y0, 'go', markersize=8, markeredgecolor='darkgreen', 
               markeredgewidth=1.5)
    
    plt.tight_layout()
    plt.savefig('test_ciclo_limite.png', dpi=150, bbox_inches='tight')
    print("\n   ✓ Gráfica guardada como 'test_ciclo_limite.png'")
    
    plt.show()
    
    print("\n" + "="*60)
    print("TEST COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    test_ciclo_limite()
