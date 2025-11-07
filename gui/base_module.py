"""
Clase base reutilizable para todos los módulos GUI
Implementa patrón DRY eliminando código duplicado
"""

import tkinter as tk
from tkinter import ttk
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES


class ModuloBase:
    """Base para todos los módulos GUI - implementa estructura común"""
    
    def __init__(self, root, titulo=None):
        """
        Inicializa módulo base
        
        Parámetros:
        - root: ventana raíz o frame padre
        - titulo: título del módulo (para ventana)
        """
        self.root = root
        self.titulo = titulo or "Módulo"
        self._configurar_ventana()
        self._inicializar_variables()
    
    def _configurar_ventana(self):
        """Configura la ventana/frame de forma estándar"""
        if isinstance(self.root, tk.Tk):
            self.root.title(self.titulo)
            self.root.geometry("1400x800")
            self.root.configure(bg=COLORES['fondo'])
            configurar_estilos_ttk()
            self.es_ventana = True
        else:
            if isinstance(self.root, tk.Frame):
                self.root.configure(bg=COLORES['fondo'])
            self.es_ventana = False
    
    def _inicializar_variables(self):
        """Inicializa variables - sobrescribir en subclases"""
        pass
    
    def _crear_layout_principal(self):
        """Crea layout estándar: panel izquierdo (controles) y derecho (contenido)"""
        main_frame = ttk.Frame(self.root, padding="10")
        
        if self.es_ventana:
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
            main_frame.rowconfigure(0, weight=1)
        else:
            main_frame.pack(fill=tk.BOTH, expand=True)
        
        return main_frame
    
    def _crear_panel_izquierdo(self, parent):
        """Crea panel izquierdo estándar (sobrescribir en subclases)"""
        if self.es_ventana:
            panel = ttk.Frame(parent, padding="5")
            panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        else:
            panel = ttk.Frame(parent, padding="5")
            panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        return panel
    
    def _crear_panel_derecho(self, parent):
        """Crea panel derecho estándar (sobrescribir en subclases)"""
        if self.es_ventana:
            panel = ttk.Frame(parent)
            panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
            parent.columnconfigure(1, weight=1)
        else:
            panel = ttk.Frame(parent)
            panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        return panel
    
    def _crear_boton_estandar(self, parent, texto, comando, color=None, **kwargs):
        """Crea botón con estilo estándar"""
        color = color or COLORES['primario']
        
        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=color,
            fg='white',
            padx=kwargs.get('padx', 15),
            pady=kwargs.get('pady', 10),
            relief=tk.FLAT,
            cursor='hand2',
            font=kwargs.get('font', FUENTES['normal']),
            activebackground=kwargs.get('activebackground', COLORES['primario_hover']),
            **{k: v for k, v in kwargs.items() if k not in ['padx', 'pady', 'font', 'activebackground']}
        )
        
        return btn
    
    def _crear_seccion(self, parent, titulo, rellenar=True):
        """Crea sección con título"""
        frame = ttk.LabelFrame(parent, text=titulo, padding="10")
        
        if rellenar:
            if isinstance(parent.master, ttk.Frame):
                frame.pack(fill=tk.BOTH, expand=True, pady=5)
            else:
                frame.pack(fill=tk.X, pady=5)
        else:
            frame.pack(pady=5)
        
        return frame
    
    def _crear_titulo(self, parent, texto, tamaño='titulo'):
        """Crea etiqueta de título"""
        label = tk.Label(
            parent,
            text=texto,
            font=FUENTES.get(tamaño, FUENTES['titulo']),
            fg=COLORES['texto_principal'],
            bg=COLORES['fondo']
        )
        label.pack(pady=10)
        return label
    
    def _criar_entrada_parametro(self, parent, etiqueta, variable, ancho=10):
        """Crea entrada de parámetro estándar"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=3)
        
        ttk.Label(frame, text=etiqueta, font=FUENTES['normal']).pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(frame, textvariable=variable, width=ancho)
        entry.pack(side=tk.LEFT, padx=5)
        
        return entry
    
    def limpiar_widget(self, widget):
        """Limpia todos los widgets hijos"""
        for child in widget.winfo_children():
            child.destroy()
    
    def obtener_ventana_root(self):
        """Obtiene la ventana raíz Tk"""
        widget = self.root
        while not isinstance(widget, tk.Tk):
            widget = widget.master
        return widget
