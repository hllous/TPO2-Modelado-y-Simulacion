"""
GUI para análisis de bifurcaciones 1D
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

# Agregar el directorio padre al path para importar src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import BifurcationAnalyzer
from src.visualization import BifurcationVisualizer
from src.examples import get_example_names, get_example


class BifurcationGUI:
    """Interfaz gráfica para análisis de bifurcaciones"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Bifurcaciones 1D")
        self.root.geometry("1400x800")
        
        self.analyzer = None
        self.visualizer = None
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crea los widgets de la interfaz"""
        
        # Frame principal dividido en dos: controles (izquierda) y gráficos (derecha)
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # === PANEL IZQUIERDO: Controles ===
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Sección de ejemplos
        ttk.Label(control_frame, text="Ejemplos Predefinidos:", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.example_var = tk.StringVar()
        example_combo = ttk.Combobox(control_frame, textvariable=self.example_var,
                                     values=get_example_names(), state='readonly', width=30)
        example_combo.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        example_combo.bind('<<ComboboxSelected>>', self._on_example_selected)
        
        ttk.Button(control_frame, text="Cargar Ejemplo", 
                  command=self._load_example).grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Separador
        ttk.Separator(control_frame, orient='horizontal').grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Entrada de función personalizada
        ttk.Label(control_frame, text="Función f(x, r):", 
                 font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(control_frame, text="Ingrese la función (ej: r + x**2):", 
                 font=('Arial', 9)).grid(row=5, column=0, sticky=tk.W)
        
        self.function_entry = ttk.Entry(control_frame, width=35)
        self.function_entry.grid(row=6, column=0, pady=5, sticky=(tk.W, tk.E))
        self.function_entry.insert(0, "r + x**2")
        
        # Parámetros
        ttk.Label(control_frame, text="Parámetros:", 
                 font=('Arial', 10, 'bold')).grid(row=7, column=0, sticky=tk.W, pady=(10, 5))
        
        # Rango de r
        r_frame = ttk.Frame(control_frame)
        r_frame.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(r_frame, text="Rango de r:", font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W)
        
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
        ttk.Label(x_frame, text="Rango de x:", font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W)
        
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
                 font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W)
        
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
                  command=self._analyze, style='Accent.TButton').grid(row=11, column=0, 
                                                                       pady=15, sticky=(tk.W, tk.E))
        
        # Separador
        ttk.Separator(control_frame, orient='horizontal').grid(row=12, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Resultados de análisis
        ttk.Label(control_frame, text="Resultados:", 
                 font=('Arial', 10, 'bold')).grid(row=13, column=0, sticky=tk.W, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(control_frame, width=40, height=15, 
                                                      font=('Courier', 9), wrap=tk.WORD)
        self.results_text.grid(row=14, column=0, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        control_frame.rowconfigure(14, weight=1)
        
        # === PANEL DERECHO: Gráficos ===
        plot_frame = ttk.Frame(main_frame)
        plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.rowconfigure(1, weight=1)
        
        # Frame para diagrama de bifurcación
        bifurcation_frame = ttk.LabelFrame(plot_frame, text="Diagrama de Bifurcación", padding="5")
        bifurcation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        bifurcation_frame.columnconfigure(0, weight=1)
        bifurcation_frame.rowconfigure(0, weight=1)
        
        self.bifurcation_fig = Figure(figsize=(8, 4), dpi=100)
        self.bifurcation_canvas = FigureCanvasTkAgg(self.bifurcation_fig, master=bifurcation_frame)
        self.bifurcation_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para diagrama de fase
        phase_frame = ttk.LabelFrame(plot_frame, text="Diagramas de Fase", padding="5")
        phase_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        phase_frame.columnconfigure(0, weight=1)
        phase_frame.rowconfigure(0, weight=1)
        
        self.phase_fig = Figure(figsize=(8, 3), dpi=100)
        self.phase_canvas = FigureCanvasTkAgg(self.phase_fig, master=phase_frame)
        self.phase_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def _on_example_selected(self, event=None):
        """Maneja la selección de un ejemplo"""
        pass
    
    def _load_example(self):
        """Carga un ejemplo predefinido"""
        example_name = self.example_var.get()
        if not example_name:
            messagebox.showwarning("Advertencia", "Por favor seleccione un ejemplo")
            return
        
        example = get_example(example_name)
        if example:
            self.function_entry.delete(0, tk.END)
            self.function_entry.insert(0, example['function'])
            
            self.r_min_entry.delete(0, tk.END)
            self.r_min_entry.insert(0, str(example['r_range'][0]))
            self.r_max_entry.delete(0, tk.END)
            self.r_max_entry.insert(0, str(example['r_range'][1]))
            
            self.x_min_entry.delete(0, tk.END)
            self.x_min_entry.insert(0, str(example['x_range'][0]))
            self.x_max_entry.delete(0, tk.END)
            self.x_max_entry.insert(0, str(example['x_range'][1]))
            
            self.r_neg_entry.delete(0, tk.END)
            self.r_neg_entry.insert(0, str(example['r_values'][0]))
            self.r_zero_entry.delete(0, tk.END)
            self.r_zero_entry.insert(0, str(example['r_values'][1]))
            self.r_pos_entry.delete(0, tk.END)
            self.r_pos_entry.insert(0, str(example['r_values'][2]))
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Ejemplo cargado: {example_name}\n\n")
            self.results_text.insert(tk.END, f"{example['description']}\n\n")
            self.results_text.insert(tk.END, "Presione ANALIZAR para ver los resultados.")
    
    def _analyze(self):
        """Realiza el análisis de bifurcación"""
        try:
            # Obtener parámetros
            function_str = self.function_entry.get()
            r_min = float(self.r_min_entry.get())
            r_max = float(self.r_max_entry.get())
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
            r_neg = float(self.r_neg_entry.get())
            r_zero = float(self.r_zero_entry.get())
            r_pos = float(self.r_pos_entry.get())
            
            # Crear analizador
            self.analyzer = BifurcationAnalyzer(function_str)
            self.visualizer = BifurcationVisualizer(self.analyzer)
            
            # Limpiar resultados previos
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Función: f(x, r) = {function_str}\n")
            self.results_text.insert(tk.END, "="*50 + "\n\n")
            
            # Analizar para los tres valores de r
            for r_val, label in [(r_neg, "r < 0"), (r_zero, "r = 0"), (r_pos, "r > 0")]:
                self.results_text.insert(tk.END, f"{label} (r = {r_val}):\n")
                eq_data = self.analyzer.get_equilibria_with_stability(r_val)
                
                if eq_data:
                    for i, eq in enumerate(eq_data, 1):
                        status = "ESTABLE" if eq['stability'] == 'stable' else "INESTABLE"
                        self.results_text.insert(tk.END, 
                                               f"  x*_{i} = {eq['x']:.4f} ({status})\n")
                else:
                    self.results_text.insert(tk.END, "  No hay puntos de equilibrio reales\n")
                
                self.results_text.insert(tk.END, "\n")
            
            # Generar diagrama de bifurcación
            self.bifurcation_fig.clear()
            self.visualizer.plot_bifurcation_diagram((r_min, r_max), self.bifurcation_fig)
            self.bifurcation_canvas.draw()
            
            # Generar diagramas de fase
            self.phase_fig.clear()
            self.visualizer.plot_phase_diagram([r_neg, r_zero, r_pos], 
                                              (x_min, x_max), self.phase_fig)
            self.phase_canvas.draw()
            
            self.results_text.insert(tk.END, "="*50 + "\n")
            self.results_text.insert(tk.END, "Análisis completado con éxito!\n")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis: {e}")


def main():
    root = tk.Tk()
    app = BifurcationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
