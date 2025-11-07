"""
Utilidades DRY para widgets e interfaz
Centraliza componentes repetidos
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from ui.estilos import COLORES, FUENTES, ESPACIOS


class PanelAnalisisBase:
    """Clase base para paneles de análisis reutilizables"""
    
    @staticmethod
    def crear_ventana_analisis(padre, titulo, ancho=900, alto=700):
        """
        Crea ventana de análisis genérica
        
        Parámetros:
        - padre: ventana padre
        - titulo: título de la ventana
        - ancho, alto: dimensiones
        
        Retorna: (ventana, notebook)
        """
        ventana = tk.Toplevel(padre)
        ventana.title(titulo)
        ventana.geometry(f"{ancho}x{alto}")
        ventana.configure(bg=COLORES['fondo'])
        
        notebook = ttk.Notebook(ventana)
        notebook.pack(fill=tk.BOTH, expand=True, padx=ESPACIOS['md'], pady=ESPACIOS['md'])
        
        return ventana, notebook
    
    @staticmethod
    def crear_pestaña_texto(notebook, titulo_pestaña, contenido):
        """
        Crea pestaña con texto desplazable
        
        Parámetros:
        - notebook: notebook padre
        - titulo_pestaña: texto de la pestaña
        - contenido: texto a mostrar
        """
        frame = ttk.Frame(notebook, padding=f"{ESPACIOS['md']}")
        notebook.add(frame, text=titulo_pestaña)
        
        text_widget = scrolledtext.ScrolledText(
            frame, 
            height=25, 
            width=100,
            font=FUENTES['monoespaciada_pequena'],
            bg=COLORES['fondo'],
            fg=COLORES['texto_principal'],
            insertbackground=COLORES['primario']
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', contenido)
        text_widget.config(state=tk.DISABLED)
        
        return text_widget


class ConstructorUI:
    """Centraliza construcción de elementos UI comunes"""
    
    @staticmethod
    def crear_boton(parent, texto, comando, bg=None, emoji=True, **kwargs):
        """
        Crea botón estilizado
        
        Parámetros:
        - parent: widget padre
        - texto: texto del botón
        - comando: función a ejecutar
        - bg: color de fondo (por defecto primario)
        - emoji: si incluir emoji inicial
        - kwargs: argumentos adicionales
        
        Retorna: botón tkinter
        """
        bg = bg or COLORES['primario']
        
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=bg,
            fg='white',
            padx=kwargs.get('padx', ESPACIOS['md']),
            pady=kwargs.get('pady', ESPACIOS['sm']),
            relief=tk.FLAT,
            cursor='hand2',
            font=kwargs.get('font', FUENTES['normal_bold']),
            activebackground=kwargs.get('activebackground', COLORES['primario_hover']),
            activeforeground='white',
            bd=0,
            highlightthickness=0
        )
        
        return btn
    
    @staticmethod
    def crear_entrada_parametro(parent, nombre, valor_inicial, min_val=None, 
                               max_val=None, callback=None):
        """
        Crea widget de entrada de parámetro con escala opcional
        
        Parámetros:
        - parent: widget padre
        - nombre: nombre del parámetro
        - valor_inicial: valor inicial
        - min_val, max_val: rango para escala (opcional)
        - callback: función callback al cambiar
        
        Retorna: variable tkinter
        """
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=ESPACIOS['sm'], pady=ESPACIOS['xs'])
        
        label = ttk.Label(frame, text=nombre + ":", font=FUENTES['normal'])
        label.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        
        var = tk.DoubleVar(value=valor_inicial)
        
        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        
        if min_val is not None and max_val is not None:
            scale = ttk.Scale(
                frame, 
                from_=min_val, 
                to=max_val,
                variable=var,
                orient=tk.HORIZONTAL,
                command=callback
            )
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=ESPACIOS['sm'])
        
        return var


class FormularioParametros:
    """Crea formularios parametrizables de entrada"""
    
    def __init__(self, parent, parametros_config):
        """
        Inicializa formulario
        
        Parámetros:
        - parent: widget padre
        - parametros_config: dict con configuración de parámetros
            {
                'nombre_param': {
                    'etiqueta': str,
                    'inicial': float,
                    'minimo': float,
                    'maximo': float,
                    'tipo': 'float|int|bool' (default: float)
                },
                ...
            }
        """
        self.parent = parent
        self.config = parametros_config
        self.variables = {}
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Construye widgets del formulario"""
        frame = ttk.LabelFrame(self.parent, text="Parámetros", padding=f"{ESPACIOS['md']}")
        frame.pack(fill=tk.BOTH, expand=True, padx=ESPACIOS['sm'], pady=ESPACIOS['sm'])
        
        for i, (param_key, param_info) in enumerate(self.config.items()):
            # Etiqueta
            label_text = param_info.get('etiqueta', param_key)
            label = ttk.Label(frame, text=label_text + ":", font=FUENTES['normal'])
            label.grid(row=i, column=0, sticky=tk.W, pady=ESPACIOS['sm'])
            
            # Variable
            param_type = param_info.get('tipo', 'float')
            if param_type == 'bool':
                var = tk.BooleanVar(value=param_info.get('inicial', False))
                widget = ttk.Checkbutton(frame, variable=var)
            else:
                VarClass = tk.DoubleVar if param_type == 'float' else tk.IntVar
                var = VarClass(value=param_info.get('inicial', 0))
                
                # Entry
                entry = ttk.Entry(frame, textvariable=var, width=10)
                entry.grid(row=i, column=1, sticky=tk.W, padx=ESPACIOS['sm'], pady=ESPACIOS['sm'])
                
                # Scale si hay rango
                if 'minimo' in param_info and 'maximo' in param_info:
                    scale = ttk.Scale(
                        frame,
                        from_=param_info['minimo'],
                        to=param_info['maximo'],
                        variable=var,
                        orient=tk.HORIZONTAL
                    )
                    scale.grid(row=i, column=2, sticky=(tk.W, tk.E), padx=ESPACIOS['sm'], pady=ESPACIOS['sm'])
                    frame.columnconfigure(2, weight=1)
                
                widget = entry
            
            if param_type == 'bool':
                widget.grid(row=i, column=1, sticky=tk.W, padx=ESPACIOS['sm'], pady=ESPACIOS['sm'])
            
            self.variables[param_key] = var
    
    def obtener_valores(self):
        """Retorna dict con valores actuales"""
        return {key: var.get() for key, var in self.variables.items()}
    
    def establecer_valores(self, valores):
        """Establece valores del formulario"""
        for key, valor in valores.items():
            if key in self.variables:
                self.variables[key].set(valor)


def crear_panel_botones_estandar(parent, botones_config):
    """
    Crea panel de botones estandarizado
    
    Parámetros:
    - parent: widget padre
    - botones_config: list de dicts
        [
            {'texto': str, 'comando': callable, 'color': str (opt)},
            ...
        ]
    
    Retorna: frame con botones
    """
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, padx=ESPACIOS['sm'], pady=ESPACIOS['sm'])
    
    for config in botones_config:
        btn = ConstructorUI.crear_boton(
            frame,
            config['texto'],
            config['comando'],
            bg=config.get('color', COLORES['primario'])
        )
        btn.pack(fill=tk.X, pady=ESPACIOS['xs'])
    
    return frame


def crear_panel_indicadores(parent, indicadores_config):
    """
    Crea panel con indicadores de estado
    
    Parámetros:
    - parent: widget padre
    - indicadores_config: dict
        {
            'nombre_indicador': valor,
            ...
        }
    
    Retorna: frame con indicadores
    """
    frame = ttk.LabelFrame(parent, text="Indicadores", padding=f"{ESPACIOS['md']}")
    frame.pack(fill=tk.X, padx=ESPACIOS['sm'], pady=ESPACIOS['sm'])
    
    for nombre, valor in indicadores_config.items():
        ind_frame = ttk.Frame(frame)
        ind_frame.pack(fill=tk.X, pady=ESPACIOS['xs'])
        
        label = ttk.Label(ind_frame, text=f"{nombre}:", font=FUENTES['normal'])
        label.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
        
        valor_label = ttk.Label(
            ind_frame,
            text=str(valor),
            font=FUENTES['normal_bold'],
            foreground=COLORES['primario']
        )
        valor_label.pack(side=tk.LEFT, padx=ESPACIOS['sm'])
    
    return frame


def crear_titulo_seccion(parent, titulo):
    """Crea título de sección con formato estándar"""
    label = tk.Label(
        parent,
        text=titulo,
        font=FUENTES['titulo_seccion'],
        fg=COLORES['primario'],
        bg=COLORES['fondo']
    )
    label.pack(anchor=tk.W, pady=(ESPACIOS['md'], ESPACIOS['sm']))
    return label


def crear_descripcion_texto(parent, texto, wraplength=400):
    """Crea texto descriptivo con formato estándar"""
    label = tk.Label(
        parent,
        text=texto,
        font=FUENTES['pequena'],
        fg=COLORES['texto_secundario'],
        bg=COLORES['fondo'],
        justify=tk.LEFT,
        wraplength=wraplength
    )
    label.pack(anchor=tk.W, pady=ESPACIOS['xs'])
    return label

