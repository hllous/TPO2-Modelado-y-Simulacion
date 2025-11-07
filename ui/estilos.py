"""
Configuración centralizada de estilos para ttk
Diseño moderno y consistente
"""

from tkinter import ttk


def configurar_estilos_ttk():
    """Configura todos los estilos de ttk de forma centralizada"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Estilo botón acentuado
    style.configure(
        'Accent.TButton',
        background='#2196F3',
        foreground='white',
        borderwidth=0,
        focuscolor='none',
        font=('Segoe UI', 10, 'bold'),
        padding=12
    )
    style.map('Accent.TButton', background=[('active', '#1976D2'), ('pressed', '#0D47A1')])
    
    # Estilo frame tipo tarjeta
    style.configure(
        'Card.TFrame',
        background='white',
        relief='flat',
        borderwidth=1
    )
    
    # Estilo título
    style.configure(
        'Title.TLabel',
        background='#f0f0f0',
        font=('Segoe UI', 12, 'bold'),
        foreground='#1a1a1a'
    )
    
    # Estilo subtítulo
    style.configure(
        'Subtitle.TLabel',
        background='#f0f0f0',
        font=('Segoe UI', 10),
        foreground='#555555'
    )
    
    # Frame mejorado
    style.configure(
        'Tframe',
        background='#f0f0f0',
        relief='flat'
    )
    
    # Label mejorado
    style.configure(
        'TLabel',
        background='#f0f0f0',
        font=('Segoe UI', 9),
        foreground='#333333'
    )
    
    # Entry mejorado
    style.configure(
        'TEntry',
        fieldbackground='white',
        foreground='#333333',
        font=('Segoe UI', 9),
        padding=6
    )
    
    # Button mejorado
    style.configure(
        'TButton',
        font=('Segoe UI', 9),
        padding=8
    )
    style.map('TButton', background=[('active', '#e0e0e0')])
    
    # Combobox mejorado
    style.configure(
        'TCombobox',
        fieldbackground='white',
        background='white',
        foreground='#333333',
        font=('Segoe UI', 9)
    )
    
    # LabelFrame mejorado
    style.configure(
        'TLabelframe',
        background='#f0f0f0',
        foreground='#1a1a1a',
        font=('Segoe UI', 10, 'bold'),
        relief='solid',
        borderwidth=1
    )
    
    style.configure(
        'TLabelframe.Label',
        background='#f0f0f0',
        foreground='#2196F3',
        font=('Segoe UI', 10, 'bold')
    )
    
    return style


# Configuración de colores - Paleta moderna
COLORES = {
    'primario': '#2196F3',
    'primario_hover': '#1976D2',
    'primario_oscuro': '#0D47A1',
    'secundario': '#4CAF50',
    'fondo': '#f5f5f5',
    'fondo_claro': '#fafafa',
    'tarjeta': '#ffffff',
    'texto_principal': '#212121',
    'texto_secundario': '#757575',
    'texto_deshabilitado': '#bdbdbd',
    'exito': '#4CAF50',
    'error': '#f44336',
    'advertencia': '#ff9800',
    'info': '#2196F3',
    'borde': '#e0e0e0',
    'sombra': '#cccccc'
}


# Configuración de fuentes - Mejorada
FUENTES = {
    'titulo': ('Segoe UI', 18, 'bold'),
    'titulo_modulo': ('Segoe UI', 16, 'bold'),
    'titulo_seccion': ('Segoe UI', 13, 'bold'),
    'normal': ('Segoe UI', 10),
    'normal_bold': ('Segoe UI', 10, 'bold'),
    'pequena': ('Segoe UI', 9),
    'muy_pequena': ('Segoe UI', 8),
    'monoespaciada': ('Consolas', 10),
    'monoespaciada_pequena': ('Consolas', 9)
}


# Espaciados estándar
ESPACIOS = {
    'xs': 2,
    'sm': 5,
    'md': 10,
    'lg': 15,
    'xl': 20,
    'xxl': 30
}
