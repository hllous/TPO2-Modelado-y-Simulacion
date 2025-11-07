"""
Tests para análisis de sistemas dinámicos
"""

import unittest
import numpy as np
from core.sistema import SistemaDinamico2D


class TestSistemaDinamico2D(unittest.TestCase):
    """Tests para sistema dinámico 2D"""
    
    def setUp(self):
        """Configura sistema de prueba"""
        self.matriz = np.array([[-1, 0], [0, -2]])
        self.sistema = SistemaDinamico2D(self.matriz)
    
    def test_creacion_sistema(self):
        """Prueba creación del sistema"""
        self.assertIsNotNone(self.sistema)
        np.testing.assert_array_equal(self.sistema.matriz, self.matriz)
    
    def test_ecuaciones_sistema(self):
        """Prueba que las ecuaciones se evalúan correctamente"""
        estado = np.array([1, 1])
        resultado = self.sistema.sistema_ecuaciones(estado, 0)
        esperado = self.matriz @ estado
        np.testing.assert_array_almost_equal(resultado, esperado)
    
    def test_sistema_con_termino_forzado(self):
        """Prueba sistema con término forzado"""
        coef_forzado = np.array([0.5, 0.5])
        sistema_forzado = SistemaDinamico2D(self.matriz, coef_forzado=coef_forzado)
        self.assertIsNotNone(sistema_forzado)


class TestValidacionSistema(unittest.TestCase):
    """Tests para validación de entrada del sistema"""
    
    def test_matriz_cuadrada(self):
        """Verifica que la matriz sea cuadrada 2x2"""
        matriz = np.array([[1, 2], [3, 4]])
        sistema = SistemaDinamico2D(matriz)
        self.assertEqual(sistema.matriz.shape, (2, 2))
    
    def test_manejo_valores_nulos(self):
        """Prueba que el sistema maneja valores cero correctamente"""
        matriz = np.array([[0, 0], [0, 0]])
        sistema = SistemaDinamico2D(matriz)
        estado = np.array([1, 1])
        resultado = sistema.sistema_ecuaciones(estado, 0)
        np.testing.assert_array_equal(resultado, np.array([0, 0]))


if __name__ == '__main__':
    unittest.main()
