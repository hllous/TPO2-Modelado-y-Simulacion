#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test exhaustivo de todos los ejemplos default de soluciones paramétricas
"""

import sys
sys.path.append('.')

from core.sistema import SistemaDinamico2D
import numpy as np

# Todos los ejemplos del GUI
EJEMPLOS = {
    '🎯 Centro (Ejemplo por defecto)': {
        'f1': 'y',
        'f2': '-x',
        'esperado': {
            'tipo': 'Autovalores complejos conjugados',
            'autovalores_tipo': 'imaginarios puros',  # ±i
            'debe_contener_x': ['cos', 'sin'],
            'debe_contener_y': ['cos', 'sin'],
            'no_debe_contener': ['exp']  # No debe tener exponencial (α=0)
        }
    },
    '📉 Nodo Estable': {
        'f1': '-x',
        'f2': '-2*y',
        'esperado': {
            'tipo': 'Autovalores reales distintos',
            'autovalores_tipo': 'negativos',  # -1, -2
            'debe_contener_x': ['exp(-t)'],
            'debe_contener_y': ['exp(-2'],
            'no_debe_contener': ['sin', 'cos']
        }
    },
    '📈 Nodo Inestable': {
        'f1': 'x',
        'f2': '2*y',
        'esperado': {
            'tipo': 'Autovalores reales distintos',
            'autovalores_tipo': 'positivos',  # 1, 2
            'debe_contener_x': ['exp(t)'],
            'debe_contener_y': ['exp(2'],
            'no_debe_contener': ['sin', 'cos', 'exp(-']
        }
    },
    '⚡ Nodo Silla': {
        'f1': 'x',
        'f2': '-y',
        'esperado': {
            'tipo': 'Autovalores reales distintos',
            'autovalores_tipo': 'signos opuestos',  # 1, -1
            'debe_contener_x': ['exp(t)'],
            'debe_contener_y': ['exp(-t)'],
            'no_debe_contener': ['sin', 'cos']
        }
    },
    '🌀 Espiral Estable 1': {
        'f1': '-x + 2*y',
        'f2': '-2*x - y',
        'esperado': {
            'tipo': 'Autovalores complejos conjugados',
            'autovalores_tipo': 'parte real negativa',  # -1 ± 2i
            'debe_contener_x': ['sin', 'cos', 'exp(-'],
            'debe_contener_y': ['sin', 'cos', 'exp(-'],
            'no_debe_contener': []
        }
    },
    '🌪️ Espiral Inestable 1': {
        'f1': 'x - 2*y',
        'f2': '2*x + y',
        'esperado': {
            'tipo': 'Autovalores complejos conjugados',
            'autovalores_tipo': 'parte real positiva',  # 1 ± 2i
            'debe_contener_x': ['sin', 'cos', 'exp('],
            'debe_contener_y': ['sin', 'cos', 'exp('],
            'no_debe_contener': []
        }
    },
    '🔄 Espiral Estable 2': {
        'f1': '-2*x + y',
        'f2': '-x - 2*y',
        'esperado': {
            'tipo': 'Autovalores complejos conjugados',
            'autovalores_tipo': 'parte real negativa',
            'debe_contener_x': ['sin', 'cos', 'exp(-'],
            'debe_contener_y': ['sin', 'cos', 'exp(-'],
            'no_debe_contener': []
        }
    },
    '💫 Sistema Acoplado 1': {
        'f1': '-x + y',
        'f2': '-2*x',
        'esperado': {
            'tipo': None,  # Puede ser real o complejo
            'autovalores_tipo': 'acoplado',
            'debe_contener_x': ['exp'],
            'debe_contener_y': ['exp'],
            'no_debe_contener': []
        }
    },
    '✨ Sistema Acoplado 2': {
        'f1': '2*x + y',
        'f2': 'x + 2*y',
        'esperado': {
            'tipo': 'Autovalores reales distintos',
            'autovalores_tipo': 'positivos',  # 1, 3
            'debe_contener_x': ['exp'],
            'debe_contener_y': ['exp'],
            'no_debe_contener': ['sin', 'cos']
        }
    },
    '🎨 Sistema Mixto': {
        'f1': '-x + 3*y',
        'f2': '-3*x - y',
        'esperado': {
            'tipo': 'Autovalores complejos conjugados',
            'autovalores_tipo': 'parte real negativa',
            'debe_contener_x': ['sin', 'cos', 'exp(-'],
            'debe_contener_y': ['sin', 'cos', 'exp(-'],
            'no_debe_contener': []
        }
    }
}

def verificar_autovalores(autovalores, tipo_esperado):
    """Verifica que los autovalores sean del tipo esperado"""
    λ1, λ2 = autovalores
    
    if tipo_esperado == 'imaginarios puros':
        # Parte real ≈ 0, parte imaginaria ≠ 0
        return abs(λ1.real) < 1e-10 and abs(λ1.imag) > 1e-10
    
    elif tipo_esperado == 'negativos':
        # Ambos negativos y reales
        return λ1.real < 0 and λ2.real < 0 and abs(λ1.imag) < 1e-10 and abs(λ2.imag) < 1e-10
    
    elif tipo_esperado == 'positivos':
        # Ambos positivos y reales
        return λ1.real > 0 and λ2.real > 0 and abs(λ1.imag) < 1e-10 and abs(λ2.imag) < 1e-10
    
    elif tipo_esperado == 'signos opuestos':
        # Uno positivo, uno negativo (reales)
        return (λ1.real * λ2.real < 0) and abs(λ1.imag) < 1e-10 and abs(λ2.imag) < 1e-10
    
    elif tipo_esperado == 'parte real negativa':
        # Complejos conjugados con parte real < 0
        return λ1.real < 0 and abs(λ1.imag) > 1e-10
    
    elif tipo_esperado == 'parte real positiva':
        # Complejos conjugados con parte real > 0
        return λ1.real > 0 and abs(λ1.imag) > 1e-10
    
    elif tipo_esperado == 'acoplado':
        # Cualquier tipo es válido
        return True
    
    return False

def test_ejemplo(nombre, config):
    """Prueba un ejemplo específico"""
    print("\n" + "="*80)
    print(f"TEST: {nombre}")
    print("="*80)
    
    f1 = config['f1']
    f2 = config['f2']
    esperado = config['esperado']
    
    print(f"\nSistema:")
    print(f"  f₁(x,y) = {f1}")
    print(f"  f₂(x,y) = {f2}")
    
    # Crear sistema
    funcion_personalizada = {
        'f1': f1,
        'f2': f2,
        'es_lineal': True
    }
    
    try:
        sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
        resultado = sistema.obtener_soluciones_parametricas()
        
        if not resultado['es_valido']:
            print(f"\n❌ ERROR: {resultado.get('mensaje', 'Sin mensaje')}")
            return False
        
        # Mostrar resultados
        print(f"\nTipo detectado: {resultado['tipo']}")
        print(f"Autovalores: {resultado['autovalores']}")
        print(f"\nSolución x(t): {resultado['solucion_general']['x']}")
        print(f"Solución y(t): {resultado['solucion_general']['y']}")
        
        # Verificaciones
        errores = []
        
        # 1. Verificar tipo (si se especificó)
        if esperado['tipo'] is not None:
            if resultado['tipo'] != esperado['tipo']:
                errores.append(f"Tipo esperado: '{esperado['tipo']}', obtenido: '{resultado['tipo']}'")
        
        # 2. Verificar autovalores
        if not verificar_autovalores(resultado['autovalores'], esperado['autovalores_tipo']):
            errores.append(f"Autovalores no cumplen criterio: {esperado['autovalores_tipo']}")
        
        # 3. Verificar contenido de x(t)
        x_str = resultado['solucion_general']['x']
        for termino in esperado['debe_contener_x']:
            if termino not in x_str:
                errores.append(f"x(t) debería contener '{termino}'")
        
        # 4. Verificar contenido de y(t)
        y_str = resultado['solucion_general']['y']
        for termino in esperado['debe_contener_y']:
            if termino not in y_str:
                errores.append(f"y(t) debería contener '{termino}'")
        
        # 5. Verificar que NO contenga ciertos términos
        for termino in esperado['no_debe_contener']:
            if termino in x_str or termino in y_str:
                errores.append(f"Las soluciones NO deberían contener '{termino}'")
        
        # 6. Verificar que no haya soluciones triviales (0) cuando no debería
        if x_str == '0' and 'Centro' not in nombre:
            errores.append("x(t) = 0 (solución trivial incorrecta)")
        if y_str == '0' and 'Centro' not in nombre:
            errores.append("y(t) = 0 (solución trivial incorrecta)")
        
        # Resultado
        if errores:
            print("\n❌ ERRORES DETECTADOS:")
            for error in errores:
                print(f"   • {error}")
            return False
        else:
            print("\n✅ TODAS LAS VERIFICACIONES PASARON")
            return True
            
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*80)
    print("  TEST EXHAUSTIVO DE TODOS LOS EJEMPLOS DEFAULT")
    print("="*80)
    
    resultados = {}
    
    for nombre, config in EJEMPLOS.items():
        resultado = test_ejemplo(nombre, config)
        resultados[nombre] = resultado
    
    # Resumen
    print("\n" + "="*80)
    print("  RESUMEN DE RESULTADOS")
    print("="*80)
    
    pasados = sum(1 for r in resultados.values() if r)
    totales = len(resultados)
    
    for nombre, resultado in resultados.items():
        emoji = "✅" if resultado else "❌"
        print(f"{emoji} {nombre}")
    
    print("\n" + "="*80)
    print(f"TOTAL: {pasados}/{totales} ejemplos correctos")
    print("="*80)
    
    if pasados == totales:
        print("\n🎉 ¡TODOS LOS EJEMPLOS SON CORRECTOS!")
        return True
    else:
        print(f"\n⚠️  {totales - pasados} ejemplo(s) tienen problemas")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
