"""
Interfaz gráfica principal del sistema dinámico
Orquesta todos los módulos para crear la aplicación
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')

from core.sistema import SistemaDinamico2D
from core.utils import normalizar_funciones
from visualization.grapher import Grapher
from visualization.plotter import integrate_trajectory_limited
from ui.widgets import ToolTip
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES
from input_module.ejemplos import EJEMPLOS_LINEALES
from gui.popup_analisis import VentanaAnalisisPopup


class InterfazGrafica:
    """Interfaz gráfica del módulo sistemas 2D"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica
        
        Parámetros:
        - root: ventana raíz o frame principal de tkinter
        """
        self.root = root
        
        # Configurar solo si es ventana principal
        if isinstance(root, tk.Tk):
            self.root.title("Sistemas Dinámicos 2D - Análisis Completo")
            self.root.geometry("1400x800")
            self.root.configure(bg=COLORES['fondo'])
        else:
            # Si es un frame de tk, configurar con bg
            if isinstance(root, tk.Frame):
                root.configure(bg=COLORES['fondo'])
            # Si es ttk.Frame, no configurar bg (usa estilos)
        
        # Configurar estilos
        configurar_estilos_ttk()
        
        # Variables de control
        self._inicializar_variables()
        
        # No crear widgets aquí si se usa como módulo
        # Se crearán cuando se llame a crear_widgets()
    
    def _obtener_ventana_root(self):
        """Obtiene la ventana root del widget actual"""
        widget = self.root
        while not isinstance(widget, tk.Tk):
            widget = widget.master
        return widget
    
    def _inicializar_variables(self):
        """Inicializa todas las variables de control de la UI"""
        # Variables de matriz
        self.a11_var = tk.StringVar(value="-1")
        self.a12_var = tk.StringVar(value="0")
        self.a21_var = tk.StringVar(value="0")
        self.a22_var = tk.StringVar(value="-2")
        
        # Variables de término forzado
        self.usar_forzado = tk.BooleanVar(value=False)
        self.tipo_forzado = tk.StringVar(value="constante")
        self.coef1_var = tk.StringVar(value="0")
        self.coef2_var = tk.StringVar(value="0")
        self.param_var = tk.StringVar(value="1")
        
        # Variables de funciones personalizadas
        self.modo_funcion = tk.BooleanVar(value=False)
        self.f1_expr = tk.StringVar(value="-x")
        self.f2_expr = tk.StringVar(value="-y")
        
        # Variables de parámetros personalizados
        self.parametros_expr = tk.StringVar(value="")  # Solo el valor de 'u'
        
        # Sistema actual
        self.sistema_actual = None
    
    def crear_widgets(self):
        """Crea la estructura principal de widgets"""
        # Usar grid si es ventana Tk, pack si es frame
        if isinstance(self.root, tk.Tk):
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
            main_frame.rowconfigure(0, weight=1)
            
            # Panel izquierdo (controles)
            self._crear_panel_izquierdo(main_frame)
            
            # Panel derecho (gráfica)
            self._crear_panel_derecho(main_frame)
        else:
            # Modo frame: usar pack en todo
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Panel izquierdo y derecho lado a lado con pack
            left_container = ttk.Frame(main_frame)
            left_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
            
            right_container = ttk.Frame(main_frame)
            right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            self._crear_panel_izquierdo(left_container)
            self._crear_panel_derecho(right_container)
        
        # Analizar sistema inicial
        self.analizar_sistema()
    
    def _crear_panel_izquierdo(self, parent):
        """Crea panel de controles izquierdo"""
        left_frame = ttk.Frame(parent, padding="5")
        
        if isinstance(self.root, tk.Tk):
            left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        else:
            left_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Título
        self._crear_seccion_titulo(left_frame)
        
        # Selector de modo
        self._crear_selector_modo(left_frame)
        
        # Entrada de matriz
        self._crear_entrada_matriz(left_frame)
        
        # Entrada de funciones
        self._crear_entrada_funciones(left_frame)
        
        # Término forzado (solo en modo matriz)
        self._crear_termino_forzado(left_frame)
        
        # Ejemplos (solo en modo matriz)
        self._crear_ejemplos(left_frame)
        
        # Resultados
        self._crear_resultados(left_frame)
    
    def _crear_seccion_titulo(self, parent):
        """Crea sección de título"""
        titulo_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        titulo_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(titulo_frame, text="Sistemas Dinámicos 2D",
                 style='Title.TLabel', font=FUENTES['titulo']).grid(row=0, column=0)
        ttk.Label(titulo_frame, text="Lineales, no lineales, homogéneos y no homogéneos",
                 style='Subtitle.TLabel').grid(row=1, column=0, pady=(5, 0))
    
    def _crear_selector_modo(self, parent):
        """Crea selector entre modo matriz y modo función"""
        modo_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        modo_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(modo_frame, text="Modo de Entrada:", style='Title.TLabel').grid(
            row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Radiobutton(modo_frame, text="Matriz (Sistema Lineal)", 
                       variable=self.modo_funcion, value=False,
                       command=self.cambiar_modo).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(modo_frame, text="Funciones (Lineal/No Lineal)", 
                       variable=self.modo_funcion, value=True,
                       command=self.cambiar_modo).grid(row=1, column=1, sticky=tk.W, pady=2)
    
    def _crear_entrada_matriz(self, parent):
        """Crea frame para entrada de matriz"""
        self.matriz_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        self.matriz_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.matriz_frame, text="Matriz del Sistema A (2×2)",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Símbolos de matriz
        ttk.Label(self.matriz_frame, text="⎡", font=('Arial', 40), 
                 background='white').grid(row=1, column=0, rowspan=2)
        ttk.Label(self.matriz_frame, text="⎤", font=('Arial', 40), 
                 background='white').grid(row=1, column=3, rowspan=2)
        
        # Entradas
        ventana_root = self._obtener_ventana_root()
        vcmd = (ventana_root.register(self.validar_numero), '%P')
        
        entries = [
            (self.a11_var, 1, 1, "a₁₁"),
            (self.a12_var, 1, 2, "a₁₂"),
            (self.a21_var, 2, 1, "a₂₁"),
            (self.a22_var, 2, 2, "a₂₂"),
        ]
        
        for var, row, col, tooltip_text in entries:
            entry = ttk.Entry(self.matriz_frame, textvariable=var,
                            width=12, justify='center',
                            validate='key', validatecommand=vcmd,
                            font=FUENTES['normal'])
            entry.grid(row=row, column=col, padx=5, pady=5)
            ToolTip(entry, f"Elemento {tooltip_text} de la matriz")
        
        # Botón analizar
        btn_analizar = ttk.Button(self.matriz_frame, text="Analizar Sistema",
                                 style='Accent.TButton',
                                 command=self.analizar_sistema)
        btn_analizar.grid(row=3, column=0, columnspan=4, pady=(15, 0), sticky=(tk.W, tk.E))
    
    def _crear_entrada_funciones(self, parent):
        """Crea frame para entrada de funciones personalizadas"""
        self.funciones_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        self.funciones_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.funciones_frame, text="Funciones del Sistema",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Entrada dx/dt
        ttk.Label(self.funciones_frame, text="dx₁/dt =", 
                 background='white', font=FUENTES['normal']).grid(
            row=1, column=0, sticky=tk.E, padx=(0, 5), pady=5)
        
        self.entry_f1 = ttk.Entry(self.funciones_frame, textvariable=self.f1_expr,
                                  width=30, font=FUENTES['monoespaciada'])
        self.entry_f1.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Entrada dy/dt
        ttk.Label(self.funciones_frame, text="dx₂/dt =", 
                 background='white', font=FUENTES['normal']).grid(
            row=2, column=0, sticky=tk.E, padx=(0, 5), pady=5)
        
        self.entry_f2 = ttk.Entry(self.funciones_frame, textvariable=self.f2_expr,
                                  width=30, font=FUENTES['monoespaciada'])
        self.entry_f2.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Entrada de parámetro u
        ttk.Label(self.funciones_frame, text="u (opcional):", 
                 background='white', font=FUENTES['normal']).grid(
            row=3, column=0, sticky=tk.E, padx=(0, 5), pady=5)
        
        self.entry_params = ttk.Entry(self.funciones_frame, textvariable=self.parametros_expr,
                                      width=30, font=FUENTES['monoespaciada'])
        self.entry_params.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.funciones_frame.columnconfigure(1, weight=1)
        
        # Ayuda
        ayuda_text = "Variables: x, y, t | Funciones: sin(), cos(), exp(), sqrt(), abs()\n"
        ayuda_text += "Puede usar 'u' como parámetro. Ej: u*x-y con u=0.5\n"
        ayuda_text += "Use 'sen' o 'sin' para seno, ambos son válidos"
        ttk.Label(self.funciones_frame, text=ayuda_text,
                 background='white', foreground=COLORES['texto_secundario'],
                 font=FUENTES['pequena'], wraplength=350).grid(
            row=4, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # Botón analizar
        btn_analizar = ttk.Button(self.funciones_frame, text="Analizar Función",
                                 style='Accent.TButton',
                                 command=self.analizar_sistema)
        btn_analizar.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky=(tk.W, tk.E))
        
        # Ejemplos rápidos
        ttk.Label(self.funciones_frame, text="Ejemplos Rápidos:",
                 style='Title.TLabel').grid(row=6, column=0, columnspan=2, pady=(15, 5))
        
        ejemplos = [
            ("Lineal simple", "-x", "-2*y", ""),
            ("Hopf (u=0.5)", "u*x - y - x*(x**2 + y**2)", "x + u*y - y*(x**2 + y**2)", "0.5"),
            ("No lineal", "-x + y**2", "-y + x*y", ""),
            ("Van der Pol", "y", "(1-x**2)*y - x", ""),
            ("Lotka-Volterra", "x - 0.5*x*y", "0.5*x*y - 0.5*y", ""),
            ("Hopf (u=-0.5)", "u*x - y - x*(x**2 + y**2)", "x + u*y - y*(x**2 + y**2)", "-0.5"),
        ]
        
        for i, ejemplo in enumerate(ejemplos):
            row = 6 + i // 2
            col = i % 2
            if len(ejemplo) == 4:
                nombre, f1, f2, params = ejemplo
                btn = ttk.Button(self.funciones_frame, text=nombre,
                               command=lambda f1=f1, f2=f2, p=params: self._cargar_ejemplo_funcion(f1, f2, p))
            else:
                nombre, f1, f2 = ejemplo
                btn = ttk.Button(self.funciones_frame, text=nombre,
                               command=lambda f1=f1, f2=f2: self._cargar_ejemplo_funcion(f1, f2, ""))
            btn.grid(row=row, column=col, pady=2, padx=2, sticky=(tk.W, tk.E))
        
        self.funciones_frame.columnconfigure(0, weight=1)
        self.funciones_frame.columnconfigure(1, weight=1)
        
        # Ocultar inicialmente
        self.funciones_frame.grid_remove()
    
    def _crear_termino_forzado(self, parent):
        """Crea frame para término forzado (solo en modo matriz)"""
        self.forzado_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        self.forzado_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        check = ttk.Checkbutton(self.forzado_frame, 
                               text="Agregar Término Forzado f(t)",
                               variable=self.usar_forzado,
                               command=self.toggle_forzado,
                               style='Title.TLabel')
        check.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        
        # Frame de controles (oculto inicialmente)
        self.forzado_controls = ttk.Frame(self.forzado_frame)
        self.forzado_controls.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Tipo
        ttk.Label(self.forzado_controls, text="Tipo:", background='white').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        tipo_combo = ttk.Combobox(self.forzado_controls, 
                                 textvariable=self.tipo_forzado,
                                 values=['constante', 'exponencial', 'seno', 'coseno'],
                                 state='readonly', width=12)
        tipo_combo.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E), 
                       pady=5, padx=(5, 0))
        tipo_combo.bind('<<ComboboxSelected>>', lambda e: self._actualizar_forzado())
        
        # Coeficientes
        ttk.Label(self.forzado_controls, text="f₁:", background='white').grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.entry_coef1 = ttk.Entry(self.forzado_controls, 
                                     textvariable=self.coef1_var,
                                     width=8, justify='center')
        self.entry_coef1.grid(row=1, column=1, pady=5, padx=(5, 0))
        
        ttk.Label(self.forzado_controls, text="f₂:", background='white').grid(
            row=1, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        self.entry_coef2 = ttk.Entry(self.forzado_controls, 
                                     textvariable=self.coef2_var,
                                     width=8, justify='center')
        self.entry_coef2.grid(row=1, column=3, pady=5, padx=(5, 0))
        
        # Parámetro
        self.label_param = tk.Label(self.forzado_controls, text="(no aplica)", 
                                    background='white')
        self.label_param.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_param = ttk.Entry(self.forzado_controls, 
                                     textvariable=self.param_var,
                                     width=8, justify='center',
                                     state='disabled')
        self.entry_param.grid(row=2, column=1, pady=5, padx=(5, 0))
        
        # Fórmula
        self.label_formula = tk.Label(self.forzado_controls, 
                                      text="f(t) = [0, 0]ᵀ",
                                      background='white',
                                      font=FUENTES['monoespaciada'],
                                      foreground='#0066cc')
        self.label_formula.grid(row=3, column=0, columnspan=4, pady=(10, 0))
        
        # Botón Aplicar
        btn_aplicar = ttk.Button(self.forzado_controls, text="Aplicar Término Forzado",
                                style='Accent.TButton',
                                command=self.aplicar_termino_forzado)
        btn_aplicar.grid(row=4, column=0, columnspan=4, pady=(15, 0), sticky=(tk.W, tk.E))
        
        self.forzado_controls.grid_remove()
        self.forzado_frame.grid_remove()
    
    def _crear_ejemplos(self, parent):
        """Crea frame de ejemplos predefinidos en dos columnas (solo modo matriz)"""
        self.ejemplos_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        self.ejemplos_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.ejemplos_frame, text="Ejemplos Predefinidos",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Agrupar ejemplos por columna
        ejemplos_col0 = [
            (k, v) for k, v in EJEMPLOS_LINEALES.items() 
            if v.get('columna', 0) == 0
        ]
        ejemplos_col1 = [
            (k, v) for k, v in EJEMPLOS_LINEALES.items() 
            if v.get('columna', 1) == 1
        ]
        
        for i, (clave, datos) in enumerate(ejemplos_col0):
            btn = ttk.Button(self.ejemplos_frame, text=datos['nombre'],
                           command=lambda m=datos['matriz']: self.cargar_ejemplo(m))
            btn.grid(row=i+1, column=0, pady=2, padx=(0, 2), sticky=(tk.W, tk.E))
        
        for i, (clave, datos) in enumerate(ejemplos_col1):
            btn = ttk.Button(self.ejemplos_frame, text=datos['nombre'],
                           command=lambda m=datos['matriz']: self.cargar_ejemplo(m))
            btn.grid(row=i+1, column=1, pady=2, padx=(2, 0), sticky=(tk.W, tk.E))
        
        self.ejemplos_frame.columnconfigure(0, weight=1)
        self.ejemplos_frame.columnconfigure(1, weight=1)
    
    def _crear_resultados(self, parent):
        """Crea frame de resultados (solo botón, análisis en popup)"""
        resultados_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        resultados_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        parent.rowconfigure(5, weight=1)
        
        self.btn_analisis_detallado = ttk.Button(
            resultados_frame, text="📊 Ver Análisis Detallado",
            command=self.mostrar_analisis_popup,
            style='Accent.TButton')
        self.btn_analisis_detallado.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _crear_panel_derecho(self, parent):
        """Crea panel derecho con gráfica"""
        right_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        
        if isinstance(self.root, tk.Tk):
            right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        else:
            right_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        ttk.Label(right_frame, text="Visualización del Sistema",
                 style='Title.TLabel').grid(row=0, column=0, pady=(0, 10))
        
        # Controles
        controles_frame = ttk.Frame(right_frame)
        controles_frame.grid(row=0, column=0, pady=(0, 10), sticky=tk.E, padx=10)
        
        btn_limpiar = ttk.Button(controles_frame, text="Limpiar Trayectorias",
                                command=self.limpiar_trayectorias)
        btn_limpiar.pack(side=tk.RIGHT, padx=5)
        
        info = ttk.Label(controles_frame, 
                        text="Clic en la gráfica para generar trayectorias",
                        background='white', font=FUENTES['pequena'],
                        foreground=COLORES['texto_secundario'])
        info.pack(side=tk.RIGHT, padx=10)
        
        # Gráfica de matplotlib
        self.fig = Figure(figsize=(8, 7), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Conectar clic
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
    
    def cambiar_modo(self):
        """Cambia entre modo matriz y modo función"""
        if self.modo_funcion.get():
            # Modo funciones: ocultar matriz, ejemplos y término forzado
            self.matriz_frame.grid_remove()
            self.ejemplos_frame.grid_remove()
            self.forzado_frame.grid_remove()
            self.funciones_frame.grid()
            self.usar_forzado.set(False)
        else:
            # Modo matriz: mostrar matriz, ejemplos y término forzado
            self.funciones_frame.grid_remove()
            self.matriz_frame.grid()
            self.ejemplos_frame.grid()
            self.forzado_frame.grid()
        self.analizar_sistema()
    
    def toggle_forzado(self):
        """Muestra/oculta controles del término forzado y analiza"""
        if self.usar_forzado.get():
            self.forzado_controls.grid()
            self._actualizar_forzado()
        else:
            self.forzado_controls.grid_remove()
            self.analizar_sistema()
    
    def _actualizar_forzado(self):
        """Actualiza parámetro y fórmula sin analizar"""
        tipo = self.tipo_forzado.get()
        
        # Actualizar estado del parámetro
        if tipo == 'constante':
            self.label_param.config(text="(no aplica)")
            self.entry_param.config(state='disabled')
        elif tipo == 'exponencial':
            self.label_param.config(text="k:")
            self.entry_param.config(state='normal')
        elif tipo in ['seno', 'coseno']:
            self.label_param.config(text="ω:")
            self.entry_param.config(state='normal')
        
        # Actualizar fórmula
        try:
            c1 = float(self.coef1_var.get() or 0)
            c2 = float(self.coef2_var.get() or 0)
            param = float(self.param_var.get() or 1)
            
            if tipo == 'constante':
                formula = f"f(t) = [{c1}, {c2}]ᵀ"
            elif tipo == 'exponencial':
                formula = f"f(t) = [{c1}e^({param}t), {c2}e^({param}t)]ᵀ"
            elif tipo == 'seno':
                formula = f"f(t) = [{c1}sin({param}t), {c2}sin({param}t)]ᵀ"
            elif tipo == 'coseno':
                formula = f"f(t) = [{c1}cos({param}t), {c2}cos({param}t)]ᵀ"
            
            self.label_formula.config(text=formula)
        except:
            pass  # Si hay error en conversión, no actualizar fórmula
    
    def aplicar_termino_forzado(self):
        """Aplica el término forzado y actualiza la gráfica"""
        self._actualizar_forzado()
        self.analizar_sistema()
    
    def cargar_ejemplo(self, matriz):
        """Carga un ejemplo predefinido de matriz"""
        self.a11_var.set(str(matriz[0][0]))
        self.a12_var.set(str(matriz[0][1]))
        self.a21_var.set(str(matriz[1][0]))
        self.a22_var.set(str(matriz[1][1]))
        self.usar_forzado.set(False)
        self.toggle_forzado()
    
    def validar_numero(self, valor):
        """Valida que el input sea un número"""
        if valor == "" or valor == "-" or valor == ".":
            return True
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    def analizar_sistema(self):
        """Analiza el sistema y actualiza la interfaz"""
        try:
            if self.modo_funcion.get():
                sistema = self._crear_sistema_personalizado()
            else:
                sistema = self._crear_sistema_matriz()
            
            if sistema:
                self.sistema_actual = sistema
                
                grapher = Grapher(sistema)
                grapher.crear_grafica(self.ax)
                self.canvas.draw()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el sistema:\n{str(e)}")
    
    def _cargar_ejemplo_funcion(self, f1, f2, params=""):
        """Carga un ejemplo de función"""
        self.f1_expr.set(f1)
        self.f2_expr.set(f2)
        self.parametros_expr.set(params)
        self.analizar_sistema()
    
    def _crear_sistema_personalizado(self):
        """Crea sistema con funciones personalizadas"""
        f1 = self.f1_expr.get().strip()
        f2 = self.f2_expr.get().strip()
        
        if not f1 or not f2:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambas funciones")
            return None
        
        # Normalizar nombres de funciones
        f1 = normalizar_funciones(f1)
        f2 = normalizar_funciones(f2)
        
        # Parsear parámetro u
        parametros = {}
        params_str = self.parametros_expr.get().strip()
        if params_str:
            try:
                parametros['u'] = float(params_str)
            except Exception as e:
                messagebox.showerror("Error en parámetro u",
                    f"Error al parsear el valor de u:\n{str(e)}\n\n"
                    f"Ingrese solo el valor numérico. Ej: 0.5")
                return None
        
        # Crear sistema directamente (la validación se hace en core.sistema)
        return SistemaDinamico2D(
            funcion_personalizada={'f1': f1, 'f2': f2, 'es_lineal': False},
            parametros=parametros
        )
    
    def _crear_sistema_matriz(self):
        """Crea sistema desde matriz"""
        try:
            matriz = [
                [float(self.a11_var.get() or 0), float(self.a12_var.get() or 0)],
                [float(self.a21_var.get() or 0), float(self.a22_var.get() or 0)]
            ]
            
            termino_forzado = None
            if self.usar_forzado.get():
                termino_forzado = {
                    'tipo': self.tipo_forzado.get(),
                    'coef1': float(self.coef1_var.get() or 0),
                    'coef2': float(self.coef2_var.get() or 0),
                    'param': float(self.param_var.get() or 1)
                }
            
            return SistemaDinamico2D(matriz, termino_forzado)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
            return None
    
    def on_canvas_click(self, event):
        """Maneja clics en la gráfica para agregar trayectorias"""
        if self.sistema_actual is None or event.inaxes != self.ax:
            return
        
        if event.xdata is None or event.ydata is None:
            return
        
        try:
            condicion_inicial = [event.xdata, event.ydata]
            
            # Calcular trayectorias hacia adelante y atrás
            solucion_fw = integrate_trajectory_limited(
                self.sistema_actual, condicion_inicial, direccion=1)
            solucion_bw = integrate_trajectory_limited(
                self.sistema_actual, condicion_inicial, direccion=-1)
            
            # Dibujar con flechas direccionales
            if len(solucion_fw) > 1:
                self.ax.plot(solucion_fw[:, 0], solucion_fw[:, 1], 
                           'b-', linewidth=2, alpha=0.8)
                # Agregar flechas a la trayectoria hacia adelante
                self._agregar_flechas_a_trayectoria(self.ax, solucion_fw, 'b')
            
            if len(solucion_bw) > 1:
                self.ax.plot(solucion_bw[:, 0], solucion_bw[:, 1], 
                           'b-', linewidth=2, alpha=0.8)
                # Agregar flechas a la trayectoria hacia atrás
                self._agregar_flechas_a_trayectoria(self.ax, solucion_bw, 'b')
            
            # Marcar punto inicial
            self.ax.plot(event.xdata, event.ydata, 'ro', markersize=8,
                        markeredgecolor='darkred', markeredgewidth=2)
            
            self.canvas.draw()
        except Exception as e:
            print(f"Error al crear trayectoria: {e}")
    
    def _agregar_flechas_a_trayectoria(self, ax, trayectoria, color):
        """Agrega flechas direccionales a una trayectoria"""
        if len(trayectoria) < 10:
            return
        
        # Agregar 3-5 flechas distribuidas uniformemente
        num_flechas = min(5, len(trayectoria) // 20)
        if num_flechas < 1:
            num_flechas = 1
        
        indices = np.linspace(10, len(trayectoria)-10, num_flechas, dtype=int)
        
        for idx in indices:
            if idx < len(trayectoria) - 1:
                x_start, y_start = trayectoria[idx]
                x_end, y_end = trayectoria[idx + 1]
                
                # Dibujar flecha
                ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                           arrowprops=dict(arrowstyle='->', color=color, 
                                         lw=2, alpha=0.8))
    
    def limpiar_trayectorias(self):
        """Limpia trayectorias y redibuja"""
        if self.sistema_actual:
            grapher = Grapher(self.sistema_actual)
            grapher.crear_grafica(self.ax)
            self.canvas.draw()
    
    def mostrar_analisis_popup(self):
        """Abre ventana popup con análisis detallado"""
        if self.sistema_actual:
            try:
                ventana_root = self._obtener_ventana_root()
                VentanaAnalisisPopup(ventana_root, self.sistema_actual)
            except Exception as e:
                messagebox.showerror("Error", f"Error al abrir análisis:\n{str(e)}")
        else:
            messagebox.showwarning("Advertencia", 
                                 "Por favor analice un sistema primero")
