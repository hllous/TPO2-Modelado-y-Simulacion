"""
Módulo core: contiene la lógica matemática del sistema dinámico
"""
try:
    from .sistema import SistemaDinamico2D
    from .bifurcacion import AnalizadorBifurcacion
except ImportError:
    from sistema import SistemaDinamico2D
    from bifurcacion import AnalizadorBifurcacion

__all__ = ['SistemaDinamico2D', 'AnalizadorBifurcacion']
