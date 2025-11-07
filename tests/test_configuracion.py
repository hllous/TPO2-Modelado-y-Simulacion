"""
Tests para configuración y componentes
"""

import unittest
from config import (
    CONFIG_VENTANAS, CONFIG_GRAFICOS, CONFIG_VALIDACION,
    MENSAJES_ERROR, MENSAJES_EXITO, VALORES_INICIALES,
    obtener_config_ventana, obtener_mensaje_error, obtener_mensaje_exito
)


class TestConfiguracion(unittest.TestCase):
    """Tests para configuración centralizada"""
    
    def test_config_ventana_existe(self):
        """Verifica que existan configuraciones de ventana"""
        self.assertIsNotNone(CONFIG_VENTANAS)
        self.assertIn('principal', CONFIG_VENTANAS)
        self.assertIn('2d', CONFIG_VENTANAS)
    
    def test_obtener_config_ventana(self):
        """Test función obtener_config_ventana"""
        config = obtener_config_ventana('2d')
        self.assertIn('titulo', config)
        self.assertIn('ancho', config)
        self.assertIn('alto', config)
    
    def test_config_graficos(self):
        """Verifica configuración de gráficos"""
        self.assertIsNotNone(CONFIG_GRAFICOS)
        self.assertEqual(CONFIG_GRAFICOS['figura_tamano'], (8, 6))
        self.assertGreater(CONFIG_GRAFICOS['dpi'], 0)
    
    def test_mensajes_error(self):
        """Verifica mensajes de error"""
        self.assertIsNotNone(MENSAJES_ERROR)
        self.assertTrue(len(MENSAJES_ERROR) > 0)
        
        # Probar obtener mensaje
        msg = obtener_mensaje_error('entrada_vacia')
        self.assertIsNotNone(msg)
        self.assertTrue(len(msg) > 0)
    
    def test_mensajes_exito(self):
        """Verifica mensajes de éxito"""
        self.assertIsNotNone(MENSAJES_EXITO)
        self.assertTrue(len(MENSAJES_EXITO) > 0)
        
        # Probar obtener mensaje
        msg = obtener_mensaje_exito('analisis_completo')
        self.assertIsNotNone(msg)
        self.assertTrue(len(msg) > 0)
    
    def test_valores_iniciales(self):
        """Verifica valores iniciales"""
        self.assertIsNotNone(VALORES_INICIALES)
        self.assertIn('matriz_2d', VALORES_INICIALES)
        self.assertIn('funcion_1d', VALORES_INICIALES)


class TestValidacionConfig(unittest.TestCase):
    """Tests para validación de configuración"""
    
    def test_todas_ventanas_tienen_dimensiones(self):
        """Verifica que todas las ventanas tengan dimensiones"""
        for tipo, config in CONFIG_VENTANAS.items():
            self.assertIn('ancho', config)
            self.assertIn('alto', config)
            self.assertGreater(config['ancho'], 0)
            self.assertGreater(config['alto'], 0)
    
    def test_validacion_limits(self):
        """Verifica límites de validación"""
        self.assertLess(CONFIG_VALIDACION['min_valor'], CONFIG_VALIDACION['max_valor'])
        self.assertGreater(CONFIG_VALIDACION['precision_decimal'], 0)
        self.assertGreater(CONFIG_VALIDACION['max_iteraciones'], 0)


if __name__ == '__main__':
    unittest.main()
