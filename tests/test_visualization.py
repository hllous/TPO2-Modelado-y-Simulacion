"""
Tests para visualización y gráficos
"""

import unittest
import numpy as np
from matplotlib.figure import Figure


class TestVisualizacion(unittest.TestCase):
    """Tests básicos para visualización"""
    
    def test_creacion_figura(self):
        """Prueba creación de figura matplotlib"""
        fig = Figure(figsize=(8, 6), dpi=100)
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.axes), 0)
    
    def test_subplot_creation(self):
        """Prueba creación de subplots"""
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        self.assertIsNotNone(ax)
        self.assertEqual(len(fig.axes), 1)
    
    def test_plot_data(self):
        """Prueba graficar datos"""
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        ax.plot(x, y)
        self.assertEqual(len(ax.lines), 1)


class TestDatosVisualizacion(unittest.TestCase):
    """Tests para datos de visualización"""
    
    def test_normalizacion_datos(self):
        """Prueba normalización de datos para visualización"""
        datos = np.array([1, 2, 3, 4, 5])
        min_val = datos.min()
        max_val = datos.max()
        
        self.assertEqual(min_val, 1)
        self.assertEqual(max_val, 5)
    
    def test_generacion_malla(self):
        """Prueba generación de malla para campos"""
        x = np.linspace(-5, 5, 20)
        y = np.linspace(-5, 5, 20)
        X, Y = np.meshgrid(x, y)
        
        self.assertEqual(X.shape, (20, 20))
        self.assertEqual(Y.shape, (20, 20))


if __name__ == '__main__':
    unittest.main()
