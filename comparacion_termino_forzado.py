"""
Comparación visual entre sistema con y sin término forzado
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from sistemas_dinamicos_gui import SistemaDinamico2D

def comparar_sistemas():
    """Compara visualmente un sistema con y sin término forzado"""

    print("\n" + "=" * 80)
    print("COMPARACIÓN: SISTEMA CON Y SIN TÉRMINO FORZADO")
    print("=" * 80 + "\n")

    # Sistema base: Nodo estable
    matriz = [[-1, 0], [0, -2]]
    print("Sistema base (Nodo Estable):")
    print("Matriz A = [[-1, 0], [0, -2]]")
    print("dx₁/dt = -x₁")
    print("dx₂/dt = -2x₂")
    print()

    # Sistema sin término forzado
    sistema_homogeneo = SistemaDinamico2D(matriz)
    print("1. SISTEMA HOMOGÉNEO (sin término forzado):")
    print("   dx/dt = Ax")
    print("   Punto de equilibrio: (0, 0)")

    tipo_homo, estab_homo = sistema_homogeneo.clasificar_punto_equilibrio()
    print(f"   Clasificación: {tipo_homo} - {estab_homo}")
    print()

    # Sistema con término forzado constante
    termino_forzado = {
        'tipo': 'constante',
        'coef1': 1.0,    # Fuerza constante en x₁
        'coef2': 0.5,    # Fuerza constante en x₂
        'param': 0       # No aplica para constante
    }

    sistema_forzado = SistemaDinamico2D(matriz, termino_forzado)
    print("2. SISTEMA NO HOMOGÉNEO (con término forzado constante):")
    print("   dx/dt = Ax + f(t)")
    print("   f(t) = [1.0, 0.5]ᵀ  (constante)")

    # Calcular punto de equilibrio teórico
    A_inv = np.linalg.inv(matriz)
    f_constante = np.array([1.0, 0.5])
    eq_teorico = -np.dot(A_inv, f_constante)
    print(f"   Punto de equilibrio teórico: ({eq_teorico[0]:.6f}, {eq_teorico[1]:.6f})")
    print("   dx₁/dt = -x₁ + 1.0")
    print("   dx₂/dt = -2x₂ + 0.5")
    print()

    # Verificar punto de equilibrio encontrado
    eq_encontrado = sistema_forzado.encontrar_puntos_equilibrio()
    if eq_encontrado:
        eq_x, eq_y = eq_encontrado[0]
        print(f"   Punto de equilibrio encontrado: ({eq_x:.6f}, {eq_y:.6f})")
        error = np.linalg.norm(np.array([eq_x, eq_y]) - eq_teorico)
        print(f"   Error en cálculo: {error:.6f}")
    tipo_forzado, estab_forzado = sistema_forzado.clasificar_punto_equilibrio()
    print(f"   Clasificación (parte homogénea): {tipo_forzado} - {estab_forzado}")
    print()

    # Simulación numérica
    print("3. SIMULACIÓN NUMÉRICA:")
    print("-" * 40)

    # Condición inicial
    X0 = np.array([2.0, 1.0])  # Punto inicial
    t_span = np.linspace(0, 8, 200)  # Tiempo de simulación

    print(f"   Condición inicial: x₀ = ({X0[0]:.1f}, {X0[1]:.1f})")
    print()

    # Resolver sistemas
    try:
        sol_homogeneo = odeint(sistema_homogeneo.sistema_ecuaciones, X0, t_span)
        sol_forzado = odeint(sistema_forzado.sistema_ecuaciones, X0, t_span)

        print("✓ Integración numérica exitosa")
        print()

        # Análisis de convergencia
        print("4. ANÁLISIS DE CONVERGENCIA:")
        print("-" * 40)

        # Para sistema homogéneo: debería converger a (0,0)
        final_homogeneo = sol_homogeneo[-1]
        distancia_homogeneo = np.linalg.norm(final_homogeneo)
        print(f"   Sistema homogéneo - Distancia final al origen: {distancia_homogeneo:.6f}")
        # Para sistema forzado: debería converger al nuevo punto de equilibrio
        final_forzado = sol_forzado[-1]
        distancia_forzado = np.linalg.norm(final_forzado - eq_teorico)
        print(f"   Sistema forzado - Distancia final al equilibrio: {distancia_forzado:.6f}")
        print()

        # Comparación de trayectorias
        print("5. DIFERENCIAS ENTRE TRAYECTORIAS:")
        print("-" * 40)

        # Calcular diferencia máxima entre trayectorias
        diferencia_max = np.max(np.linalg.norm(sol_homogeneo - sol_forzado, axis=1))
        print(f"   Diferencia máxima entre trayectorias: {diferencia_max:.6f}")
        # Calcular tiempo hasta convergencia aproximada
        tolerancia = 0.01
        tiempo_convergencia_homo = None
        tiempo_convergencia_forzado = None

        for i, t in enumerate(t_span):
            if tiempo_convergencia_homo is None and np.linalg.norm(sol_homogeneo[i]) < tolerancia:
                tiempo_convergencia_homo = t
            if tiempo_convergencia_forzado is None and np.linalg.norm(sol_forzado[i] - eq_teorico) < tolerancia:
                tiempo_convergencia_forzado = t

        if tiempo_convergencia_homo:
            print(f"   Tiempo de convergencia (homogéneo): {tiempo_convergencia_homo:.2f} s")
        if tiempo_convergencia_forzado:
            print(f"   Tiempo de convergencia (forzado): {tiempo_convergencia_forzado:.2f} s")
        print()

        # Crear gráfica comparativa
        print("6. GENERANDO GRÁFICA COMPARATIVA...")
        print("-" * 40)

        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # Gráfica 1: Sistema homogéneo
        sistema_homogeneo.crear_grafica(axes[0], xlim=(-3, 3), ylim=(-2, 2))
        axes[0].plot(sol_homogeneo[:, 0], sol_homogeneo[:, 1], 'r-', linewidth=3,
                    label=f'Trayectoria desde {X0}', alpha=0.8)
        axes[0].plot(X0[0], X0[1], 'ro', markersize=8, label='Punto inicial')
        axes[0].set_title('Sistema Homogéneo\ndx/dt = Ax', fontsize=14, fontweight='bold')
        axes[0].legend()

        # Gráfica 2: Sistema con término forzado
        sistema_forzado.crear_grafica(axes[1], xlim=(-1, 3), ylim=(-0.5, 1.5))
        axes[1].plot(sol_forzado[:, 0], sol_forzado[:, 1], 'r-', linewidth=3,
                    label=f'Trayectoria desde {X0}', alpha=0.8)
        axes[1].plot(X0[0], X0[1], 'ro', markersize=8, label='Punto inicial')
        # Marcar nuevo punto de equilibrio
        if eq_encontrado:
            axes[1].plot(eq_x, eq_y, 'kx', markersize=12, markeredgewidth=3,
                        label=f'Equilibrio: ({eq_x:.2f}, {eq_y:.2f})')
        axes[1].set_title('Sistema No Homogéneo\ndx/dt = Ax + f(t)', fontsize=14, fontweight='bold')
        axes[1].legend()

        plt.tight_layout()
        plt.savefig('comparacion_termino_forzado.png', dpi=150, bbox_inches='tight')
        print("✓ Gráfica guardada como 'comparacion_termino_forzado.png'")
        plt.show()

        print("\n" + "=" * 80)
        print("RESUMEN DE DIFERENCIAS:")
        print("=" * 80)
        print("• Sistema homogéneo: converge al origen (0, 0)")
        print("• Sistema forzado: converge al punto desplazado (1.0, 0.25)")
        print("• El término forzado desplaza el punto de equilibrio")
        print("• Las trayectorias son cualitativamente similares pero cuantitativamente diferentes")
        print("• La estabilidad local se mantiene (determinada por la matriz A)")
        print("• El término forzado añade una componente particular a la solución")

    except Exception as e:
        print(f"✗ Error en la simulación: {e}")

    print("\n" + "=" * 80 + "\n")

def ejemplo_otro_termino_forzado():
    """Ejemplo con término forzado sinusoidal"""

    print("\n" + "=" * 80)
    print("EJEMPLO ADICIONAL: TÉRMINO FORZADO SINUSOIDAL")
    print("=" * 80 + "\n")

    # Sistema base: Centro (oscilador armónico)
    matriz = [[0, 1], [-1, 0]]
    print("Sistema base (Centro):")
    print("Matriz A = [[0, 1], [-1, 0]]")
    print("dx₁/dt = x₂")
    print("dx₂/dt = -x₁")
    print()

    # Sistema con término forzado sinusoidal
    termino_forzado_sin = {
        'tipo': 'seno',
        'coef1': 0.0,    # Sin fuerza en x₁
        'coef2': 0.5,    # Fuerza sinusoidal en x₂
        'param': 2.0     # Frecuencia ω = 2
    }

    sistema_sin = SistemaDinamico2D(matriz, termino_forzado_sin)
    print("Sistema con término forzado sinusoidal:")
    print("dx₁/dt = x₂")
    print("dx₂/dt = -x₁ + 0.5·sin(2t)")
    print()

    # Simulación rápida
    X0 = np.array([1.0, 0.0])
    t_span = np.linspace(0, 10, 300)

    try:
        sol_sin = odeint(sistema_sin.sistema_ecuaciones, X0, t_span)

        # Crear gráfica
        fig, ax = plt.subplots(figsize=(10, 6))
        sistema_sin.crear_grafica(ax, xlim=(-2, 2), ylim=(-2, 2))
        ax.plot(sol_sin[:, 0], sol_sin[:, 1], 'r-', linewidth=2,
               label=f'Trayectoria desde {X0}', alpha=0.8)
        ax.plot(X0[0], X0[1], 'ro', markersize=8, label='Punto inicial')
        ax.set_title('Sistema Centro con Término Forzado Sinusoidal\ndx₂/dt = -x₁ + 0.5·sin(2t)',
                    fontsize=14, fontweight='bold')
        ax.legend()

        plt.tight_layout()
        plt.savefig('ejemplo_sinusoidal.png', dpi=150, bbox_inches='tight')
        print("✓ Gráfica guardada como 'ejemplo_sinusoidal.png'")
        plt.show()

        print("Observación: El término sinusoidal añade oscilaciones forzadas")
        print("al movimiento circular natural del sistema.")

    except Exception as e:
        print(f"✗ Error en simulación sinusoidal: {e}")

    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    comparar_sistemas()
    ejemplo_otro_termino_forzado()