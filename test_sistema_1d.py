"""
Prueba del módulo de sistemas no lineales 1D
"""

from core.sistema_1d import SistemaDinamico1D
from visualization.sistema_1d import VisualizadorSistema1D
from input_module.sistema_1d import obtener_nombres_ejemplos_1d, obtener_ejemplo_1d
import matplotlib.pyplot as plt


def prueba_sistema_1d():
    """Prueba el sistema 1D"""
    print("="*50)
    print("PRUEBA DE SISTEMAS NO LINEALES 1D")
    print("="*50)
    
    # Cargar un ejemplo
    nombre_ejemplo = "Crecimiento Logístico"
    ejemplo = obtener_ejemplo_1d(nombre_ejemplo)
    
    print(f"\nEjemplo: {nombre_ejemplo}")
    print(f"Función: {ejemplo['funcion']}")
    print(f"Descripción: {ejemplo['descripcion']}")
    
    # Crear sistema
    sistema = SistemaDinamico1D(ejemplo['funcion'])
    print("\n" + "="*50)
    print("ANÁLISIS MATEMÁTICO")
    print("="*50)
    
    # Encontrar equilibrios
    xlim = ejemplo['xlim']
    equilibrios = sistema.encontrar_equilibrios(xlim)
    print(f"\nPuntos de Equilibrio en [{xlim[0]}, {xlim[1]}]:")
    
    for i, x_eq in enumerate(equilibrios, 1):
        estab = sistema.clasificar_estabilidad(x_eq)
        print(f"  x*_{i} = {x_eq:.6f} - {estab.upper()}")
    
    # Crear visualizador
    visualizador = VisualizadorSistema1D(sistema)
    
    # Crear figura con subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Campo de fase
    print("\nGenerando gráficos...")
    fig1 = plt.figure(figsize=(7, 5))
    visualizador.graficar_campo_fase(xlim, fig1)
    
    # Trayectorias
    fig2 = plt.figure(figsize=(10, 5))
    x0_values = ejemplo['x0_iniciales']
    t_span = ejemplo['t_span']
    visualizador.graficar_espacio_fase_tiempo(x0_values, t_span, fig2)
    
    print("✓ Gráficos generados exitosamente")
    print("\nPrueba completada exitosamente!")


if __name__ == "__main__":
    prueba_sistema_1d()
