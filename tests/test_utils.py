"""
Tests para utilidades de core
"""

import unittest
import numpy as np
from core.utils import (
    normalizar_funciones, validar_expresion_matematica,
    evaluar_expresion, calcular_jacobiano, analizar_estabilidad_punto,
    clasificar_equilibrio
)


class TestUtilidades(unittest.TestCase):
    """Tests para funciones de utilidad"""
    
    def test_normalizar_funciones(self):
        """Test normalización de funciones"""
        self.assertEqual(normalizar_funciones("sen(x)"), "sin(x)")
        self.assertEqual(normalizar_funciones("x**2"), "x**2")
    
    def test_validar_expresion_valida(self):
        """Test validación de expresiones válidas"""
        valida, error = validar_expresion_matematica("x + y")
        self.assertTrue(valida)
        self.assertIsNone(error)
        
        valida, error = validar_expresion_matematica("sin(x) + cos(y)")
        self.assertTrue(valida)
    
    def test_validar_expresion_invalida(self):
        """Test validación de expresiones inválidas"""
        valida, error = validar_expresion_matematica("x ++ y")
        self.assertFalse(valida)
    
    def test_evaluar_expresion(self):
        """Test evaluación de expresiones"""
        resultado = evaluar_expresion("x + y", {'x': 2, 'y': 3})
        self.assertEqual(resultado, 5)
        
        resultado = evaluar_expresion("x**2", {'x': 3})
        self.assertEqual(resultado, 9)
    
    def test_calcular_jacobiano(self):
        """Test cálculo de jacobiano"""
        # Sistema lineal simple
        jac = calcular_jacobiano("-x", "-y", (1, 1))
        self.assertEqual(jac.shape, (2, 2))
        
        # Verificar que los valores sean cercanos a los esperados
        self.assertAlmostEqual(jac[0, 0], -1, places=3)
        self.assertAlmostEqual(jac[1, 1], -1, places=3)
    
    def test_analizar_estabilidad(self):
        """Test análisis de estabilidad"""
        # Matriz con eigenvalores negativos (estable)
        matriz = np.array([[-1, 0], [0, -2]])
        resultado = analizar_estabilidad_punto(matriz)
        
        self.assertTrue(resultado['estable'])
        self.assertIn('eigenvalores', resultado)
        self.assertIn('traza', resultado)
        self.assertIn('determinante', resultado)
    
    def test_clasificar_equilibrio(self):
        """Test clasificación de equilibrios"""
        # Silla (determinante negativo)
        eigenvalores = np.array([1, -1])
        tipo = clasificar_equilibrio(eigenvalores, 0, -1)
        self.assertEqual(tipo, 'silla')
        
        # Nodo estable
        eigenvalores = np.array([-1, -2])
        tipo = clasificar_equilibrio(eigenvalores, -3, 2)
        self.assertEqual(tipo, 'nodo_estable')


class TestEvaluacionSegura(unittest.TestCase):
    """Tests para evaluación segura de expresiones"""
    
    def test_evaluacion_con_funciones_trigonometricas(self):
        """Test funciones trigonométricas"""
        resultado = evaluar_expresion("sin(x)", {'x': 0})
        self.assertAlmostEqual(resultado, 0, places=5)
        
        resultado = evaluar_expresion("cos(x)", {'x': 0})
        self.assertAlmostEqual(resultado, 1, places=5)
    
    def test_evaluacion_con_exponenciales(self):
        """Test funciones exponenciales"""
        resultado = evaluar_expresion("exp(x)", {'x': 0})
        self.assertAlmostEqual(resultado, 1, places=5)
    
    def test_evaluacion_con_sqrt(self):
        """Test raíz cuadrada"""
        resultado = evaluar_expresion("sqrt(x)", {'x': 4})
        self.assertAlmostEqual(resultado, 2, places=5)
    
    def test_evaluacion_error_manejo(self):
        """Test manejo de errores en evaluación"""
        with self.assertRaises(ValueError):
            evaluar_expresion("sqrt(x)", {'x': -1})


if __name__ == '__main__':
    unittest.main()
