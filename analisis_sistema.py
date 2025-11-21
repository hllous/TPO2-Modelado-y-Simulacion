#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Análisis del sistema x*(1-x²-y²), y*(1-x²-y²)
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Definir sistema simbólicamente
x, y = sp.symbols('x y', real=True)
f1 = x*(1 - x**2 - y**2)
f2 = y*(1 - x**2 - y**2)

print("="*80)
print("ANÁLISIS DEL SISTEMA NO LINEAL")
print("="*80)
print(f"\nSistema:")
print(f"  dx/dt = f₁(x,y) = {f1}")
print(f"  dy/dt = f₂(x,y) = {f2}")

# Factorizar para entender mejor
print(f"\nFactorización:")
print(f"  f₁ = x·(1 - x² - y²)")
print(f"  f₂ = y·(1 - x² - y²)")
print(f"\nAmbas funciones tienen el factor común: (1 - x² - y²)")

# Encontrar puntos de equilibrio
print("\n" + "="*80)
print("PUNTOS DE EQUILIBRIO")
print("="*80)

print("\nResolviendo f₁ = 0 Y f₂ = 0:")

# Resolver el sistema
sols = sp.solve([f1, f2], [x, y])

print(f"\nNúmero de soluciones: {len(sols)}")
print("\nPuntos encontrados:")

for i, sol in enumerate(sols, 1):
    print(f"\n{i}. x = {sol[0]}")
    print(f"   y = {sol[1]}")
    
    # Intentar evaluar numéricamente
    try:
        x_val = float(sol[0])
        y_val = float(sol[1])
        print(f"   → Numérico: ({x_val:.6f}, {y_val:.6f})")
    except:
        print(f"   → Solución simbólica/paramétrica")

# Análisis geométrico
print("\n" + "="*80)
print("ANÁLISIS GEOMÉTRICO")
print("="*80)

print("\nPara que f₁ = 0:")
print("  x·(1 - x² - y²) = 0")
print("  → x = 0  O  1 - x² - y² = 0")
print("  → x = 0  O  x² + y² = 1 (círculo unitario)")

print("\nPara que f₂ = 0:")
print("  y·(1 - x² - y²) = 0")
print("  → y = 0  O  1 - x² - y² = 0")
print("  → y = 0  O  x² + y² = 1 (círculo unitario)")

print("\nPuntos de equilibrio REALES:")
print("  1. Intersección de x=0 e y=0:")
print("     → (0, 0) - ORIGEN")
print("\n  2. Círculo unitario x² + y² = 1:")
print("     → INFINITOS puntos en el círculo")
print("     → Cada punto (x, y) con x² + y² = 1 es equilibrio")

# Visualización
print("\n" + "="*80)
print("INTERPRETACIÓN")
print("="*80)

print("\n¿Por qué aparecen muchos puntos?")
print("  SymPy intenta resolver algebraicamente y puede devolver:")
print("  - Soluciones paramétricas")
print("  - Casos especiales")
print("  - Representaciones simbólicas del círculo")

print("\nLa REALIDAD FÍSICA del sistema:")
print("  ✓ 1 punto de equilibrio: (0, 0)")
print("  ✓ 1 CURVA de equilibrios: círculo x² + y² = 1")
print("     (infinitos puntos)")

print("\n" + "="*80)
print("COMPORTAMIENTO DEL SISTEMA")
print("="*80)

print("\nAnálisis del campo vectorial:")
print("  • Dentro del círculo (x² + y² < 1):")
print("    → 1 - x² - y² > 0")
print("    → f₁ = x·(positivo) y f₂ = y·(positivo)")
print("    → Las trayectorias se ALEJAN del origen")

print("\n  • Fuera del círculo (x² + y² > 1):")
print("    → 1 - x² - y² < 0")
print("    → f₁ = x·(negativo) y f₂ = y·(negativo)")
print("    → Las trayectorias van HACIA el origen")

print("\n  • En el círculo (x² + y² = 1):")
print("    → 1 - x² - y² = 0")
print("    → f₁ = 0 y f₂ = 0")
print("    → EQUILIBRIO ESTABLE (ciclo límite)")

print("\n" + "="*80)
print("CONCLUSIÓN")
print("="*80)
print("\nEste sistema tiene:")
print("  • Un PUNTO de equilibrio inestable en (0,0)")
print("  • Un CICLO LÍMITE estable en el círculo unitario")
print("\nEs un ejemplo clásico de sistema con CICLO LÍMITE.")
print("Todas las trayectorias tienden al círculo x² + y² = 1.")
print("="*80)
