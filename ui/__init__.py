"""
Módulo ui: componentes y estilos de la interfaz gráfica
"""
try:
    from .widgets import ToolTip
    from .estilos import configurar_estilos_ttk
    from .widget_utils import PanelAnalisisBase, ConstructorUI, FormularioParametros
except ImportError:
    from widgets import ToolTip
    from estilos import configurar_estilos_ttk
    from widget_utils import PanelAnalisisBase, ConstructorUI, FormularioParametros

__all__ = ['ToolTip', 'configurar_estilos_ttk', 'PanelAnalisisBase', 'ConstructorUI', 'FormularioParametros']
