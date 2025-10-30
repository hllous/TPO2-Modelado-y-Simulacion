"""
Interfaz gráfica para análisis de bifurcaciones 1D
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')

from core.bifurcacion import AnalizadorBifurcacion
from visualization.bifurcacion import VisualizadorBifurcacion
from input_module.bifurcacion import obtener_nombres_ejemplos_bifurcacion, obtener_ejemplo_bifurcacion
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES


class InterfazBifurcacion:
    """Interfaz gráfica para análisis de bifurcaciones"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz de bifurcaciones
        
        Parámetros:
        - root: ventana raíz o frame principal de tkinter
        """
        self.root = root
        self.analizador = None
        self.visualizador = None
        
        if isinstance(root, tk.Tk):
            root.title("Análisis de Bifurcaciones 1D")
            root.geometry("1400x800")
            root.configure(bg=COLORES['fondo'])
            configurar_estilos_ttk()
        elif isinstance(root, tk.Frame):
            root.configure(bg=COLORES['fondo'])
        
        self._crear_widgets()
        
    def _crear_widgets(self):
        """Crea los widgets de la interfaz"""
        
        main_frame = ttk.Frame(self.root, padding="10")
        if isinstance(self.root, tk.Tk):
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
        else:
            main_frame.pack(fill=tk.BOTH, expand=True)
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo: Controles
        self._crear_panel_controles(main_frame)
        
        # Panel derecho: Gráficos
        self._crear_panel_graficos(main_frame)
        
    def _crear_panel_controles(self, parent):
        """Crea panel de controles"""
        control_frame = ttk.LabelFrame(parent, text="Controles", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Ejemplos
        ttk.Label(control_frame, text="Ejemplos Predefinidos:", 
                 font=FUENTES['titulo_seccion']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.ejemplo_var = tk.StringVar()
        ejemplo_combo = ttk.Combobox(control_frame, textvariable=self.ejemplo_var,
                                     values=obtener_nombres_ejemplos_bifurcacion(), 
                                     state='readonly', width=30)
        ejemplo_combo.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="Cargar Ejemplo", 
                  command=self._cargar_ejemplo).grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Separator(control_frame, orient='horizontal').grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Función personalizada
        ttk.Label(control_frame, text="Función f(x, r):", 
                 font=FUENTES['titulo_seccion']).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(control_frame, text="Ingrese la función (ej: r + x**2):", 
                 font=FUENTES['pequena']).grid(row=5, column=0, sticky=tk.W)
        
        self.funcion_entry = ttk.Entry(control_frame, width=35)
        self.funcion_entry.grid(row=6, column=0, pady=5, sticky=(tk.W, tk.E))
        self.funcion_entry.insert(0, "r + x**2")
        
        # Parámetros
        ttk.Label(control_frame, text="Parámetros:", 
                 font=FUENTES['titulo_seccion']).grid(row=7, column=0, sticky=tk.W, pady=(10, 5))
        
        # Rango de r
        r_frame = ttk.Frame(control_frame)
        r_frame.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(r_frame, text="Rango de r:", font=FUENTES['pequena']).grid(row=0, column=0, sticky=tk.W)
        
        r_entry_frame = ttk.Frame(r_frame)
        r_entry_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        ttk.Label(r_entry_frame, text="Min:").grid(row=0, column=0)
        self.r_min_entry = ttk.Entry(r_entry_frame, width=10)
        self.r_min_entry.grid(row=0, column=1, padx=2)
        self.r_min_entry.insert(0, "-2")
        ttk.Label(r_entry_frame, text="Max:").grid(row=0, column=2, padx=(5, 0))
        self.r_max_entry = ttk.Entry(r_entry_frame, width=10)
        self.r_max_entry.grid(row=0, column=3, padx=2)
        self.r_max_entry.insert(0, "2")
        
        # Rango de x
        x_frame = ttk.Frame(control_frame)
        x_frame.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(x_frame, text="Rango de x:", font=FUENTES['pequena']).grid(row=0, column=0, sticky=tk.W)
        
        x_entry_frame = ttk.Frame(x_frame)
        x_entry_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        ttk.Label(x_entry_frame, text="Min:").grid(row=0, column=0)
        self.x_min_entry = ttk.Entry(x_entry_frame, width=10)
        self.x_min_entry.grid(row=0, column=1, padx=2)
        self.x_min_entry.insert(0, "-3")
        ttk.Label(x_entry_frame, text="Max:").grid(row=0, column=2, padx=(5, 0))
        self.x_max_entry = ttk.Entry(x_entry_frame, width=10)
        self.x_max_entry.grid(row=0, column=3, padx=2)
        self.x_max_entry.insert(0, "3")
        
        # Valores de r para diagramas de fase
        r_vals_frame = ttk.Frame(control_frame)
        r_vals_frame.grid(row=10, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(r_vals_frame, text="Valores de r para fase:", 
                 font=FUENTES['pequena']).grid(row=0, column=0, sticky=tk.W)
        
        r_vals_entry_frame = ttk.Frame(r_vals_frame)
        r_vals_entry_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        ttk.Label(r_vals_entry_frame, text="r<0:").grid(row=0, column=0)
        self.r_neg_entry = ttk.Entry(r_vals_entry_frame, width=7)
        self.r_neg_entry.grid(row=0, column=1, padx=2)
        self.r_neg_entry.insert(0, "-1")
        ttk.Label(r_vals_entry_frame, text="r=0:").grid(row=0, column=2)
        self.r_zero_entry = ttk.Entry(r_vals_entry_frame, width=7)
        self.r_zero_entry.grid(row=0, column=3, padx=2)
        self.r_zero_entry.insert(0, "0")
        ttk.Label(r_vals_entry_frame, text="r>0:").grid(row=0, column=4)
        self.r_pos_entry = ttk.Entry(r_vals_entry_frame, width=7)
        self.r_pos_entry.grid(row=0, column=5, padx=2)
        self.r_pos_entry.insert(0, "1")
        
        # Botón de análisis
        ttk.Button(control_frame, text="ANALIZAR", 
                  command=self._analizar, style='Accent.TButton').grid(row=11, column=0, 
                                                                       pady=15, sticky=(tk.W, tk.E))
        
        ttk.Separator(control_frame, orient='horizontal').grid(row=12, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Resultados
        ttk.Label(control_frame, text="Resultados:", 
                 font=FUENTES['titulo_seccion']).grid(row=13, column=0, sticky=tk.W, pady=5)
        
        self.resultados_text = scrolledtext.ScrolledText(control_frame, width=40, height=15, 
                                                         font=FUENTES['monoespaciada'], wrap=tk.WORD)
        self.resultados_text.grid(row=14, column=0, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        control_frame.rowconfigure(14, weight=1)
        
    def _crear_panel_graficos(self, parent):
        """Crea panel de gráficos"""
        plot_frame = ttk.Frame(parent)
        plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=1)
        
        # Diagrama de bifurcación
        bifurcacion_frame = ttk.LabelFrame(plot_frame, text="Diagrama de Bifurcación", padding="5")
        bifurcacion_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        bifurcacion_frame.columnconfigure(0, weight=1)
        bifurcacion_frame.rowconfigure(0, weight=1)
        
        self.bifurcacion_fig = Figure(figsize=(8, 4), dpi=100)
        self.bifurcacion_canvas = FigureCanvasTkAgg(self.bifurcacion_fig, master=bifurcacion_frame)
        self.bifurcacion_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Diagramas de fase
        phase_frame = ttk.LabelFrame(plot_frame, text="Diagramas de Fase", padding="5")
        phase_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        phase_frame.columnconfigure(0, weight=1)
        phase_frame.rowconfigure(0, weight=1)
        
        self.phase_fig = Figure(figsize=(8, 3), dpi=100)
        self.phase_canvas = FigureCanvasTkAgg(self.phase_fig, master=phase_frame)
        self.phase_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _cargar_ejemplo(self):
        """Carga un ejemplo predefinido"""
        nombre_ejemplo = self.ejemplo_var.get()
        if not nombre_ejemplo:
            messagebox.showwarning("Advertencia", "Por favor seleccione un ejemplo")
            return
        
        ejemplo = obtener_ejemplo_bifurcacion(nombre_ejemplo)
        if ejemplo:
            self.funcion_entry.delete(0, tk.END)
            self.funcion_entry.insert(0, ejemplo['funcion'])
            
            self.r_min_entry.delete(0, tk.END)
            self.r_min_entry.insert(0, str(ejemplo['r_range'][0]))
            self.r_max_entry.delete(0, tk.END)
            self.r_max_entry.insert(0, str(ejemplo['r_range'][1]))
            
            self.x_min_entry.delete(0, tk.END)
            self.x_min_entry.insert(0, str(ejemplo['x_range'][0]))
            self.x_max_entry.delete(0, tk.END)
            self.x_max_entry.insert(0, str(ejemplo['x_range'][1]))
            
            self.r_neg_entry.delete(0, tk.END)
            self.r_neg_entry.insert(0, str(ejemplo['r_valores'][0]))
            self.r_zero_entry.delete(0, tk.END)
            self.r_zero_entry.insert(0, str(ejemplo['r_valores'][1]))
            self.r_pos_entry.delete(0, tk.END)
            self.r_pos_entry.insert(0, str(ejemplo['r_valores'][2]))
            
            self.resultados_text.delete(1.0, tk.END)
            self.resultados_text.insert(tk.END, f"Ejemplo cargado: {nombre_ejemplo}\n\n")
            self.resultados_text.insert(tk.END, f"{ejemplo['descripcion']}\n\n")
            self.resultados_text.insert(tk.END, "Presione ANALIZAR para ver los resultados.")
    
    def _analizar(self):
        """Realiza el análisis de bifurcación"""
        try:
            funcion_str = self.funcion_entry.get()
            r_min = float(self.r_min_entry.get())
            r_max = float(self.r_max_entry.get())
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
            r_neg = float(self.r_neg_entry.get())
            r_zero = float(self.r_zero_entry.get())
            r_pos = float(self.r_pos_entry.get())
            
            self.analizador = AnalizadorBifurcacion(funcion_str)
            self.visualizador = VisualizadorBifurcacion(self.analizador)
            
            self.resultados_text.delete(1.0, tk.END)
            self.resultados_text.insert(tk.END, f"Función: f(x, r) = {funcion_str}\n")
            self.resultados_text.insert(tk.END, "="*50 + "\n\n")
            
            for r_val, label in [(r_neg, "r < 0"), (r_zero, "r = 0"), (r_pos, "r > 0")]:
                self.resultados_text.insert(tk.END, f"{label} (r = {r_val}):\n")
                eq_data = self.analizador.obtener_equilibrios_con_estabilidad(r_val)
                
                if eq_data:
                    for i, eq in enumerate(eq_data, 1):
                        status = "ESTABLE" if eq['estabilidad'] == 'estable' else "INESTABLE"
                        self.resultados_text.insert(tk.END, 
                                                   f"  x*_{i} = {eq['x']:.4f} ({status})\n")
                else:
                    self.resultados_text.insert(tk.END, "  No hay puntos de equilibrio reales\n")
                
                self.resultados_text.insert(tk.END, "\n")
            
            self.bifurcacion_fig.clear()
            self.visualizador.graficar_diagrama_bifurcacion((r_min, r_max), self.bifurcacion_fig)
            self.bifurcacion_canvas.draw()
            
            self.phase_fig.clear()
            self.visualizador.graficar_diagrama_fase([r_neg, r_zero, r_pos], 
                                                     (x_min, x_max), self.phase_fig)
            self.phase_canvas.draw()
            
            self.resultados_text.insert(tk.END, "="*50 + "\n")
            self.resultados_text.insert(tk.END, "Análisis completado con éxito!\n")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis: {e}")
