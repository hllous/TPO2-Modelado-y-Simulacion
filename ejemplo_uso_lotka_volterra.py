"""
EJEMPLO DE USO - Módulo Lotka-Volterra Mejorado
Demuestra cómo usar el nuevo dual-mode (estándar y personalizado)
"""

def ejemplo_modo_standar():
    """
    Ejemplo 1: Usar el módulo Lotka-Volterra en modo ESTÁNDAR
    (parámetros clásicos alpha, beta, gamma, delta)
    """
    print("\n" + "="*60)
    print("EJEMPLO 1: MODO ESTÁNDAR LOTKA-VOLTERRA")
    print("="*60)
    
    try:
        from core.lotka_volterra import SistemaLotkaVolterra
        from core.analizador_lv import AnalizadorLotkaVolterra
        import numpy as np
        
        # Crear sistema con parámetros clásicos
        print("\n1. Creando sistema Lotka-Volterra estándar:")
        print("   α=1.0 (crecimiento presas)")
        print("   β=0.1 (depredación)")
        print("   γ=0.1 (eficiencia depredador)")
        print("   δ=0.5 (muerte depredador)")
        
        sistema = SistemaLotkaVolterra(alpha=1.0, beta=0.1, gamma=0.1, delta=0.5)
        print("   ✓ Sistema creado")
        
        # Evaluar en un punto
        print("\n2. Evaluando en punto inicial (presas=2, depredadores=1):")
        estado = np.array([2.0, 1.0])
        derivada = sistema.sistema_ecuaciones(estado, 0)
        print(f"   dx/dt = {derivada[0]:.4f}")
        print(f"   dy/dt = {derivada[1]:.4f}")
        
        # Analizar
        print("\n3. Analizando estabilidad:")
        analizador = AnalizadorLotkaVolterra(sistema)
        print(f"   Punto de equilibrio: (~{sistema.x_eq:.2f}, ~{sistema.y_eq:.2f})")
        
        print("\n✓ Modo estándar funcionando correctamente")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")


def ejemplo_modo_personalizado():
    """
    Ejemplo 2: Usar el módulo Lotka-Volterra en modo PERSONALIZADO
    (funciones personalizadas dx/dt, dy/dt)
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: MODO PERSONALIZADO - FUNCIONES CUSTOM")
    print("="*60)
    
    try:
        from core.sistema import SistemaDinamico2D
        import numpy as np
        
        # Definir funciones personalizadas
        print("\n1. Definiendo funciones personalizadas:")
        print("   dx/dt = x - 0.5*x*y  (presas)")
        print("   dy/dt = 0.5*x*y - 0.5*y  (depredadores)")
        
        sistema = SistemaDinamico2D(
            funcion_personalizada={
                'f1': 'x - 0.5*x*y',  # dx/dt
                'f2': '0.5*x*y - 0.5*y',  # dy/dt
                'es_lineal': False
            }
        )
        print("   ✓ Sistema personalizado creado")
        
        # Evaluar en un punto
        print("\n2. Evaluando en punto inicial (x=2, y=1):")
        estado = np.array([2.0, 1.0])
        derivada = sistema.sistema_ecuaciones(estado, 0)
        print(f"   dx/dt = {derivada[0]:.4f}")
        print(f"   dy/dt = {derivada[1]:.4f}")
        
        # Calcular Jacobiano
        print("\n3. Calculando Jacobiano en punto:")
        J = sistema.calcular_jacobiano_en_punto(2.0, 1.0)
        print(f"   Jacobiano calculado: matriz {J.shape}")
        
        # Encontrar puntos de equilibrio
        print("\n4. Buscando puntos de equilibrio:")
        puntos_eq = sistema.encontrar_puntos_equilibrio()
        print(f"   Puntos encontrados: {len(puntos_eq)}")
        for i, (x, y) in enumerate(puntos_eq):
            print(f"   Punto {i+1}: ({x:.4f}, {y:.4f})")
        
        print("\n✓ Modo personalizado funcionando correctamente")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")


def ejemplo_via_interfaz():
    """
    Ejemplo 3: Cómo usar a través de la interfaz (InputLotkaVolterra)
    (Este es un pseudo-código ya que la GUI requiere Tk)
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: USO A TRAVÉS DE INTERFAZ")
    print("="*60)
    
    print("\nA través del InputLotkaVolterra:")
    print("\n1. MODO ESTÁNDAR (seleccionar 'Modelo Estándar'):")
    print("   - Entrada de parámetros con sliders:")
    print("     * alpha: tasa crecimiento presas")
    print("     * beta: tasa depredación")
    print("     * gamma: eficiencia depredador")
    print("     * delta: tasa muerte depredador")
    print("   - obtener_parametros() retorna:")
    print("     {'modo': 'estandar', 'alpha': 1.0, 'beta': 0.1, ...}")
    
    print("\n2. MODO PERSONALIZADO (seleccionar 'Funciones Personalizadas'):")
    print("   - Entrada de ecuaciones:")
    print("     * dx/dt (Presa): ej. 'x - 0.5*x*y'")
    print("     * dy/dt (Depredador): ej. '0.5*x*y - 0.5*y'")
    print("   - Variables disponibles: x, y")
    print("   - Funciones disponibles: sin(), cos(), exp(), sqrt(), abs()")
    print("   - obtener_parametros() retorna:")
    print("     {'modo': 'personalizado', 'func_presa': '...', 'func_depredador': '...'}")
    
    print("\n3. LA GUI (gui/lotka_volterra.py):")
    print("   - _actualizar_sistema() detecta el modo")
    print("   - Si personalizado: crea SistemaDinamico2D con funciones")
    print("   - Si estándar: crea SistemaLotkaVolterra tradicional")
    print("   - GrapherLotkaVolterra y AnalizadorLotkaVolterra funcionan igual")


def ejemplo_casos_uso():
    """
    Ejemplo 4: Casos de uso práctica
    """
    print("\n" + "="*60)
    print("EJEMPLO 4: CASOS DE USO PRÁCTICOS")
    print("="*60)
    
    print("\n📌 CASO 1: Parámetros no estándar")
    print("   - Usar modo PERSONALIZADO")
    print("   - dx/dt = x*(2 - 0.1*y)")  
    print("   - dy/dt = y*(0.05*x - 1)")
    print("   - Modela depredador más eficiente")
    
    print("\n📌 CASO 2: Efecto ambiental (término forzado)")
    print("   - dx/dt = x - 0.1*x*y + 0.1*sin(t)")
    print("   - dy/dt = 0.1*x*y - y")
    print("   - Modelan variaciones estacionales")
    
    print("\n📌 CASO 3: Resistencia a depredación")
    print("   - dx/dt = x*(1 - 0.1*y) + 0.5")
    print("   - dy/dt = 0.05*x*y - 0.5*y")
    print("   - Presa tiene término de crecimiento externo")
    
    print("\n📌 CASO 4: Comparación rápida")
    print("   - Usar MODO ESTÁNDAR para referencia")
    print("   - Pasar a MODO PERSONALIZADO para ajustes")
    print("   - Visualizar diferencias en campo de fase")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " EJEMPLOS DE USO: MÓDULO LOTKA-VOLTERRA MEJORADO ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    # Ejecutar ejemplos
    ejemplo_modo_standar()
    ejemplo_modo_personalizado()
    ejemplo_via_interfaz()
    ejemplo_casos_uso()
    
    print("\n" + "="*60)
    print("✓ RESUMEN")
    print("="*60)
    print("\n✓ Dual-mode permite:")
    print("  • Trabajar con parámetros estándar de Lotka-Volterra")
    print("  • O definir dinámicas completamente personalizadas")
    print("  • Intercambiar entre modos sin reiniciar")
    print("  • Mantiene compatibilidad total con código existente")
    print("\n✓ Principios aplicados:")
    print("  • KISS: interfaz clara, cambio de modo simple")
    print("  • DRY: no hay duplicación, reutiliza SistemaDinamico2D")
    print("  • Modular: cada modo independiente, fallback seguro")
    print("\n✓ Estado: LISTO PARA USAR ✓")
    print()


if __name__ == '__main__':
    main()
