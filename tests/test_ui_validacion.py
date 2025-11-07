"""
Tests para validación de entrada y manejo de excepciones
"""

import unittest
from ui.gui_utils import validar_numero, validar_numero_entero, crear_etiqueta_informativa


class TestValidacionEntrada(unittest.TestCase):
    """Tests para funciones de validación"""
    
    def test_validar_numero_valido(self):
        """Prueba validación de números válidos"""
        self.assertTrue(validar_numero("5"))
        self.assertTrue(validar_numero("5.5"))
        self.assertTrue(validar_numero("-5"))
        self.assertTrue(validar_numero("-5.5"))
        self.assertTrue(validar_numero(".5"))
        self.assertTrue(validar_numero("-"))
        self.assertTrue(validar_numero("."))
        self.assertTrue(validar_numero(""))
    
    def test_validar_numero_invalido(self):
        """Prueba validación de números inválidos"""
        self.assertFalse(validar_numero("abc"))
        self.assertFalse(validar_numero("5a"))
        self.assertFalse(validar_numero("a5"))
    
    def test_validar_numero_entero_valido(self):
        """Prueba validación de enteros válidos"""
        self.assertTrue(validar_numero_entero("5"))
        self.assertTrue(validar_numero_entero("-5"))
        self.assertTrue(validar_numero_entero("-"))
        self.assertTrue(validar_numero_entero(""))
    
    def test_validar_numero_entero_invalido(self):
        """Prueba validación de enteros inválidos"""
        self.assertFalse(validar_numero_entero("5.5"))
        self.assertFalse(validar_numero_entero("abc"))
        self.assertFalse(validar_numero_entero(".5"))


class TestGUIUtilidades(unittest.TestCase):
    """Tests para utilidades de GUI"""
    
    def test_valores_defecto(self):
        """Verifica que las funciones manejen valores por defecto"""
        self.assertIsNone(crear_etiqueta_informativa(None, "test"))


if __name__ == '__main__':
    unittest.main()
