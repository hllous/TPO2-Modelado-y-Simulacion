"""
Módulo ui: componentes y estilos de la interfaz gráfica
"""
try:
    from .widgets import ToolTip
    from .estilos import configurar_estilos_ttk
except ImportError:
    from widgets import ToolTip
    from estilos import configurar_estilos_ttk

__all__ = ['ToolTip', 'configurar_estilos_ttk']
