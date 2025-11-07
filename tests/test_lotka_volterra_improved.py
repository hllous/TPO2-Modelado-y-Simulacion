"""
Test de integración para el módulo Lotka-Volterra mejorado
Verifica que el dual-mode (estándar y personalizado) funciona correctamente
"""

import unittest
import numpy as np
import tkinter as tk
from io import StringIO
import sys


class TestLotkaVolterra(unittest.TestCase):
    """Tests para el módulo Lotka-Volterra"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        pass
    
    def test_importar_modulos_lotka_volterra(self):
        """Verifica que todos los módulos LV se importan correctamente"""
        try:
            from core.lotka_volterra import SistemaLotkaVolterra
            from core.analizador_lv import AnalizadorLotkaVolterra
            from visualization.lotka_volterra import GrapherLotkaVolterra
            from input_module.lotka_volterra import InputLotkaVolterra
            from core.sistema import SistemaDinamico2D
        except ImportError as e:
            self.fail(f"Error al importar módulos LV: {e}")
    
    def test_crear_sistema_standar(self):
        """Verifica creación de sistema estándar Lotka-Volterra"""
        from core.lotka_volterra import SistemaLotkaVolterra
        
        sistema = SistemaLotkaVolterra(alpha=1.0, beta=0.1, gamma=0.1, delta=0.5)
        
        self.assertIsNotNone(sistema)
        self.assertEqual(sistema.alpha, 1.0)
        self.assertEqual(sistema.beta, 0.1)
        self.assertEqual(sistema.gamma, 0.1)
        self.assertEqual(sistema.delta, 0.5)
    
    def test_crear_sistema_personalizado(self):
        """Verifica creación de sistema con funciones personalizadas"""
        from core.sistema import SistemaDinamico2D
        
        # Sistema personalizado con funciones
        sistema = SistemaDinamico2D(
            funcion_personalizada={
                'f1': 'x - 0.5*x*y',  # dx/dt
                'f2': '0.5*x*y - 0.5*y',  # dy/dt
                'es_lineal': False
            }
        )
        
        self.assertIsNotNone(sistema)
        self.assertTrue(sistema.es_no_lineal)
        self.assertIsNotNone(sistema.f1_sym)
        self.assertIsNotNone(sistema.f2_sym)
    
    def test_evaluar_sistema_personalizado(self):
        """Verifica que el sistema personalizado evalúa correctamente"""
        from core.sistema import SistemaDinamico2D
        
        sistema = SistemaDinamico2D(
            funcion_personalizada={
                'f1': 'x - x*y',
                'f2': 'x*y - y',
                'es_lineal': False
            }
        )
        
        # Evaluar en punto (1, 1)
        resultado = sistema.sistema_ecuaciones(np.array([1, 1]), 0)
        
        # En (1,1) con estas ecuaciones: dx/dt = 1 - 1 = 0, dy/dt = 1 - 1 = 0
        self.assertAlmostEqual(resultado[0], 0.0, places=5)
        self.assertAlmostEqual(resultado[1], 0.0, places=5)
    
    def test_jacobiano_sistema_personalizado(self):
        """Verifica cálculo del Jacobiano en sistema personalizado"""
        from core.sistema import SistemaDinamico2D
        
        sistema = SistemaDinamico2D(
            funcion_personalizada={
                'f1': 'x - x*y',
                'f2': 'x*y - y',
                'es_lineal': False
            }
        )
        
        J = sistema.calcular_jacobiano_en_punto(1, 1)
        
        self.assertIsNotNone(J)
        self.assertEqual(J.shape, (2, 2))
    
    def test_input_lotka_volterra_modo_standar(self):
        """Verifica InputLotkaVolterra en modo estándar"""
        root = tk.Tk()
        try:
            from input_module.lotka_volterra import InputLotkaVolterra
            
            frame = ttk.Frame(root)
            frame.pack()
            
            input_panel = InputLotkaVolterra(frame)
            params = input_panel.obtener_parametros()
            
            self.assertEqual(params['modo'], 'estandar')
            self.assertIn('alpha', params)
            self.assertIn('beta', params)
            self.assertIn('gamma', params)
            self.assertIn('delta', params)
        finally:
            root.destroy()
    
    def test_input_lotka_volterra_modo_personalizado(self):
        """Verifica InputLotkaVolterra en modo personalizado"""
        root = tk.Tk()
        try:
            from input_module.lotka_volterra import InputLotkaVolterra
            from tkinter import ttk
            
            frame = ttk.Frame(root)
            frame.pack()
            
            input_panel = InputLotkaVolterra(frame)
            
            # Cambiar a modo personalizado
            input_panel.modo_personalizado.set(True)
            input_panel._cambiar_modo()
            
            # Establecer funciones
            input_panel.func_presa.set('x - x*y')
            input_panel.func_depredador.set('x*y - y')
            
            params = input_panel.obtener_parametros()
            
            self.assertEqual(params['modo'], 'personalizado')
            self.assertEqual(params['func_presa'], 'x - x*y')
            self.assertEqual(params['func_depredador'], 'x*y - y')
        finally:
            root.destroy()
    
    def test_compatibilidad_backward_compatibility(self):
        """Verifica que el sistema estándar sigue funcionando"""
        from core.lotka_volterra import SistemaLotkaVolterra
        
        sistema = SistemaLotkaVolterra(alpha=1.0, beta=0.1, gamma=0.1, delta=0.5)
        
        # Verificar que puede evaluar
        resultado = sistema.sistema_ecuaciones(np.array([1, 1]), 0)
        
        self.assertEqual(len(resultado), 2)
        self.assertFalse(np.isnan(resultado).any())


class TestIntegracionLotkaVolterra(unittest.TestCase):
    """Tests de integración para el módulo LV completo"""
    
    def test_flujo_completo_modo_standar(self):
        """Test del flujo completo en modo estándar"""
        from core.lotka_volterra import SistemaLotkaVolterra
        from core.analizador_lv import AnalizadorLotkaVolterra
        
        # 1. Crear sistema
        sistema = SistemaLotkaVolterra(alpha=1.0, beta=0.1, gamma=0.1, delta=0.5)
        
        # 2. Crear analizador
        analizador = AnalizadorLotkaVolterra(sistema)
        
        # 3. Verificar que funciona
        self.assertIsNotNone(analizador)
        self.assertIsNotNone(sistema)
    
    def test_flujo_completo_modo_personalizado(self):
        """Test del flujo completo en modo personalizado"""
        from core.sistema import SistemaDinamico2D
        
        # 1. Crear sistema personalizado
        sistema = SistemaDinamico2D(
            funcion_personalizada={
                'f1': 'x - 0.1*x*y',
                'f2': '0.1*x*y - 0.5*y',
                'es_lineal': False
            }
        )
        
        # 2. Evaluar
        estado = np.array([2.0, 2.0])
        derivada = sistema.sistema_ecuaciones(estado, 0)
        
        # 3. Verificar resultado
        self.assertEqual(len(derivada), 2)
        self.assertFalse(np.isnan(derivada).any())


if __name__ == '__main__':
    # Importar ttk aquí para evitar conflictos
    from tkinter import ttk
    
    unittest.main(verbosity=2)
