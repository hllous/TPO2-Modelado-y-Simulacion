"""
Interfaz gráfica para análisis de sistemas no lineales 1D
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')

from core.sistema_1d import SistemaDinamico1D
from visualization.sistema_1d import VisualizadorSistema1D
from input_module.sistema_1d import (
    obtener_nombres_ejemplos_1d, 
    obtener_ejemplo_1d,
    validar_funcion_entrada
)
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES


class InterfazSistema1D:
    """Interfaz gráfica para análisis de sistemas 1D no lineales"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz
        
        Parámetros:
        - root: ventana raíz o frame principal
        """
        self.root = root
        self.sistema = None
        self.visualizador = None
        
        if isinstance(root, tk.Tk):
            root.title("Sistemas Dinámicos 1D - Análisis No Lineal")
            root.geometry("1400x800")
            root.configure(bg=COLORES['fondo'])
            configurar_estilos_ttk()
        elif isinstance(root, tk.Frame):
            root.configure(bg=COLORES['fondo'])
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea la estructura de widgets"""
        main_frame = ttk.Frame(self.root, padding="10")
        
        if isinstance(self.root, tk.Tk):
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
        else:
            main_frame.pack(fill=tk.BOTH, expand=True)
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        self._crear_panel_control(main_frame)
        self._crear_panel_graficos(main_frame)
    
    def _crear_panel_control(self, parent):
        """Crea panel de controles"""
        control_frame = ttk.LabelFrame(parent, text="Controles", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        control_frame.columnconfigure(0, weight=1)
        
        # Ejemplos
        ttk.Label(control_frame, text="Ejemplos Predefinidos:",
                 font=FUENTES['titulo_seccion']).pack(anchor=tk.W, pady=(0, 5))
        
        self.ejemplo_var = tk.StringVar()
        ejemplo_combo = ttk.Combobox(
            control_frame,
            textvariable=self.ejemplo_var,
            values=obtener_nombres_ejemplos_1d(),
            state='readonly',
            width=30
        )
        ejemplo_combo.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            control_frame,
            text="Cargar Ejemplo",
            command=self._cargar_ejemplo
        ).pack(fill=tk.X, pady=5)
        
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Función personalizada
        ttk.Label(control_frame, text="Función dx/dt:",
                 font=FUENTES['titulo_seccion']).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(control_frame, text="Ingrese la función (ej: -x + x**3):",
                 font=FUENTES['pequena']).pack(anchor=tk.W)
        
        self.funcion_entry = ttk.Entry(control_frame, width=35)
        self.funcion_entry.pack(fill=tk.X, pady=5)
        self.funcion_entry.insert(0, "-x")
        
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Parámetros de visualización
        ttk.Label(control_frame, text="Parámetros de Visualización:",
                 font=FUENTES['titulo_seccion']).pack(anchor=tk.W, pady=(0, 5))
        
        # Rango de x
        ttk.Label(control_frame, text="Rango de x:",
                 font=FUENTES['pequena']).pack(anchor=tk.W)
        x_frame = ttk.Frame(control_frame)
        x_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(x_frame, text="Min:").pack(side=tk.LEFT)
        self.x_min_var = tk.StringVar(value="-5")
        ttk.Entry(x_frame, textvariable=self.x_min_var, width=10).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(x_frame, text="Max:").pack(side=tk.LEFT, padx=(10, 0))
        self.x_max_var = tk.StringVar(value="5")
        ttk.Entry(x_frame, textvariable=self.x_max_var, width=10).pack(side=tk.LEFT, padx=2)
        
        # Condiciones iniciales
        ttk.Label(control_frame, text="Condiciones Iniciales:",
                 font=FUENTES['pequena']).pack(anchor=tk.W, pady=(10, 0))
        
        ttk.Label(control_frame, text="(separadas por comas)",
                 font=FUENTES['pequena'], foreground='gray').pack(anchor=tk.W)
        
        self.x0_entry = ttk.Entry(control_frame, width=35)
        self.x0_entry.pack(fill=tk.X, pady=5)
        self.x0_entry.insert(0, "-2,-1,0,1,2")
        
        # Tiempo
        ttk.Label(control_frame, text="Rango de Tiempo:",
                 font=FUENTES['pequena']).pack(anchor=tk.W)
        t_frame = ttk.Frame(control_frame)
        t_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(t_frame, text="t_final:").pack(side=tk.LEFT)
        self.t_final_var = tk.StringVar(value="10")
        ttk.Entry(t_frame, textvariable=self.t_final_var, width=10).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Botones de análisis
        ttk.Button(
            control_frame,
            text="CAMPO DE FASE",
            command=self._analizar_campo_fase,
            style='Accent.TButton'
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            control_frame,
            text="TRAYECTORIAS",
            command=self._analizar_trayectorias,
            style='Accent.TButton'
        ).pack(fill=tk.X, pady=5)
        
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Información
        ttk.Label(control_frame, text="Información:",
                 font=FUENTES['titulo_seccion']).pack(anchor=tk.W, pady=(0, 5))
        
        self.info_text = scrolledtext.ScrolledText(
            control_frame,
            width=40,
            height=12,
            font=FUENTES['monoespaciada'],
            wrap=tk.WORD
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, pady=5)
        control_frame.rowconfigure(control_frame.winfo_children().__len__() - 1, weight=1)
    
    def _crear_panel_graficos(self, parent):
        """Crea panel de gráficos"""
        plot_frame = ttk.Frame(parent)
        plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        
        # Figura principal
        self.fig_principal = Figure(figsize=(10, 7), dpi=100)
        self.canvas_principal = FigureCanvasTkAgg(
            self.fig_principal,
            master=plot_frame
        )
        self.canvas_principal.get_tk_widget().grid(row=0, column=0,
                                                    sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Toolbar de navegación
        toolbar_frame = ttk.Frame(plot_frame)
        toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.toolbar = NavigationToolbar2Tk(self.canvas_principal, toolbar_frame)
        self.toolbar.update()
    
    def _cargar_ejemplo(self):
        """Carga un ejemplo predefinido"""
        nombre = self.ejemplo_var.get()
        if not nombre:
            messagebox.showwarning("Advertencia", "Seleccione un ejemplo")
            return
        
        ejemplo = obtener_ejemplo_1d(nombre)
        if ejemplo:
            self.funcion_entry.delete(0, tk.END)
            self.funcion_entry.insert(0, ejemplo['funcion'])
            
            self.x_min_var.set(str(ejemplo['xlim'][0]))
            self.x_max_var.set(str(ejemplo['xlim'][1]))
            
            self.t_final_var.set(str(ejemplo['t_span'][1]))
            
            x0_str = ','.join(str(x) for x in ejemplo['x0_iniciales'])
            self.x0_entry.delete(0, tk.END)
            self.x0_entry.insert(0, x0_str)
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"{nombre}\n\n")
            self.info_text.insert(tk.END, f"{ejemplo['descripcion']}\n")
    
    def _validar_entrada(self) -> bool:
        """Valida la entrada del usuario"""
        funcion_str = self.funcion_entry.get().strip()
        
        if not funcion_str:
            messagebox.showerror("Error", "Ingrese una función")
            return False
        
        if not validar_funcion_entrada(funcion_str):
            messagebox.showerror("Error", "Función inválida. Verifique la sintaxis")
            return False
        
        try:
            float(self.x_min_var.get())
            float(self.x_max_var.get())
            float(self.t_final_var.get())
        except ValueError:
            messagebox.showerror("Error", "Parámetros numéricos inválidos")
            return False
        
        return True
    
    def _analizar_campo_fase(self):
        """Analiza el campo de fase"""
        if not self._validar_entrada():
            return
        
        try:
            funcion_str = self.funcion_entry.get()
            xlim = (float(self.x_min_var.get()), float(self.x_max_var.get()))
            
            self.sistema = SistemaDinamico1D(funcion_str)
            self.visualizador = VisualizadorSistema1D(self.sistema)
            
            equilibrios = self.sistema.encontrar_equilibrios(xlim)
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Función: dx/dt = {funcion_str}\n")
            self.info_text.insert(tk.END, "="*45 + "\n\n")
            
            if equilibrios:
                self.info_text.insert(tk.END, "Puntos de Equilibrio:\n")
                for i, x_eq in enumerate(equilibrios, 1):
                    estab = self.sistema.clasificar_estabilidad(x_eq)
                    estado = "ESTABLE" if estab == "estable" else \
                            "INESTABLE" if estab == "inestable" else "NEUTRAL"
                    self.info_text.insert(tk.END, f"  x*_{i} = {x_eq:8.4f}  ({estado})\n")
            else:
                self.info_text.insert(tk.END, "No hay puntos de equilibrio\n")
            
            # Graficar
            self.fig_principal.clear()
            self.visualizador.graficar_campo_fase(xlim, self.fig_principal)
            self.canvas_principal.draw()
            
            self.info_text.insert(tk.END, "\n" + "="*45)
            self.info_text.insert(tk.END, "\nAnálisis completado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis: {e}")
    
    def _analizar_trayectorias(self):
        """Analiza trayectorias temporales"""
        if not self._validar_entrada():
            return
        
        try:
            funcion_str = self.funcion_entry.get()
            xlim = (float(self.x_min_var.get()), float(self.x_max_var.get()))
            t_final = float(self.t_final_var.get())
            
            x0_str = self.x0_entry.get().strip()
            if not x0_str:
                messagebox.showerror("Error", "Ingrese condiciones iniciales")
                return
            
            try:
                x0_values = [float(x.strip()) for x in x0_str.split(',')]
            except ValueError:
                messagebox.showerror("Error", "Condiciones iniciales inválidas")
                return
            
            self.sistema = SistemaDinamico1D(funcion_str)
            self.visualizador = VisualizadorSistema1D(self.sistema)
            
            equilibrios = self.sistema.encontrar_equilibrios(xlim)
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Función: dx/dt = {funcion_str}\n")
            self.info_text.insert(tk.END, f"Condiciones iniciales: {x0_str}\n")
            self.info_text.insert(tk.END, f"Tiempo final: {t_final}\n")
            self.info_text.insert(tk.END, "="*45 + "\n\n")
            
            if equilibrios:
                self.info_text.insert(tk.END, "Equilibrios:\n")
                for i, x_eq in enumerate(equilibrios, 1):
                    estab = self.sistema.clasificar_estabilidad(x_eq)
                    estado = "ESTABLE" if estab == "estable" else "INESTABLE"
                    self.info_text.insert(tk.END, f"  x*_{i} = {x_eq:8.4f}  ({estado})\n")
            
            # Graficar
            self.fig_principal.clear()
            self.visualizador.graficar_espacio_fase_tiempo(
                x0_values,
                (0, t_final),
                self.fig_principal
            )
            self.canvas_principal.draw()
            
            self.info_text.insert(tk.END, "\n" + "="*45)
            self.info_text.insert(tk.END, "\nAnálisis completado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis: {e}")
