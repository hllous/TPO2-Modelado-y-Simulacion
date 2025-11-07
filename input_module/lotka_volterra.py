"""
Módulo de entrada para Lotka-Volterra
Centraliza configuración de parámetros
"""

import tkinter as tk
from tkinter import ttk
from ui.gui_utils import crear_separador


class InputLotkaVolterra:
    """Maneja entrada de parámetros para Lotka-Volterra"""
    
    PARAMETROS = {
        'alpha': (0.1, 5.0, 'Tasa crecimiento presas'),
        'beta': (0.01, 1.0, 'Tasa depredación'),
        'gamma': (0.01, 1.0, 'Eficiencia depredador'),
        'delta': (0.1, 5.0, 'Tasa muerte depredador')
    }
    
    VALORES_DEFECTO = [1.0, 0.1, 0.1, 0.5]
    
    def __init__(self, parent):
        """Inicializa el módulo de entrada"""
        self.parent = parent
        self.variables = {}
        self.modo_personalizado = tk.BooleanVar(value=False)
        self.func_presa = tk.StringVar(value="x - beta*x*y")
        self.func_depredador = tk.StringVar(value="gamma*x*y - delta*y")
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea widgets de entrada"""
        # Frame principal
        frame = ttk.LabelFrame(self.parent, text="Parámetros", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Selector de modo
        self._crear_selector_modo(frame)
        
        # Frame de parámetros estándar
        self.frame_parametros = ttk.LabelFrame(frame, text="Lotka-Volterra Estándar", padding="5")
        self.frame_parametros.pack(fill=tk.BOTH, expand=True, pady=5)
        
        for i, (param, (min_val, max_val, desc)) in enumerate(self.PARAMETROS.items()):
            self._crear_fila_parametro(self.frame_parametros, i, param, min_val, max_val, desc, self.VALORES_DEFECTO[i])
        
        # Frame de función personalizada
        self.frame_personalizado = ttk.LabelFrame(frame, text="Funciones Personalizadas", padding="5")
        self.frame_personalizado.pack(fill=tk.BOTH, expand=True, pady=5)
        self.frame_personalizado.pack_forget()
        
        self._crear_entrada_funciones(self.frame_personalizado)
    
    def _crear_selector_modo(self, parent):
        """Crea selector entre modo estándar y personalizado"""
        modo_frame = ttk.Frame(parent)
        modo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(
            modo_frame,
            text="Modelo Estándar",
            variable=self.modo_personalizado,
            value=False,
            command=self._cambiar_modo
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            modo_frame,
            text="Funciones Personalizadas",
            variable=self.modo_personalizado,
            value=True,
            command=self._cambiar_modo
        ).pack(side=tk.LEFT, padx=5)
    
    def _cambiar_modo(self):
        """Cambia entre modo estándar y personalizado"""
        if self.modo_personalizado.get():
            self.frame_parametros.pack_forget()
            self.frame_personalizado.pack(fill=tk.BOTH, expand=True, pady=5)
        else:
            self.frame_personalizado.pack_forget()
            self.frame_parametros.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def _crear_fila_parametro(self, frame, fila, param, min_val, max_val, desc, valor_defecto):
        """Crea una fila de entrada para un parámetro (KISS + DRY)"""
        label = ttk.Label(frame, text=f"{param} ({desc}):")
        label.grid(row=fila, column=0, sticky=tk.W, pady=5)
        
        var = tk.DoubleVar(value=valor_defecto)
        self.variables[param] = var
        
        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.grid(row=fila, column=1, sticky=tk.W, padx=5, pady=5)
        
        scale = ttk.Scale(frame, from_=min_val, to=max_val, 
                        variable=var, orient=tk.HORIZONTAL)
        scale.grid(row=fila, column=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        frame.columnconfigure(2, weight=1)
    
    def _crear_entrada_funciones(self, parent):
        """Crea entradas para funciones personalizadas"""
        # dx/dt (presa)
        label_presa = ttk.Label(parent, text="dx/dt (Presa):")
        label_presa.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        entry_presa = ttk.Entry(parent, textvariable=self.func_presa, width=40)
        entry_presa.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # dy/dt (depredador)
        label_depredador = ttk.Label(parent, text="dy/dt (Depredador):")
        label_depredador.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        entry_depredador = ttk.Entry(parent, textvariable=self.func_depredador, width=40)
        entry_depredador.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        parent.columnconfigure(1, weight=1)
        
        # Ayuda
        ayuda = ttk.Label(
            parent,
            text="Variables: x (presa), y (depredador) | Funciones: sin(), cos(), exp(), sqrt(), abs()\nEjemplo: x - 0.5*x*y para presas, 0.5*x*y - 0.5*y para depredadores",
            foreground="#666666",
            font=("Arial", 9)
        )
        ayuda.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def obtener_parametros(self):
        """Retorna los parámetros actuales"""
        if self.modo_personalizado.get():
            return {
                'modo': 'personalizado',
                'func_presa': self.func_presa.get(),
                'func_depredador': self.func_depredador.get()
            }
        else:
            return {
                'modo': 'estandar',
                **{param: var.get() for param, var in self.variables.items()}
            }
    
    def establecer_parametros(self, params):
        """Establece los parámetros"""
        if 'modo' in params:
            modo_personalizado = params['modo'] == 'personalizado'
            self.modo_personalizado.set(modo_personalizado)
            self._cambiar_modo()
            
            if modo_personalizado:
                if 'func_presa' in params:
                    self.func_presa.set(params['func_presa'])
                if 'func_depredador' in params:
                    self.func_depredador.set(params['func_depredador'])
        
        for param, valor in params.items():
            if param in self.variables:
                self.variables[param].set(valor)

