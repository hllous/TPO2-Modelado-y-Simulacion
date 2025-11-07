"""
Interfaz gráfica para análisis de sistemas Hamiltonianos
"""

import tkinter as tk
from tkinter import ttk, messagebox
import traceback
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')

from core.hamilton import AnalizadorHamilton
from ui.estilos import COLORES, FUENTES
from ui.gui_utils import crear_entrada_ecuacion, mostrar_paso_analisis


class InterfazHamilton:
    """Interfaz para análisis de sistemas Hamiltonianos"""
    
    def __init__(self, parent):
        """Inicializa la interfaz Hamilton"""
        self.parent = parent
        self._crear_layout()
    
    def _crear_layout(self):
        """Crea la estructura de la interfaz"""
        main_frame = ttk.Frame(self.parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="Análisis de Sistemas Hamiltonianos",
            font=FUENTES['titulo'],
            fg=COLORES['primario']
        )
        titulo.pack(pady=10)
        
        # Frame para entrada
        entrada_frame = ttk.LabelFrame(main_frame, text="Ingrese el Sistema", padding="15")
        entrada_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # U(x,y) = dx/dt
        self.u_frame, self.u_entry = crear_entrada_ecuacion(
            entrada_frame, "U(x,y) = dx/dt:", 
            tk.StringVar(value="-x"),
            "Ej: -x, -x + y, x*y, sin(x)"
        )
        self.u_frame.pack(fill=tk.X, pady=5)
        
        # V(x,y) = dy/dt
        self.v_frame, self.v_entry = crear_entrada_ecuacion(
            entrada_frame, "V(x,y) = dy/dt:", 
            tk.StringVar(value="-y"),
            "Ej: -y, x - y, x**2, cos(y)"
        )
        self.v_frame.pack(fill=tk.X, pady=5)
        
        # Frame de botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_analizar = ttk.Button(btn_frame, text="Analizar", command=self._analizar)
        btn_analizar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = ttk.Button(btn_frame, text="Limpiar", command=self._limpiar)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Frame principal con scroll
        self.contenido_frame = ttk.Frame(main_frame)
        self.contenido_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas con scrollbar
        self.canvas = tk.Canvas(self.contenido_frame, bg=COLORES['fondo'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.contenido_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)
        
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind scroll
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))
    
    def _analizar(self):
        """Ejecuta el análisis"""
        try:
            u_str = self.u_entry.get().strip()
            v_str = self.v_entry.get().strip()
            
            if not u_str or not v_str:
                messagebox.showwarning("Entrada Vacía", "Ingrese ambas funciones")
                return
            
            analizador = AnalizadorHamilton(u_str, v_str)
            resultado = analizador.analizar()
            
            self._mostrar_resultado(resultado)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis:\n{str(e)}\n\n{traceback.format_exc()}")
    
    def _mostrar_resultado(self, resultado):
        """Muestra el resultado del análisis paso a paso"""
        # Limpiar frame anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Título resultado
        es_conservativo = resultado['es_conservativo']
        color_resultado = 'green' if es_conservativo else 'red'
        
        titulo_resultado = tk.Label(
            self.scroll_frame,
            text="Resultado del Análisis",
            font=FUENTES['titulo'],
            fg=color_resultado,
            bg=COLORES['fondo']
        )
        titulo_resultado.pack(fill=tk.X, pady=(0, 10))
        
        # Mostrar pasos usando utilidad DRY
        for i, paso in enumerate(resultado['pasos'], 1):
            mostrar_paso_analisis(
                self.scroll_frame, i, paso['titulo'], *paso['contenido']
            )
    
    def _limpiar(self):
        """Limpia los campos"""
        self.u_entry.delete(0, tk.END)
        self.v_entry.delete(0, tk.END)
        self.u_entry.insert(0, "-x")
        self.v_entry.insert(0, "-y")
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
