"""
Módulo de entrada para Lotka-Volterra
Centraliza configuración de parámetros
"""

import tkinter as tk
from tkinter import ttk


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
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea widgets de entrada"""
        frame = ttk.LabelFrame(self.parent, text="Parámetros Lotka-Volterra", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for i, (param, (min_val, max_val, desc)) in enumerate(self.PARAMETROS.items()):
            self._crear_fila_parametro(frame, i, param, min_val, max_val, desc, self.VALORES_DEFECTO[i])
    
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
    
    def obtener_parametros(self):
        """Retorna los parámetros actuales"""
        return {param: var.get() for param, var in self.variables.items()}
    
    def establecer_parametros(self, params):
        """Establece los parámetros"""
        for param, valor in params.items():
            if param in self.variables:
                self.variables[param].set(valor)
