"""
Script de prueba para verificar el funcionamiento del sistema
"""

import numpy as np
from sistemas_dinamicos_2d import SistemaDinamico2D

def probar_clasificaciones():
    """Prueba la clasificación de diferentes tipos de sistemas"""
    
    print("\n" + "=" * 70)
    print("PRUEBA DE CLASIFICACIÓN DE SISTEMAS")
    print("=" * 70 + "\n")
    
    casos_prueba = [
        ("Nodo Estable", [[-1, 0], [0, -2]], "Nodo Propio", "Estable"),
        ("Nodo Inestable", [[1, 0], [0, 2]], "Nodo Propio", "Inestable"),
        ("Punto Silla", [[1, 0], [0, -1]], "Punto Silla", "Inestable"),
        ("Espiral Estable", [[-0.5, 1], [-1, -0.5]], "Espiral", "Estable"),
        ("Espiral Inestable", [[0.5, 1], [-1, 0.5]], "Espiral", "Inestable"),
        ("Centro", [[0, 1], [-1, 0]], "Centro", "Neutral"),
        ("Nodo Estrella Estable", [[-2, 0], [0, -2]], "Nodo Estrella", "Estable"),
    ]
    
    pasados = 0
    fallados = 0
    
    for nombre, matriz, tipo_esperado, estabilidad_esperada in casos_prueba:
        sistema = SistemaDinamico2D(matriz)
        tipo, estabilidad = sistema.clasificar_punto_equilibrio()
        
        tipo_correcto = tipo_esperado in tipo
        estabilidad_correcta = estabilidad_esperada in estabilidad
        
        if tipo_correcto and estabilidad_correcta:
            resultado = "✓ PASADO"
            pasados += 1
            color = "\033[92m"  # Verde
        else:
            resultado = "✗ FALLADO"
            fallados += 1
            color = "\033[91m"  # Rojo
        
        reset = "\033[0m"
        
        print(f"{color}{resultado}{reset} - {nombre}")
        print(f"  Esperado: {tipo_esperado}, {estabilidad_esperada}")
        print(f"  Obtenido: {tipo}, {estabilidad}")
        print(f"  Autovalores: {sistema.autovalores}")
        print()
    
    print("=" * 70)
    print(f"Resultados: {pasados} pasados, {fallados} fallados")
    print("=" * 70 + "\n")


def probar_calculos():
    """Prueba los cálculos matemáticos básicos"""
    
    print("\n" + "=" * 70)
    print("PRUEBA DE CÁLCULOS MATEMÁTICOS")
    print("=" * 70 + "\n")
    
    # Caso conocido: matriz diagonal
    matriz = [[2, 0], [0, 3]]
    sistema = SistemaDinamico2D(matriz)
    
    print("Matriz diagonal simple: [[2, 0], [0, 3]]")
    print(f"  Determinante calculado: {sistema.determinante}")
    print(f"  Determinante esperado: 6.0")
    print(f"  Traza calculada: {sistema.traza}")
    print(f"  Traza esperada: 5.0")
    print(f"  Autovalores: {sistema.autovalores}")
    print(f"  Autovalores esperados: [2, 3]")
    
    det_correcto = abs(sistema.determinante - 6.0) < 1e-10
    traza_correcta = abs(sistema.traza - 5.0) < 1e-10
    
    if det_correcto and traza_correcta:
        print(f"\n✓ Cálculos correctos")
    else:
        print(f"\n✗ Error en cálculos")
    
    print("\n" + "=" * 70 + "\n")


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print("=" * 70 + "\n")
    
    dependencias = [
        ("numpy", "NumPy"),
        ("matplotlib", "Matplotlib"),
        ("scipy", "SciPy"),
        ("tkinter", "Tkinter")
    ]
    
    todas_instaladas = True
    
    for modulo, nombre in dependencias:
        try:
            __import__(modulo)
            print(f"✓ {nombre} instalado correctamente")
        except ImportError:
            print(f"✗ {nombre} NO está instalado")
            todas_instaladas = False
    
    print("\n" + "=" * 70)
    
    if todas_instaladas:
        print("✓ Todas las dependencias están instaladas")
    else:
        print("✗ Faltan dependencias. Ejecute: pip install -r requirements.txt")
    
    print("=" * 70 + "\n")
    
    return todas_instaladas


if __name__ == "__main__":
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SISTEMA DE PRUEBAS AUTOMÁTICAS" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n⚠️  ADVERTENCIA: Instale las dependencias faltantes antes de continuar\n")
    
    # Probar cálculos
    probar_calculos()
    
    # Probar clasificaciones
    probar_clasificaciones()
    
    print("\n✓ Pruebas completadas\n")
