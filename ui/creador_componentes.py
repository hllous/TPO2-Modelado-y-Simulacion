"""
Fabrica de componentes UI para evitar repetición
Centraliza creación de elementos comunes
"""

import tkinter as tk
from tkinter import ttk
from ui.estilos import COLORES, FUENTES, ESPACIOS
from ui.widgets import ToolTip


class CreadorPaneles:
    """Factory para crear paneles estándar"""
    
    @staticmethod
    def panel_entrada_doble(parent, label1, label2, var1, var2, titulo=None):
        """Crea panel con dos entradas"""
        frame = ttk.LabelFrame(parent, text=titulo or "Entrada", padding=f"{ESPACIOS['md']}")
        frame.pack(fill=tk.X, pady=ESPACIOS['sm'])
        
        # Primera entrada
        row1 = ttk.Frame(frame)
        row1.pack(fill=tk.X, pady=ESPACIOS['xs'])
        ttk.Label(row1, text=label1, font=FUENTES['normal']).pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        entry1 = ttk.Entry(row1, textvariable=var1, width=15)
        entry1.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        
        # Segunda entrada
        row2 = ttk.Frame(frame)
        row2.pack(fill=tk.X, pady=ESPACIOS['xs'])
        ttk.Label(row2, text=label2, font=FUENTES['normal']).pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        entry2 = ttk.Entry(row2, textvariable=var2, width=15)
        entry2.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        
        return frame, entry1, entry2
    
    @staticmethod
    def panel_opciones(parent, opciones, titulo=None, orientacion=tk.VERTICAL):
        """Crea panel de opciones (radio buttons)"""
        frame = ttk.LabelFrame(parent, text=titulo or "Opciones", padding=f"{ESPACIOS['md']}")
        frame.pack(fill=tk.X, pady=ESPACIOS['sm'])
        
        var = tk.StringVar(value=opciones[0][0] if opciones else "")
        
        for valor, label in opciones:
            rb = ttk.Radiobutton(frame, text=label, variable=var, value=valor)
            if orientacion == tk.HORIZONTAL:
                rb.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
            else:
                rb.pack(anchor=tk.W, pady=ESPACIOS['xs'])
        
        return frame, var
    
    @staticmethod
    def panel_controles(parent, controles_config):
        """
        Crea panel de controles dinámicamente
        
        Parámetros:
        - controles_config: list de dicts
            [
                {'tipo': 'entrada', 'label': str, 'variable': tk.Variable},
                {'tipo': 'checkbox', 'label': str, 'variable': tk.BooleanVar},
                {'tipo': 'slider', 'label': str, 'variable': tk.Variable, 'min': int, 'max': int},
            ]
        """
        frame = ttk.LabelFrame(parent, text="Controles", padding=f"{ESPACIOS['md']}")
        frame.pack(fill=tk.X, pady=ESPACIOS['sm'])
        
        widgets_creados = {}
        
        for i, config in enumerate(controles_config):
            tipo = config.get('tipo', 'entrada')
            label = config.get('label', 'Parámetro')
            variable = config.get('variable')
            
            # Frame para cada control
            control_frame = ttk.Frame(frame)
            control_frame.pack(fill=tk.X, pady=ESPACIOS['xs'])
            
            ttk.Label(control_frame, text=label + ":", font=FUENTES['normal']).pack(side=tk.LEFT, padx=ESPACIOS['sm'])
            
            if tipo == 'entrada':
                entry = ttk.Entry(control_frame, textvariable=variable, width=15)
                entry.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
                widgets_creados[label] = entry
            
            elif tipo == 'checkbox':
                check = ttk.Checkbutton(control_frame, variable=variable)
                check.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
                widgets_creados[label] = check
            
            elif tipo == 'slider':
                scale = ttk.Scale(
                    control_frame,
                    from_=config.get('min', 0),
                    to=config.get('max', 10),
                    variable=variable,
                    orient=tk.HORIZONTAL
                )
                scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=ESPACIOS['sm'])
                widgets_creados[label] = scale
            
            elif tipo == 'combobox':
                combo = ttk.Combobox(
                    control_frame,
                    textvariable=variable,
                    values=config.get('valores', []),
                    state='readonly',
                    width=15
                )
                combo.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
                widgets_creados[label] = combo
        
        return frame, widgets_creados
    
    @staticmethod
    def panel_botones(parent, botones_config, titulo=None):
        """
        Crea panel de botones
        
        Parámetros:
        - botones_config: list de dicts
            [
                {'texto': str, 'comando': callable, 'color': str (opt)},
            ]
        """
        frame = ttk.Frame(parent)
        if titulo:
            frame = ttk.LabelFrame(parent, text=titulo, padding=f"{ESPACIOS['md']}")
        frame.pack(fill=tk.X, pady=ESPACIOS['sm'])
        
        botones_creados = {}
        
        for config in botones_config:
            btn = tk.Button(
                frame,
                text=config['texto'],
                command=config['comando'],
                bg=config.get('color', COLORES['primario']),
                fg='white',
                relief=tk.FLAT,
                cursor='hand2',
                font=FUENTES['normal_bold'],
                padx=ESPACIOS['md'],
                pady=ESPACIOS['sm'],
                activebackground=config.get('activebackground', COLORES['primario_hover']),
                activeforeground='white'
            )
            btn.pack(fill=tk.X, pady=ESPACIOS['xs'])
            botones_creados[config['texto']] = btn
        
        return frame, botones_creados


class CreadorTablas:
    """Factory para crear tablas/grillas de datos"""
    
    @staticmethod
    def tabla_simple(parent, columnas, datos):
        """
        Crea tabla simple con datos
        
        Parámetros:
        - columnas: list de nombres de columnas
        - datos: list de filas (cada fila es una list)
        """
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=ESPACIOS['sm'], pady=ESPACIOS['sm'])
        
        # Headers
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill=tk.X)
        
        for col in columnas:
            label = tk.Label(
                header_frame,
                text=col,
                font=FUENTES['normal_bold'],
                bg=COLORES['primario'],
                fg='white',
                padx=ESPACIOS['sm'],
                pady=ESPACIOS['xs'],
                relief=tk.SOLID,
                bd=1
            )
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Datos
        for fila in datos:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X)
            
            for valor in fila:
                label = tk.Label(
                    row_frame,
                    text=str(valor),
                    font=FUENTES['pequena'],
                    padx=ESPACIOS['sm'],
                    pady=ESPACIOS['xs'],
                    relief=tk.SOLID,
                    bd=1
                )
                label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        return frame


class CreadorResultados:
    """Factory para crear paneles de resultados"""
    
    @staticmethod
    def panel_resumen(parent, items):
        """
        Crea panel resumen con items
        
        Parámetros:
        - items: dict {label: valor}
        """
        frame = ttk.LabelFrame(parent, text="Resumen", padding=f"{ESPACIOS['md']}")
        frame.pack(fill=tk.X, pady=ESPACIOS['sm'])
        
        for label, valor in items.items():
            item_frame = ttk.Frame(frame)
            item_frame.pack(fill=tk.X, pady=ESPACIOS['xs'])
            
            ttk.Label(item_frame, text=f"{label}:", font=FUENTES['normal_bold']).pack(side=tk.LEFT, padx=ESPACIOS['sm'])
            ttk.Label(item_frame, text=str(valor), font=FUENTES['normal'], foreground=COLORES['primario']).pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        
        return frame
    
    @staticmethod
    def panel_texto_resultado(parent, titulo, texto):
        """Crea panel con texto de resultado"""
        frame = ttk.LabelFrame(parent, text=titulo, padding=f"{ESPACIOS['md']}")
        frame.pack(fill=tk.BOTH, expand=True, pady=ESPACIOS['sm'])
        
        # Crear widget de texto con scrollbar
        from tkinter import scrolledtext
        text_widget = scrolledtext.ScrolledText(
            frame,
            font=FUENTES['monoespaciada_pequena'],
            bg=COLORES['fondo'],
            fg=COLORES['texto_principal'],
            height=15,
            width=60
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', texto)
        text_widget.config(state=tk.DISABLED)
        
        return text_widget
