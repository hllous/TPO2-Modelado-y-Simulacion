#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug para investigar por qué y(t) = 0
"""

import numpy as np
import sympy as sp

# Sistema: f₁ = -x, f₂ = -2*y
A = np.array([[-1, 0], [0, -2]], dtype=float)

print("="*80)
print("DEBUG: Sistema f₁ = -x, f₂ = -2*y")
print("="*80)

print(f"\nMatriz A:")
print(A)

# Calcular autovalores y autovectores
autovalores, autovectores = np.linalg.eig(A)

print(f"\nAutovalores (numpy):")
print(autovalores)

print(f"\nAutovectores (numpy):")
print(autovectores)

print(f"\nAutovector 1 (λ₁={autovalores[0]}):")
print(f"  v₁ = {autovectores[:, 0]}")

print(f"\nAutovector 2 (λ₂={autovalores[1]}):")
print(f"  v₂ = {autovectores[:, 1]}")

# Verificación
print("\n" + "="*80)
print("VERIFICACIÓN: A·v = λ·v")
print("="*80)

for i in range(2):
    v = autovectores[:, i]
    λ = autovalores[i]
    Av = A @ v
    λv = λ * v
    print(f"\nAutovector {i+1}:")
    print(f"  A·v = {Av}")
    print(f"  λ·v = {λv}")
    print(f"  ¿Son iguales? {np.allclose(Av, λv)}")

# Solución esperada
print("\n" + "="*80)
print("SOLUCIÓN ESPERADA")
print("="*80)

t, c1, c2 = sp.symbols('t c1 c2', real=True)

λ1, λ2 = autovalores
v1 = autovectores[:, 0]
v2 = autovectores[:, 1]

print(f"\nUsando fórmula: x(t) = c₁·v₁·e^(λ₁·t) + c₂·v₂·e^(λ₂·t)")

x_t = c1 * v1[0] * sp.exp(λ1 * t) + c2 * v2[0] * sp.exp(λ2 * t)
y_t = c1 * v1[1] * sp.exp(λ1 * t) + c2 * v2[1] * sp.exp(λ2 * t)

print(f"\nx(t) = c1·{v1[0]}·e^({λ1}·t) + c2·{v2[0]}·e^({λ2}·t)")
print(f"     = {x_t}")

print(f"\ny(t) = c1·{v1[1]}·e^({λ1}·t) + c2·{v2[1]}·e^({λ2}·t)")
print(f"     = {y_t}")

print("\n" + "="*80)
print("DIAGNÓSTICO")
print("="*80)

print(f"\nv1[0] = {v1[0]} (componente x del primer autovector)")
print(f"v1[1] = {v1[1]} (componente y del primer autovector)")
print(f"v2[0] = {v2[0]} (componente x del segundo autovector)")
print(f"v2[1] = {v2[1]} (componente y del segundo autovector)")

if abs(v2[1]) < 1e-10:
    print("\n⚠️  PROBLEMA DETECTADO: v2[1] ≈ 0")
    print("   Esto hace que y(t) = c1·0·e^(-t) + c2·0·e^(-2t) = 0")
    print("   ¡Los autovectores están intercambiados!")
else:
    print("\n✓ Autovectores parecen correctos")
