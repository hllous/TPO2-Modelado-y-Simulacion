"""
Programa Principal - Análisis de Bifurcaciones 1D
Autor: Sistema de Análisis de Bifurcaciones
Fecha: Octubre 2025

Este programa permite analizar bifurcaciones en sistemas dinámicos 1D.

Características:
- Análisis de bifurcaciones Silla-Nodo, Tridente (Pitchfork), y Transcríticas
- Cálculo automático de puntos de equilibrio y estabilidad
- Diagramas de bifurcación
- Diagramas de fase para r < 0, r = 0, r > 0
- Interfaz gráfica intuitiva

Uso:
    python main.py

Requisitos:
    - Python 3.8+
    - numpy
    - sympy
    - matplotlib
    - tkinter (incluido en Python estándar)
"""

from gui import main

if __name__ == "__main__":
    print("="*60)
    print("  ANÁLISIS DE BIFURCACIONES 1D")
    print("="*60)
    print("\nIniciando interfaz gráfica...\n")
    print("Funciones disponibles:")
    print("  - Bifurcación Silla-Nodo")
    print("  - Bifurcación Tridente (Pitchfork)")
    print("  - Bifurcación Transcrítica")
    print("\nFormato de entrada: use sintaxis Python")
    print("  Ejemplos: r + x**2, r*x - x**3, r*x - x**2")
    print("="*60 + "\n")
    
    main()
