"""
Configuración centralizada de estilos para ttk
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
        font=('Arial', 10, 'bold'),
        padding=10
    )
    style.map('Accent.TButton', background=[('active', '#1976D2')])
    
    # Estilo frame tipo tarjeta
    style.configure(
        'Card.TFrame',
        background='white',
        relief='flat',
        borderwidth=2
    )
    
    # Estilo título
    style.configure(
        'Title.TLabel',
        background='white',
        font=('Arial', 12, 'bold'),
        foreground='#333333'
    )
    
    # Estilo subtítulo
    style.configure(
        'Subtitle.TLabel',
        background='white',
        font=('Arial', 10),
        foreground='#666666'
    )
    
    return style


# Configuración de colores
COLORES = {
    'primario': '#2196F3',
    'primario_hover': '#1976D2',
    'fondo': '#f0f0f0',
    'tarjeta': '#ffffff',
    'texto_principal': '#333333',
    'texto_secundario': '#666666',
    'exito': '#2E7D32',
    'error': '#C62828',
    'advertencia': '#F57C00'
}


# Configuración de fuentes
FUENTES = {
    'titulo': ('Arial', 16, 'bold'),
    'titulo_seccion': ('Arial', 12, 'bold'),
    'normal': ('Arial', 10),
    'pequena': ('Arial', 9),
    'monoespaciada': ('Consolas', 10)
}
