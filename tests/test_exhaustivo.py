"""
Tests exhaustivos para el proyecto
"""

import unittest
import sys
import numpy as np
from tkinter import tk

# Tests para validación de entrada
from ui.validacion_errores import ValidadorEntrada

class TestValidadorEntrada(unittest.TestCase):
    def test_validar_numeros(self):
        self.assertTrue(ValidadorEntrada.es_numero("5"))
        self.assertTrue(ValidadorEntrada.es_numero("-5.5"))
        self.assertFalse(ValidadorEntrada.es_numero("abc"))
    
    def test_validar_enteros(self):
        self.assertTrue(ValidadorEntrada.es_entero("5"))
        self.assertFalse(ValidadorEntrada.es_entero("5.5"))

# Tests para utilidades de core
from core.utils import (
    normalizar_funciones, validar_expresion_matematica,
    evaluar_expresion, calcular_jacobiano, analizar_estabilidad_punto
)

class TestUtilCore(unittest.TestCase):
    def test_normalizar_sen(self):
        self.assertEqual(normalizar_funciones("sen(x)"), "sin(x)")
    
    def test_validar_expresion(self):
        valida, _ = validar_expresion_matematica("x + y")
        self.assertTrue(valida)
    
    def test_evaluar_expresion(self):
        resultado = evaluar_expresion("x + y", {'x': 2, 'y': 3})
        self.assertEqual(resultado, 5)
    
    def test_jacobiano(self):
        jac = calcular_jacobiano("-x", "-y", (1, 1))
        self.assertEqual(jac.shape, (2, 2))

# Tests para sistemas
from core.sistema import SistemaDinamico2D

class TestSistema2D(unittest.TestCase):
    def setUp(self):
        self.matriz = np.array([[-1, 0], [0, -2]])
        self.sistema = SistemaDinamico2D(self.matriz)
    
    def test_sistema_creacion(self):
        self.assertIsNotNone(self.sistema)
    
    def test_ecuaciones_sistema(self):
        estado = np.array([1, 1])
        resultado = self.sistema.sistema_ecuaciones(estado, 0)
        esperado = np.array([-1, -2])
        np.testing.assert_array_almost_equal(resultado, esperado)

# Tests para modularización
class TestModularizacion(unittest.TestCase):
    def test_modulos_importables(self):
        try:
            from core import SistemaDinamico2D
            from gui.main_interface import InterfazPrincipal
            from input_module.lotka_volterra import InputLotkaVolterra
            from ui.creador_componentes import CreadorPaneles
        except ImportError as e:
            self.fail(f"Error al importar módulos: {e}")
    
    def test_config_centralizada(self):
        from config import CONFIG_VENTANAS, MENSAJES_ERROR
        self.assertIn('principal', CONFIG_VENTANAS)
        self.assertIn('entrada_vacia', MENSAJES_ERROR)

# Tests para repetición de código
class TestDRY(unittest.TestCase):
    def test_utilidades_compartidas_existen(self):
        from ui.gui_utils import (
            crear_frame_parametro, crear_frame_rango_numerico,
            crear_entrada_ecuacion, mostrar_paso_analisis
        )
        self.assertTrue(callable(crear_frame_parametro))
        self.assertTrue(callable(crear_frame_rango_numerico))
    
    def test_base_module_existe(self):
        from gui.base_module import ModuloBase
        self.assertTrue(hasattr(ModuloBase, '_crear_layout_principal'))
    
    def test_creador_componentes(self):
        from ui.creador_componentes import CreadorPaneles, CreadorTablas
        self.assertTrue(callable(CreadorPaneles.panel_entrada_doble))

if __name__ == '__main__':
    unittest.main()
