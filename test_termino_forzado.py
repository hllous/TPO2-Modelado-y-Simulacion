"""
Test específico para verificar el funcionamiento del término forzado
"""

import numpy as np
from sistemas_dinamicos_gui import SistemaDinamico2D
from scipy.integrate import odeint

def probar_termino_forzado():
    """Prueba el funcionamiento del término forzado"""

    print("\n" + "=" * 70)
    print("PRUEBA DEL TÉRMINO FORZADO")
    print("=" * 70 + "\n")

    # Sistema base: nodo estable
    matriz = [[-1, 0], [0, -2]]

    # Caso 1: Sistema homogéneo (sin término forzado)
    sistema_homogeneo = SistemaDinamico2D(matriz)

    # Caso 2: Sistema con término forzado constante
    termino_forzado_constante = {
        'tipo': 'constante',
        'coef1': 1.0,
        'coef2': 0.5,
        'param': 0  # no aplica
    }
    sistema_forzado_constante = SistemaDinamico2D(matriz, termino_forzado_constante)

    # Caso 3: Sistema con término forzado sinusoidal
    termino_forzado_seno = {
        'tipo': 'seno',
        'coef1': 0.5,
        'coef2': 0.3,
        'param': 1.0  # frecuencia ω
    }
    sistema_forzado_seno = SistemaDinamico2D(matriz, termino_forzado_seno)

    # Caso 4: Sistema con término forzado exponencial
    termino_forzado_exp = {
        'tipo': 'exponencial',
        'coef1': 0.2,
        'coef2': -0.1,
        'param': 0.5  # constante k
    }
    sistema_forzado_exp = SistemaDinamico2D(matriz, termino_forzado_exp)

    # Probar punto de equilibrio
    print("1. PRUEBA DE PUNTOS DE EQUILIBRIO")
    print("-" * 40)

    # Sistema homogéneo: punto de equilibrio en (0,0)
    eq_homogeneo = sistema_homogeneo.encontrar_puntos_equilibrio()
    print(f"Sistema homogéneo - Puntos de equilibrio: {eq_homogeneo}")

    # Sistema con término forzado constante: punto de equilibrio desplazado
    eq_forzado_constante = sistema_forzado_constante.encontrar_puntos_equilibrio()
    print(f"Sistema con f(t)=[1.0, 0.5]ᵀ - Puntos de equilibrio: {eq_forzado_constante}")

    # Verificar que el punto de equilibrio se haya desplazado correctamente
    # Para dx/dt = Ax + b, el punto de equilibrio satisface Ax + b = 0, así que x = -A⁻¹b
    if eq_forzado_constante:
        x_eq = np.array(eq_forzado_constante[0])
        A_inv = np.linalg.inv(matriz)
        b = np.array([1.0, 0.5])
        x_esperado = -np.dot(A_inv, b)

        error = np.linalg.norm(x_eq - x_esperado)
        print(f"  Error en cálculo: {error:.6f}")
        print(f"  Punto esperado: [{x_esperado[0]:.6f}, {x_esperado[1]:.6f}]")
        if error < 1e-6:
            print("✓ Punto de equilibrio correcto")
        else:
            print("✗ Error en punto de equilibrio")

    print("\n2. PRUEBA DE ECUACIONES DIFERENCIALES")
    print("-" * 40)

    # Probar que las ecuaciones se evalúan correctamente en t=0
    t_test = 0.0
    X_test = np.array([1.0, 1.0])

    # Sistema homogéneo
    deriv_homogeneo = sistema_homogeneo.sistema_ecuaciones(X_test, t_test)
    deriv_esperada_homogeneo = np.dot(matriz, X_test)
    error_homogeneo = np.linalg.norm(deriv_homogeneo - deriv_esperada_homogeneo)
    print(f"  Error sistema homogéneo: {error_homogeneo:.6f}")
    if error_homogeneo < 1e-10:
        print("✓ Sistema homogéneo correcto")
    else:
        print("✗ Error en sistema homogéneo")

    # Sistema con término forzado constante
    deriv_forzado_constante = sistema_forzado_constante.sistema_ecuaciones(X_test, t_test)
    deriv_esperada_forzado = np.dot(matriz, X_test) + np.array([1.0, 0.5])
    error_forzado_constante = np.linalg.norm(deriv_forzado_constante - deriv_esperada_forzado)
    print(f"  Error sistema constante: {error_forzado_constante:.6f}")
    if error_forzado_constante < 1e-10:
        print("✓ Sistema con término constante correcto")
    else:
        print("✗ Error en sistema con término constante")

    # Sistema con término forzado sinusoidal
    deriv_forzado_seno = sistema_forzado_seno.sistema_ecuaciones(X_test, t_test)
    deriv_esperada_seno = np.dot(matriz, X_test) + np.array([0.5 * np.sin(1.0 * t_test), 0.3 * np.sin(1.0 * t_test)])
    error_forzado_seno = np.linalg.norm(deriv_forzado_seno - deriv_esperada_seno)
    print(f"  Error sistema sinusoidal: {error_forzado_seno:.6f}")
    if error_forzado_seno < 1e-10:
        print("✓ Sistema con término sinusoidal correcto")
    else:
        print("✗ Error en sistema con término sinusoidal")

    # Sistema con término forzado exponencial
    deriv_forzado_exp = sistema_forzado_exp.sistema_ecuaciones(X_test, t_test)
    deriv_esperada_exp = np.dot(matriz, X_test) + np.array([0.2 * np.exp(0.5 * t_test), -0.1 * np.exp(0.5 * t_test)])
    error_forzado_exp = np.linalg.norm(deriv_forzado_exp - deriv_esperada_exp)
    print(f"  Error sistema exponencial: {error_forzado_exp:.6f}")
    if error_forzado_exp < 1e-10:
        print("✓ Sistema con término exponencial correcto")
    else:
        print("✗ Error en sistema con término exponencial")

    print("\n3. PRUEBA DE INTEGRACIÓN NUMÉRICA")
    print("-" * 40)

    # Probar integración numérica con diferentes términos forzados
    t_span = np.linspace(0, 5, 100)
    X0 = np.array([2.0, 1.0])

    try:
        # Sistema homogéneo
        sol_homogeneo = odeint(sistema_homogeneo.sistema_ecuaciones, X0, t_span)
        print("✓ Integración sistema homogéneo exitosa")

        # Sistema con término constante
        sol_constante = odeint(sistema_forzado_constante.sistema_ecuaciones, X0, t_span)
        print("✓ Integración sistema con término constante exitosa")

        # Sistema con término sinusoidal
        sol_seno = odeint(sistema_forzado_seno.sistema_ecuaciones, X0, t_span)
        print("✓ Integración sistema con término sinusoidal exitosa")

        # Sistema con término exponencial
        sol_exp = odeint(sistema_forzado_exp.sistema_ecuaciones, X0, t_span)
        print("✓ Integración sistema con término exponencial exitosa")

        # Verificar que las soluciones son diferentes
        diferencia_constante = np.linalg.norm(sol_homogeneo - sol_constante)
        diferencia_seno = np.linalg.norm(sol_homogeneo - sol_seno)
        diferencia_exp = np.linalg.norm(sol_homogeneo - sol_exp)

        print(f"  Diferencia con término constante: {diferencia_constante:.6f}")
        print(f"  Diferencia con término sinusoidal: {diferencia_seno:.6f}")
        print(f"  Diferencia con término exponencial: {diferencia_exp:.6f}")
        if diferencia_constante > 0.1 and diferencia_seno > 0.1 and diferencia_exp > 0.1:
            print("✓ Las soluciones con términos forzados son diferentes del sistema homogéneo")
        else:
            print("✗ Las soluciones no muestran diferencia significativa")

    except Exception as e:
        print(f"✗ Error en integración numérica: {e}")

    print("\n4. PRUEBA DE CLASIFICACIÓN")
    print("-" * 40)

    # Verificar que la clasificación funciona para sistemas con término forzado
    tipo_homo, estab_homo = sistema_homogeneo.clasificar_punto_equilibrio()
    tipo_forzado, estab_forzado = sistema_forzado_constante.clasificar_punto_equilibrio()

    print(f"Sistema homogéneo: {tipo_homo} - {estab_homo}")
    print(f"Sistema con término forzado: {tipo_forzado} - {estab_forzado}")

    # La clasificación debería ser la misma para la parte homogénea
    if tipo_homo == tipo_forzado and estab_homo == estab_forzado:
        print("✓ Clasificación correcta para sistemas con término forzado")
    else:
        print("✗ Error en clasificación de sistemas con término forzado")

    print("\n" + "=" * 70)
    print("PRUEBA COMPLETADA")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    probar_termino_forzado()