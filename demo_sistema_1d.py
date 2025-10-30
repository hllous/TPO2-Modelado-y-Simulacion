"""
Demostración completa del módulo de sistemas no lineales 1D
Muestra todas las funcionalidades sin interfaz gráfica
"""

from core.sistema_1d import SistemaDinamico1D
from visualization.sistema_1d import VisualizadorSistema1D
from input_module.sistema_1d import obtener_nombres_ejemplos_1d, obtener_ejemplo_1d


def analizar_ejemplo(nombre_ejemplo):
    """Analiza un ejemplo específico"""
    print("\n" + "="*60)
    print(f"EJEMPLO: {nombre_ejemplo}")
    print("="*60)
    
    ejemplo = obtener_ejemplo_1d(nombre_ejemplo)
    print(f"\nFunción: dx/dt = {ejemplo['funcion']}")
    print(f"Descripción: {ejemplo['descripcion']}")
    
    # Crear sistema
    sistema = SistemaDinamico1D(ejemplo['funcion'])
    
    # Encontrar equilibrios
    xlim = ejemplo['xlim']
    equilibrios = sistema.encontrar_equilibrios(xlim)
    
    print(f"\nRango de análisis: x ∈ [{xlim[0]}, {xlim[1]}]")
    print("\nPuntos de Equilibrio:")
    
    if equilibrios:
        for i, x_eq in enumerate(equilibrios, 1):
            estab = sistema.clasificar_estabilidad(x_eq)
            simbolo = "•" if estab == "estable" else "○" if estab == "inestable" else "•"
            print(f"  {simbolo} x*_{i} = {x_eq:10.6f}  [{estab.upper()}]")
    else:
        print("  No se encontraron puntos de equilibrio")
    
    # Evaluar función en puntos específicos
    print("\nValores de la función en puntos críticos:")
    import numpy as np
    test_points = [-2, -1, -0.5, 0, 0.5, 1, 1.5, 2]
    for x_test in test_points:
        if xlim[0] <= x_test <= xlim[1]:
            f_vals = sistema.evaluar_funcion(np.array([x_test]))
            df_vals = sistema.evaluar_derivada(np.array([x_test]))
            f_val = float(f_vals[0]) if hasattr(f_vals, '__len__') else float(f_vals)
            df_val = float(df_vals[0]) if hasattr(df_vals, '__len__') else float(df_vals)
            print(f"  f({x_test:5.1f}) = {f_val:8.4f}  |  f'({x_test:5.1f}) = {df_val:8.4f}")
    
    return sistema


def main():
    """Función principal"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " MÓDULO DE SISTEMAS NO LINEALES 1D ".center(58) + "║")
    print("║" + " Demostración de Funcionalidades ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    # Mostrar ejemplos disponibles
    ejemplos = obtener_nombres_ejemplos_1d()
    print(f"\nEjemplos disponibles ({len(ejemplos)}):")
    for i, nombre in enumerate(ejemplos, 1):
        print(f"  {i}. {nombre}")
    
    # Analizar algunos ejemplos
    ejemplos_demo = [
        "Decaimiento Exponencial",
        "Crecimiento Logístico",
        "Bistabilidad (Pitchfork)"
    ]
    
    sistemas = {}
    for nombre in ejemplos_demo:
        sistema = analizar_ejemplo(nombre)
        sistemas[nombre] = sistema
    
    # Demostración de integración numérica
    print("\n" + "="*60)
    print("INTEGRACIÓN NUMÉRICA")
    print("="*60)
    
    sistema = sistemas["Crecimiento Logístico"]
    print("\nTrayectorias para el modelo logístico (dx/dt = x(1-x)):")
    print("Condición inicial → Comportamiento Asintótico")
    
    x0_values = [-0.5, 0.2, 0.5, 0.8, 1.5]
    for x0 in x0_values:
        t, x_traj = sistema.integrar_trayectoria(x0, (0, 20), 1000)
        x_final = x_traj[-1]
        print(f"  x₀ = {x0:5.1f}  →  x(∞) ≈ {x_final:7.4f}")
    
    # Análisis de estabilidad
    print("\n" + "="*60)
    print("ANÁLISIS DE ESTABILIDAD")
    print("="*60)
    
    import numpy as np
    print("\nEstabilidad local en torno a equilibrios:")
    
    for nombre, sistema in sistemas.items():
        print(f"\n{nombre}:")
        equilibrios = sistema.encontrar_equilibrios((-5, 5))
        for x_eq in equilibrios:
            df_vals = sistema.evaluar_derivada(np.array([x_eq]))
            derivada = float(df_vals[0]) if hasattr(df_vals, '__len__') else float(df_vals)
            estab = "ESTABLE" if derivada < 0 else "INESTABLE" if derivada > 0 else "NEUTRAL"
            print(f"  En x* = {x_eq:7.4f}: f'(x*) = {derivada:8.4f} → {estab}")
    
    print("\n" + "="*60)
    print("✓ Demostración completada exitosamente")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
