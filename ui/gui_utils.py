"""
Utilidades compartidas para interfaces gráficas
Elimina código duplicado entre módulos GUI
"""

import tkinter as tk
from tkinter import ttk
from ui.estilos import COLORES, FUENTES, ESPACIOS


def crear_frame_parametro(parent, label, variable, ancho=10, tooltip_text=None):
    """
    Crea un frame con label y entry de forma DRY
    
    Args:
        parent: widget padre
        label: texto de la etiqueta
        variable: StringVar o similar
        ancho: ancho del entry
        tooltip_text: texto de ayuda (opcional)
    
    Returns:
        frame, entry
    """
    from ui.widgets import ToolTip
    
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=label, font=FUENTES['normal']).pack(side=tk.LEFT, padx=(0, ESPACIOS['sm']))
    
    entry = ttk.Entry(frame, textvariable=variable, width=ancho)
    entry.pack(side=tk.LEFT)
    
    if tooltip_text:
        ToolTip(entry, tooltip_text)
    
    return frame, entry


def crear_frame_rango_numerico(parent, titulo, var_min, var_max, 
                               on_change=None, width=8):
    """
    Crea frame para entrada de rango numérico (min-max)
    Patrón común en visualización
    
    Args:
        parent: widget padre
        titulo: nombre del rango (ej: "Eje X")
        var_min, var_max: DoubleVar
        on_change: callback al cambiar valores
        width: ancho de los entry
    
    Returns:
        frame del rango
    """
    frame = ttk.LabelFrame(parent, text=titulo, padding=f"{ESPACIOS['sm']}")
    
    # Min
    ttk.Label(frame, text="Min:", font=FUENTES['pequena']).pack(side=tk.LEFT, padx=ESPACIOS['sm'])
    entry_min = ttk.Entry(frame, textvariable=var_min, width=width)
    entry_min.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
    if on_change:
        entry_min.bind('<Return>', on_change)
    
    # Max
    ttk.Label(frame, text="Max:", font=FUENTES['pequena']).pack(side=tk.LEFT, padx=ESPACIOS['sm'])
    entry_max = ttk.Entry(frame, textvariable=var_max, width=width)
    entry_max.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
    if on_change:
        entry_max.bind('<Return>', on_change)
    
    return frame


def crear_header_modulo(parent, titulo, botones=None):
    """
    Crea header estándar para módulos
    
    Args:
        parent: widget padre
        titulo: título del módulo
        botones: list de (texto, comando) para botones
    
    Returns:
        header_frame
    """
    header = ttk.Frame(parent)
    header.pack(fill=tk.X, pady=(0, ESPACIOS['md']))
    
    ttk.Label(header, text=titulo, font=FUENTES['titulo_modulo']).pack(side=tk.LEFT)
    
    if botones:
        for texto, comando in botones:
            btn = ttk.Button(header, text=texto, command=comando)
            btn.pack(side=tk.RIGHT, padx=ESPACIOS['sm'])
    
    return header


def crear_entrada_ecuacion(parent, label, variable, tooltip=None):
    """
    Crea entrada estándar para ecuaciones/funciones
    
    Args:
        parent: widget padre
        label: etiqueta
        variable: StringVar
        tooltip: ayuda opcional
    
    Returns:
        frame, entry
    """
    from ui.widgets import ToolTip
    
    frame = ttk.Frame(parent)
    
    ttk.Label(frame, text=label, font=FUENTES['normal']).pack(side=tk.LEFT, padx=(0, ESPACIOS['sm']))
    
    entry = ttk.Entry(frame, textvariable=variable, width=40)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    if tooltip:
        ToolTip(entry, tooltip)
    
    return frame, entry


def mostrar_paso_analisis(parent, numero, titulo, *contenido):
    """
    Crea widget para mostrar un paso del análisis
    Patrón común entre análisis de Hamilton, Bifurcaciones, etc.
    
    Args:
        parent: widget padre
        numero: número del paso
        titulo: título del paso
        *contenido: líneas de contenido
    """
    frame = ttk.LabelFrame(
        parent,
        text=f"Paso {numero}: {titulo}",
        padding=f"{ESPACIOS['md']}"
    )
    frame.pack(fill=tk.X, pady=ESPACIOS['md'])
    
    for linea in contenido:
        label = tk.Label(
            frame,
            text=str(linea),
            font=FUENTES['monoespaciada_pequena'],
            justify=tk.LEFT,
            wraplength=600,
            bg=COLORES['fondo'],
            fg=COLORES['texto_principal']
        )
        label.pack(anchor=tk.W, pady=ESPACIOS['xs'])


def validar_numero(valor):
    """Valida que un string sea un número válido"""
    if valor == "" or valor == "-" or valor == ".":
        return True
    try:
        float(valor)
        return True
    except ValueError:
        return False


def validar_numero_entero(valor):
    """Valida que un string sea un entero válido"""
    if valor == "" or valor == "-":
        return True
    try:
        int(valor)
        return True
    except ValueError:
        return False


def crear_separador(parent, orient=tk.HORIZONTAL):
    """Crea separador estándar"""
    sep = ttk.Separator(parent, orient=orient)
    if orient == tk.HORIZONTAL:
        sep.pack(fill=tk.X, pady=ESPACIOS['md'])
    else:
        sep.pack(fill=tk.Y, padx=ESPACIOS['md'])
    return sep


def crear_etiqueta_informativa(parent, texto, tipo='info'):
    """
    Crea etiqueta informativa con icono y color
    
    Args:
        parent: widget padre
        texto: texto a mostrar
        tipo: 'info', 'exito', 'error', 'advertencia'
    """
    colores_tipo = {
        'info': COLORES['info'],
        'exito': COLORES['exito'],
        'error': COLORES['error'],
        'advertencia': COLORES['advertencia']
    }
    
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, pady=ESPACIOS['sm'], padx=ESPACIOS['sm'])
    
    label = tk.Label(
        frame,
        text=texto,
        font=FUENTES['pequena'],
        fg=colores_tipo.get(tipo, COLORES['info']),
        bg=COLORES['fondo'],
        justify=tk.LEFT,
        wraplength=400
    )
    label.pack(anchor=tk.W)
    
    return frame

