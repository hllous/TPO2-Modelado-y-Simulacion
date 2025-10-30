"""
Módulo core: contiene la lógica matemática del sistema dinámico
"""
try:
    from .sistema import SistemaDinamico2D
except ImportError:
    from sistema import SistemaDinamico2D

__all__ = ['SistemaDinamico2D']
