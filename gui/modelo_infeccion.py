"""
Interfaz gráfica para el modelo de infección viral
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')

from core.modelo_infeccion import ModeloVirusInfeccion
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES


class InterfazModeloInfeccion:
    """Interfaz gráfica para modelo de infección viral"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz
        
        Parámetros:
        - root: ventana raíz o frame principal
        """
        self.root = root
        
        # Configurar ventana si es Tk
        if isinstance(root, tk.Tk):
            self.root.title("Modelo de Infección Viral - Simulación Epidemiológica")
            self.root.geometry("1400x800")
            self.root.configure(bg=COLORES['fondo'])
        
        configurar_estilos_ttk()
        
        # Variables de control
        self._inicializar_variables()
        
        # Modelo actual
        self.modelo = None
    
    def _inicializar_variables(self):
        """Inicializa variables de control de la UI"""
        self.K_var = tk.StringVar(value="0.0001")  # Constante de infección
        self.N_var = tk.StringVar(value="10000")   # Población máxima
        self.P0_var = tk.StringVar(value="10")     # Población inicial infectada
        self.t_max_var = tk.StringVar(value="100") # Tiempo máximo de simulación
        self.t_eval_var = tk.StringVar(value="30") # Tiempo para evaluar P(t)
        self.P_eval_resultado = tk.StringVar(value="---")
    
    def crear_widgets(self):
        """Crea la estructura de widgets"""
        if isinstance(self.root, tk.Tk):
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
            main_frame.rowconfigure(0, weight=1)
        else:
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo (controles)
        panel_izq = self._crear_panel_controles(main_frame)
        panel_izq.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Panel derecho (gráfica)
        panel_der = self._crear_panel_grafica(main_frame)
        panel_der.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
    
    def _crear_panel_controles(self, parent):
        """Crea el panel de controles"""
        panel = ttk.Frame(parent, style='Card.TFrame', padding="15")
        
        # Título
        titulo = ttk.Label(panel, text="Parámetros del Modelo", 
                          font=FUENTES['titulo'])
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        row = 1
        
        # Descripción del modelo
        desc_frame = ttk.LabelFrame(panel, text="Modelo: dP/dt = K·P·(N-P)", padding="10")
        desc_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        desc_text = ("Modelo logístico de infección viral\n\n"
                     "P(t) = Población infectada\n"
                     "K = Tasa de infección\n"
                     "N = Población total\n"
                     "P(0) = Infectados iniciales")
        ttk.Label(desc_frame, text=desc_text, font=FUENTES['normal']).pack()
        
        row += 1
        
        # K - Constante de infección
        ttk.Label(panel, text="K (Tasa de infección):", font=FUENTES['normal']).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(panel, textvariable=self.K_var, width=15).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # N - Población máxima
        ttk.Label(panel, text="N (Población total):", font=FUENTES['normal']).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(panel, textvariable=self.N_var, width=15).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # P0 - Población inicial infectada
        ttk.Label(panel, text="P(0) (Infectados iniciales):", font=FUENTES['normal']).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(panel, textvariable=self.P0_var, width=15).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Separador
        ttk.Separator(panel, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Tiempo máximo de simulación
        ttk.Label(panel, text="Tiempo máximo (días):", font=FUENTES['normal']).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(panel, textvariable=self.t_max_var, width=15).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Botón simular
        btn_simular = ttk.Button(panel, text="🦠 Simular Infección", 
                                command=self.simular_modelo, style='Accent.TButton')
        btn_simular.grid(row=row, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))
        row += 1
        
        # Separador
        ttk.Separator(panel, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        row += 1
        
        # Evaluación en tiempo específico
        eval_frame = ttk.LabelFrame(panel, text="Evaluar P(t) en día específico", padding="10")
        eval_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(eval_frame, text="Día (t):", font=FUENTES['normal']).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(eval_frame, textvariable=self.t_eval_var, width=10).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        btn_evaluar = ttk.Button(eval_frame, text="Calcular", command=self.evaluar_en_tiempo)
        btn_evaluar.grid(row=0, column=2, pady=5, padx=5)
        
        ttk.Label(eval_frame, text="Resultado:", font=FUENTES['normal']).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        resultado_label = ttk.Label(eval_frame, textvariable=self.P_eval_resultado, 
                                    font=FUENTES['normal_bold'], foreground=COLORES['primario'])
        resultado_label.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        eval_frame.columnconfigure(1, weight=1)
        
        row += 1
        
        # Panel de estadísticas
        self.stats_frame = ttk.LabelFrame(panel, text="Estadísticas", padding="10")
        self.stats_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.stats_text = tk.Text(self.stats_frame, height=12, width=35, 
                                 font=FUENTES['normal'], wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.stats_text.insert('1.0', 'Simula el modelo para ver estadísticas...')
        self.stats_text.config(state=tk.DISABLED)
        
        panel.columnconfigure(1, weight=1)
        
        return panel
    
    def _crear_panel_grafica(self, parent):
        """Crea el panel de gráfica"""
        panel = ttk.Frame(parent, style='Card.TFrame', padding="15")
        
        # Título
        titulo = ttk.Label(panel, text="Evolución de la Infección", 
                          font=FUENTES['titulo'])
        titulo.pack(pady=(0, 10))
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar de navegación
        toolbar_frame = ttk.Frame(panel)
        toolbar_frame.pack(fill=tk.X, pady=(5, 0))
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Gráfica inicial vacía
        self.ax.text(0.5, 0.5, 'Configura los parámetros y\npresiona "Simular Infección"',
                    ha='center', va='center', fontsize=14, transform=self.ax.transAxes)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        
        return panel
    
    def simular_modelo(self):
        """Simula el modelo y actualiza la gráfica"""
        try:
            # Leer parámetros
            K = float(self.K_var.get())
            N = float(self.N_var.get())
            P0 = float(self.P0_var.get())
            t_max = float(self.t_max_var.get())
            
            # Crear modelo
            self.modelo = ModeloVirusInfeccion(K, N, P0)
            
            # Resolver
            t, P = self.modelo.resolver(t_max=t_max, puntos=1000)
            
            # Actualizar gráfica
            self._actualizar_grafica(t, P)
            
            # Actualizar estadísticas
            self._actualizar_estadisticas()
            
            messagebox.showinfo("Éxito", "Simulación completada exitosamente")
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al simular:\n{str(e)}")
    
    def _actualizar_grafica(self, t, P):
        """Actualiza la gráfica con los resultados"""
        self.ax.clear()
        self.ax.axis('on')
        
        # Gráfica principal
        self.ax.plot(t, P, 'b-', linewidth=2, label='P(t) - Infectados')
        
        # Línea de población máxima
        self.ax.axhline(y=self.modelo.N, color='r', linestyle='--', 
                       linewidth=1.5, label=f'N = {self.modelo.N} (Población total)')
        
        # Punto inicial
        self.ax.plot(0, self.modelo.P0, 'go', markersize=10, 
                    label=f'P(0) = {self.modelo.P0}', zorder=5)
        
        # Punto de inflexión
        t_infl, P_infl = self.modelo.punto_inflexion()
        if t_infl <= t[-1]:
            self.ax.plot(t_infl, P_infl, 'ro', markersize=10, 
                        label=f'Punto inflexión (t={t_infl:.1f})', zorder=5)
            self.ax.axvline(x=t_infl, color='r', linestyle=':', alpha=0.5)
        
        # Configuración
        self.ax.set_xlabel('Tiempo (días)', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Población Infectada', fontsize=12, fontweight='bold')
        self.ax.set_title(f'Modelo de Infección: dP/dt = {self.modelo.K}·P·({self.modelo.N}-P)\n'
                         f'K={self.modelo.K}, N={self.modelo.N}, P(0)={self.modelo.P0}',
                         fontsize=13, fontweight='bold', pad=15)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='best', fontsize=10)
        
        # Ajustar límites
        self.ax.set_xlim(0, t[-1])
        self.ax.set_ylim(0, self.modelo.N * 1.1)
        
        self.canvas.draw()
    
    def _actualizar_estadisticas(self):
        """Actualiza el panel de estadísticas"""
        stats = self.modelo.estadisticas()
        
        texto = f"""Población inicial: {stats['poblacion_inicial']:.0f}
Población máxima: {stats['poblacion_maxima']:.0f}
Tasa de infección (K): {stats['constante_infeccion']:.6f}

PUNTO DE INFLEXIÓN:
  Tiempo: {stats['punto_inflexion_tiempo']:.2f} días
  Población: {stats['punto_inflexion_poblacion']:.0f}
  Tasa máxima: {stats['tasa_maxima_infeccion']:.2f} inf/día

TIEMPOS CRÍTICOS:
  50% infectados: {stats['tiempo_50_porciento']:.2f} días
  90% infectados: {stats['tiempo_90_porciento']:.2f} días
  99% infectados: {stats['tiempo_99_porciento']:.2f} días
"""
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', texto)
        self.stats_text.config(state=tk.DISABLED)
    
    def evaluar_en_tiempo(self):
        """Evalúa P(t) en un tiempo específico"""
        if self.modelo is None:
            messagebox.showwarning("Advertencia", "Primero debes simular el modelo")
            return
        
        try:
            t = float(self.t_eval_var.get())
            P_t = self.modelo.evaluar_en_tiempo(t)
            
            self.P_eval_resultado.set(f"P({t}) = {P_t:.2f} infectados")
            
            # Marcar en la gráfica
            self._marcar_punto_evaluacion(t, P_t)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _marcar_punto_evaluacion(self, t, P):
        """Marca un punto de evaluación en la gráfica"""
        # Remover marcas anteriores de evaluación
        for line in self.ax.lines:
            if line.get_label() == '_evaluacion_temp':
                line.remove()
        
        # Agregar nueva marca
        self.ax.plot(t, P, 'mo', markersize=12, label='_evaluacion_temp', 
                    markeredgecolor='white', markeredgewidth=2, zorder=10)
        
        # Anotación
        self.ax.annotate(f'P({t:.1f}) = {P:.0f}',
                        xy=(t, P), xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='magenta', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', 
                                      color='magenta', lw=2),
                        fontsize=10, fontweight='bold', color='white')
        
        self.canvas.draw()


def main():
    """Función principal para ejecutar como standalone"""
    root = tk.Tk()
    app = InterfazModeloInfeccion(root)
    app.crear_widgets()
    root.mainloop()


if __name__ == "__main__":
    main()
