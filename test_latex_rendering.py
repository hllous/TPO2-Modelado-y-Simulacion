#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar el renderizado LaTeX con símbolos matemáticos
"""

import sympy as sp

# Crear símbolos
t = sp.Symbol('t', real=True, positive=True)
c1, c2 = sp.symbols('c1 c2', real=True)

# Ejemplo 1: Centro (autovalores ±i)
# Solución esperada con sqrt(2)/2 en lugar de 0.7071
x_centro = sp.sqrt(2)/2 * c1 * sp.cos(t) + sp.sqrt(2)/2 * c2 * sp.sin(t)
y_centro = -sp.sqrt(2)/2 * c1 * sp.sin(t) + sp.sqrt(2)/2 * c2 * sp.cos(t)

print("=" * 80)
print("EJEMPLO 1: CENTRO")
print("=" * 80)
print(f"\nExpresión simbólica x(t):")
print(x_centro)
print(f"\nLaTeX x(t):")
latex_x = sp.latex(x_centro)
print(latex_x)
print(f"\nExpresión simbólica y(t):")
print(y_centro)
print(f"\nLaTeX y(t):")
latex_y = sp.latex(y_centro)
print(latex_y)

# Ejemplo 2: Nodo Estable con raíces
# Autovalores: -sqrt(2), -1/sqrt(2)
lambda1 = -sp.sqrt(2)
lambda2 = -1/sp.sqrt(2)

x_nodo = c1 * sp.sqrt(2) * sp.exp(lambda1 * t) + c2 * (1/sp.sqrt(2)) * sp.exp(lambda2 * t)
y_nodo = c1 * sp.exp(lambda1 * t) + c2 * sp.exp(lambda2 * t)

print("\n" + "=" * 80)
print("EJEMPLO 2: NODO ESTABLE CON RAÍCES")
print("=" * 80)
print(f"\nExpresión simbólica x(t):")
print(x_nodo)
print(f"\nLaTeX x(t):")
latex_x_nodo = sp.latex(x_nodo)
print(latex_x_nodo)
print(f"\nExpresión simbólica y(t):")
print(y_nodo)
print(f"\nLaTeX y(t):")
latex_y_nodo = sp.latex(y_nodo)
print(latex_y_nodo)

# Ejemplo 3: Verificar que NO hay "sqrt(0.5)" sino "1/sqrt(2)"
print("\n" + "=" * 80)
print("VERIFICACIÓN: Símbolos matemáticos vs texto")
print("=" * 80)

# Versión incorrecta (numérica)
x_numerico = 0.7071 * c1 * sp.cos(1.0 * t) + 0.7071 * c2 * sp.sin(1.0 * t)
latex_numerico = sp.latex(x_numerico)
print(f"\n❌ VERSIÓN NUMÉRICA (indeseada):")
print(f"   LaTeX: {latex_numerico}")

# Versión correcta (simbólica)
x_simbolico = sp.sqrt(2)/2 * c1 * sp.cos(t) + sp.sqrt(2)/2 * c2 * sp.sin(t)
latex_simbolico = sp.latex(x_simbolico)
print(f"\n✅ VERSIÓN SIMBÓLICA (deseada):")
print(f"   LaTeX: {latex_simbolico}")

print("\n" + "=" * 80)
print("COMPARACIÓN:")
print("=" * 80)
print(f"Numérico contiene '0.7071': {'0.7071' in latex_numerico}")
print(f"Simbólico contiene 'sqrt': {'sqrt' in latex_simbolico}")
print(f"Simbólico contiene 'frac': {'frac' in latex_simbolico}")
