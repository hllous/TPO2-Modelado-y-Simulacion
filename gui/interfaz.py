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
from visualization.grapher import Grapher
from visualization.plotter import integrate_trajectory_limited
from ui.widgets import ToolTip
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES
from input_module.ejemplos import EJEMPLOS_LINEALES, EJEMPLOS_NO_LINEALES


class InterfazGrafica:
    """Interfaz gráfica principal de la aplicación"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica
        
        Parámetros:
        - root: ventana raíz de tkinter
        """
        self.root = root
        self.root.title("Sistemas Dinámicos 2D - Análisis Completo")
        self.root.geometry("1400x800")
        self.root.configure(bg=COLORES['fondo'])
        
        # Configurar estilos
        configurar_estilos_ttk()
        
        # Variables de control
        self._inicializar_variables()
        
        # Crear interfaz
        self.crear_widgets()
        
        # Analizar sistema inicial
        self.analizar_sistema()
    
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
        
        # Sistema actual
        self.sistema_actual = None
    
    def crear_widgets(self):
        """Crea la estructura principal de widgets"""
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
    
    def _crear_panel_izquierdo(self, parent):
        """Crea panel de controles izquierdo"""
        left_frame = ttk.Frame(parent, padding="5")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Título
        self._crear_seccion_titulo(left_frame)
        
        # Selector de modo
        self._crear_selector_modo(left_frame)
        
        # Entrada de matriz
        self._crear_entrada_matriz(left_frame)
        
        # Entrada de funciones
        self._crear_entrada_funciones(left_frame)
        
        # Término forzado
        self._crear_termino_forzado(left_frame)
        
        # Ejemplos
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
        vcmd = (self.root.register(self.validar_numero), '%P')
        
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
        
        self.funciones_frame.columnconfigure(1, weight=1)
        
        # Ayuda
        ayuda_text = "Variables: x, y, t | Funciones: sin(), cos(), exp(), sqrt(), abs()"
        ttk.Label(self.funciones_frame, text=ayuda_text,
                 background='white', foreground=COLORES['texto_secundario'],
                 font=FUENTES['pequena'], wraplength=350).grid(
            row=3, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # Botón analizar
        btn_analizar = ttk.Button(self.funciones_frame, text="Analizar Sistema",
                                 style='Accent.TButton',
                                 command=self.analizar_sistema)
        btn_analizar.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky=(tk.W, tk.E))
        
        # Ejemplos rápidos
        ttk.Label(self.funciones_frame, text="Ejemplos Rápidos:",
                 style='Title.TLabel').grid(row=5, column=0, columnspan=2, pady=(15, 5))
        
        for i, (clave, datos) in enumerate(EJEMPLOS_NO_LINEALES.items()):
            btn = ttk.Button(self.funciones_frame, text=datos['nombre'],
                           command=lambda f1=datos['f1'], f2=datos['f2']: 
                           self.cargar_funcion(f1, f2))
            btn.grid(row=6+i//2, column=i%2, pady=2, padx=2, sticky=(tk.W, tk.E))
        
        # Ocultar inicialmente
        self.funciones_frame.grid_remove()
    
    def _crear_termino_forzado(self, parent):
        """Crea frame para término forzado"""
        forzado_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        forzado_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        check = ttk.Checkbutton(forzado_frame, 
                               text="Agregar Término Forzado f(t)",
                               variable=self.usar_forzado,
                               command=self.toggle_forzado,
                               style='Title.TLabel')
        check.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        
        # Frame de controles (oculto inicialmente)
        self.forzado_controls = ttk.Frame(forzado_frame)
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
        tipo_combo.bind('<<ComboboxSelected>>', self.actualizar_label_param)
        
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
        
        self.forzado_controls.grid_remove()
    
    def _crear_ejemplos(self, parent):
        """Crea frame de ejemplos predefinidos"""
        ejemplos_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        ejemplos_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(ejemplos_frame, text="Ejemplos Predefinidos",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        for i, (clave, datos) in enumerate(EJEMPLOS_LINEALES.items()):
            btn = ttk.Button(ejemplos_frame, text=datos['nombre'],
                           command=lambda m=datos['matriz']: self.cargar_ejemplo(m))
            btn.grid(row=i+1, column=0, columnspan=2, pady=2, sticky=(tk.W, tk.E))
    
    def _crear_resultados(self, parent):
        """Crea frame de resultados"""
        resultados_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        resultados_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        parent.rowconfigure(5, weight=1)
        
        ttk.Label(resultados_frame, text="Resultados del Análisis",
                 style='Title.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        text_frame = ttk.Frame(resultados_frame)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        resultados_frame.rowconfigure(1, weight=1)
        resultados_frame.columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_resultados = tk.Text(text_frame, wrap=tk.WORD,
                                       width=40, height=20,
                                       yscrollcommand=scrollbar.set,
                                       font=FUENTES['monoespaciada'],
                                       bg=COLORES['fondo'],
                                       relief='flat',
                                       padx=10, pady=10)
        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_resultados.yview)
    
    def _crear_panel_derecho(self, parent):
        """Crea panel derecho con gráfica"""
        right_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
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
            self.matriz_frame.grid_remove()
            self.funciones_frame.grid()
            self.usar_forzado.set(False)
            self.toggle_forzado()
        else:
            self.funciones_frame.grid_remove()
            self.matriz_frame.grid()
    
    def toggle_forzado(self):
        """Muestra/oculta controles del término forzado"""
        if self.usar_forzado.get():
            self.forzado_controls.grid()
            self.actualizar_label_param()
        else:
            self.forzado_controls.grid_remove()
        self.actualizar_formula_forzado()
    
    def actualizar_label_param(self, event=None):
        """Actualiza label del parámetro según tipo"""
        tipo = self.tipo_forzado.get()
        
        if tipo == 'constante':
            self.label_param.config(text="(no aplica)")
            self.entry_param.config(state='disabled')
        elif tipo == 'exponencial':
            self.label_param.config(text="k:")
            self.entry_param.config(state='normal')
        elif tipo in ['seno', 'coseno']:
            self.label_param.config(text="ω:")
            self.entry_param.config(state='normal')
        
        self.actualizar_formula_forzado()
    
    def actualizar_formula_forzado(self):
        """Actualiza fórmula mostrada del término forzado"""
        if not self.usar_forzado.get():
            return
        
        try:
            c1 = float(self.coef1_var.get() or 0)
            c2 = float(self.coef2_var.get() or 0)
            param = float(self.param_var.get() or 1)
            tipo = self.tipo_forzado.get()
            
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
            pass
    
    def cargar_funcion(self, f1, f2):
        """Carga un ejemplo de función"""
        self.f1_expr.set(f1)
        self.f2_expr.set(f2)
        self.analizar_sistema()
    
    def cargar_ejemplo(self, matriz):
        """Carga un ejemplo predefinido de matriz"""
        self.a11_var.set(str(matriz[0][0]))
        self.a12_var.set(str(matriz[0][1]))
        self.a21_var.set(str(matriz[1][0]))
        self.a22_var.set(str(matriz[1][1]))
        self.usar_forzado.set(False)
        self.toggle_forzado()
        self.analizar_sistema()
    
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
                self._mostrar_resultados(sistema)
                
                grapher = Grapher(sistema)
                grapher.crear_grafica(self.ax)
                self.canvas.draw()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el sistema:\n{str(e)}")
    
    def _crear_sistema_personalizado(self):
        """Crea sistema con funciones personalizadas"""
        f1 = self.f1_expr.get().strip()
        f2 = self.f2_expr.get().strip()
        
        if not f1 or not f2:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambas funciones")
            return None
        
        # Validar funciones
        try:
            test_vars = {
                'x': 1.0, 'y': 1.0, 'x1': 1.0, 'x2': 1.0, 't': 0.0,
                'np': np, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                'abs': np.abs, 'pi': np.pi, 'e': np.e
            }
            float(eval(f1, {"__builtins__": {}}, test_vars))
            float(eval(f2, {"__builtins__": {}}, test_vars))
        except Exception as e:
            messagebox.showerror("Error en funciones", 
                f"Error al evaluar:\n{str(e)}")
            return None
        
        return SistemaDinamico2D(
            funcion_personalizada={'f1': f1, 'f2': f2, 'es_lineal': False}
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
                self.actualizar_formula_forzado()
            
            return SistemaDinamico2D(matriz, termino_forzado)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
            return None
    
    def _mostrar_resultados(self, sistema):
        """Muestra resultados del análisis"""
        self.text_resultados.delete(1.0, tk.END)
        
        resultado = self._generar_texto_resultados(sistema)
        self.text_resultados.insert(1.0, resultado)
    
    def _generar_texto_resultados(self, sistema):
        """Genera el texto con resultados del análisis"""
        resultado = "═" * 50 + "\n"
        
        if sistema.funcion_personalizada:
            resultado += self._texto_sistema_personalizado(sistema)
        elif sistema.termino_forzado:
            resultado += self._texto_sistema_no_homogeneo(sistema)
        else:
            resultado += self._texto_sistema_lineal(sistema)
        
        resultado += "\n" + "=" * 50 + "\n"
        return resultado
    
    def _texto_sistema_personalizado(self, sistema):
        """Texto para sistema personalizado"""
        texto = "   SISTEMA DINÁMICO PERSONALIZADO\n"
        texto += "═" * 50 + "\n\n"
        texto += f"dx₁/dt = {sistema.funcion_personalizada['f1']}\n"
        texto += f"dx₂/dt = {sistema.funcion_personalizada['f2']}\n\n"
        texto += "Tipo: " + ("NO LINEAL" if sistema.es_no_lineal else "Lineal") + "\n"
        return texto
    
    def _texto_sistema_no_homogeneo(self, sistema):
        """Texto para sistema no homogéneo"""
        texto = "   SISTEMA DINÁMICO 2D NO HOMOGÉNEO\n"
        texto += "═" * 50 + "\n\n"
        
        texto += "Matriz A:\n"
        texto += f"  ⎡ {sistema.A[0,0]:8.4f}  {sistema.A[0,1]:8.4f} ⎤\n"
        texto += f"  ⎣ {sistema.A[1,0]:8.4f}  {sistema.A[1,1]:8.4f} ⎦\n\n"
        
        texto += "Término forzado:\n"
        tf = sistema.termino_forzado
        if tf['tipo'] == 'constante':
            texto += f"  f(t) = [{tf['coef1']:.4f}, {tf['coef2']:.4f}]ᵀ\n"
        else:
            texto += f"  f(t) = [{tf['coef1']:.4f}{tf['tipo']}({tf.get('param',1):.4f}t), "
            texto += f"{tf['coef2']:.4f}{tf['tipo']}({tf.get('param',1):.4f}t)]ᵀ\n"
        
        texto += self._texto_autovalores(sistema)
        return texto
    
    def _texto_sistema_lineal(self, sistema):
        """Texto para sistema lineal homogéneo"""
        texto = "   ANÁLISIS DEL SISTEMA DINÁMICO 2D\n"
        texto += "═" * 50 + "\n\n"
        
        texto += "Matriz A:\n"
        texto += f"  ⎡ {sistema.A[0,0]:8.4f}  {sistema.A[0,1]:8.4f} ⎤\n"
        texto += f"  ⎣ {sistema.A[1,0]:8.4f}  {sistema.A[1,1]:8.4f} ⎦\n\n"
        
        texto += f"Determinante: {sistema.determinante:.6f}\n"
        texto += f"Traza:        {sistema.traza:.6f}\n\n"
        
        texto += self._texto_autovalores(sistema)
        texto += self._texto_autovectores(sistema)
        
        tipo, estab = sistema.clasificar_punto_equilibrio()
        texto += f"\nCLASIFICACIÓN:\n"
        texto += f"  Tipo:        {tipo}\n"
        texto += f"  Estabilidad: {estab}\n"
        
        return texto
    
    def _texto_autovalores(self, sistema):
        """Genera texto de autovalores"""
        texto = "─" * 50 + "\n\n"
        texto += "Autovalores:\n"
        for i, autoval in enumerate(sistema.autovalores, 1):
            if np.iscomplex(autoval):
                texto += f"  λ{i} = {autoval.real:.6f} + {autoval.imag:.6f}i\n"
            else:
                texto += f"  λ{i} = {autoval.real:.6f}\n"
        return texto + "\n"
    
    def _texto_autovectores(self, sistema):
        """Genera texto de autovectores"""
        texto = "─" * 50 + "\n\n"
        texto += "Autovectores:\n"
        for i in range(2):
            autovec = sistema.autovectores[:, i]
            if np.iscomplex(autovec[0]):
                texto += f"  v{i+1} = [{autovec[0].real:.4f} + {autovec[0].imag:.4f}i,\n"
                texto += f"        {autovec[1].real:.4f} + {autovec[1].imag:.4f}i]ᵀ\n"
            else:
                texto += f"  v{i+1} = [{autovec[0].real:.6f},\n"
                texto += f"        {autovec[1].real:.6f}]ᵀ\n"
        return texto + "\n"
    
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
            
            # Dibujar
            if len(solucion_fw) > 1:
                self.ax.plot(solucion_fw[:, 0], solucion_fw[:, 1], 
                           'b-', linewidth=2, alpha=0.8)
            
            if len(solucion_bw) > 1:
                self.ax.plot(solucion_bw[:, 0], solucion_bw[:, 1], 
                           'b-', linewidth=2, alpha=0.8)
            
            # Marcar punto inicial
            self.ax.plot(event.xdata, event.ydata, 'ro', markersize=8,
                        markeredgecolor='darkred', markeredgewidth=2)
            
            self.canvas.draw()
        except Exception as e:
            print(f"Error al crear trayectoria: {e}")
    
    def limpiar_trayectorias(self):
        """Limpia trayectorias y redibuja"""
        if self.sistema_actual:
            grapher = Grapher(self.sistema_actual)
            grapher.crear_grafica(self.ax)
            self.canvas.draw()
