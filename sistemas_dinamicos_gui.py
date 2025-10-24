"""
Sistema Dinámico 2D Homogéneo - Interfaz Gráfica
Análisis de sistemas de ecuaciones diferenciales dx/dt = Ax
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.integrate import odeint
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')


class ToolTip:
    """Clase para crear tooltips en los widgets"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        background="#ffffe0", relief="solid", 
                        borderwidth=1, font=("Arial", 9),
                        padx=5, pady=3)
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class SistemaDinamico2D:
    def __init__(self, matriz=None, termino_forzado=None, funcion_personalizada=None):
        """
        Inicializa el sistema dinámico
        
        Parámetros:
        - matriz: matriz 2x2 para sistemas lineales (dx/dt = Ax)
        - termino_forzado: dict para términos forzados lineales
        - funcion_personalizada: dict con funciones f1(x1,x2,t) y f2(x1,x2,t)
          {
              'f1': 'expresión con x1, x2, t',
              'f2': 'expresión con x1, x2, t',
              'es_lineal': bool
          }
        """
        self.funcion_personalizada = funcion_personalizada
        
        if funcion_personalizada:
            # Sistema personalizado (puede ser no lineal)
            self.A = None
            self.es_no_lineal = not funcion_personalizada.get('es_lineal', False)
            self.autovalores = None
            self.autovectores = None
            self.determinante = None
            self.traza = None
        else:
            # Sistema lineal tradicional
            self.A = np.array(matriz, dtype=float)
            self.es_no_lineal = False
            self.autovalores, self.autovectores = np.linalg.eig(self.A)
            self.determinante = np.linalg.det(self.A)
            self.traza = np.trace(self.A)
        
        self.termino_forzado = termino_forzado
    
    def encontrar_puntos_equilibrio(self, xlim=(-5, 5), ylim=(-5, 5), tolerancia=0.01):
        """
        Encuentra puntos de equilibrio del sistema donde dx/dt = 0 y dy/dt = 0
        
        Retorna:
        - lista de tuplas (x, y) con los puntos de equilibrio encontrados
        """
        puntos_equilibrio = []
        
        # Para sistemas lineales homogéneos, (0,0) es siempre punto de equilibrio
        if not self.termino_forzado and not self.funcion_personalizada:
            return [(0, 0)]
        
        # Para sistemas no homogéneos o personalizados, buscar numéricamente
        from scipy.optimize import fsolve
        
        # Función que retorna las derivadas
        def sistema_eq(X):
            return self.sistema_ecuaciones(X, 0)
        
        # Probar desde varios puntos iniciales - expandido
        puntos_prueba = [
            (0, 0),
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1),
            (2, 0), (-2, 0), (0, 2), (0, -2),
            (2, 2), (-2, -2), (2, -2), (-2, 2),
            (0.5, 0.5), (-0.5, -0.5), (1.5, 1.5), (-1.5, -1.5)
        ]
        
        for x0, y0 in puntos_prueba:
            try:
                sol = fsolve(sistema_eq, [x0, y0])
                # Verificar que la solución está dentro de los límites
                if xlim[0] <= sol[0] <= xlim[1] and ylim[0] <= sol[1] <= ylim[1]:
                    # Verificar que realmente es un punto de equilibrio
                    derivadas = sistema_eq(sol)
                    if abs(derivadas[0]) < tolerancia and abs(derivadas[1]) < tolerancia:
                        # Verificar que no esté duplicado
                        es_nuevo = True
                        for px, py in puntos_equilibrio:
                            if abs(sol[0] - px) < tolerancia and abs(sol[1] - py) < tolerancia:
                                es_nuevo = False
                                break
                        if es_nuevo:
                            puntos_equilibrio.append((sol[0], sol[1]))
                            print(f"Punto de equilibrio encontrado: ({sol[0]:.4f}, {sol[1]:.4f})")
                            print(f"  Verificación: dx/dt = {derivadas[0]:.6f}, dy/dt = {derivadas[1]:.6f}")
            except:
                continue
        
        # Si no se encontró ninguno, retornar al menos (0,0) para sistemas lineales
        if len(puntos_equilibrio) == 0 and not self.funcion_personalizada:
            puntos_equilibrio.append((0, 0))
        
        return puntos_equilibrio
    
    def clasificar_punto_equilibrio(self):
        """Clasifica el tipo de punto de equilibrio según los autovalores"""
        if self.es_no_lineal:
            return "Sistema No Lineal", "Análisis requiere linealización"
        
        if self.autovalores is None:
            return "N/A", "Sistema personalizado"
        
        lambda1, lambda2 = self.autovalores
        
        if np.iscomplex(lambda1) or np.iscomplex(lambda2):
            parte_real = lambda1.real
            if abs(parte_real) < 1e-10:
                return "Centro", "Neutral (órbitas cerradas)"
            elif parte_real < 0:
                return "Espiral (Foco)", "Estable (atractor)"
            else:
                return "Espiral (Foco)", "Inestable (repulsor)"
        else:
            if abs(lambda1) < 1e-10 or abs(lambda2) < 1e-10:
                return "Degenerado (autovalor cero)", "Caso especial"
            
            if lambda1 * lambda2 > 0:
                if abs(lambda1 - lambda2) < 1e-10:
                    return "Nodo Estrella", "Estable" if lambda1 < 0 else "Inestable"
                else:
                    tipo = "Nodo Propio"
                    estabilidad = "Estable (atractor)" if lambda1 < 0 else "Inestable (repulsor)"
                    return tipo, estabilidad
            else:
                return "Punto Silla", "Inestable (hiperbólico)"
    
    def sistema_ecuaciones(self, X, t):
        """Define el sistema de ecuaciones diferenciales dx/dt = f(x,y,t)"""
        x1, x2 = X
        
        # Sistema personalizado con funciones
        if self.funcion_personalizada:
            try:
                # Evaluar las funciones personalizadas
                f1_expr = self.funcion_personalizada['f1']
                f2_expr = self.funcion_personalizada['f2']
                
                # Variables disponibles para eval
                variables = {
                    'x1': x1, 'x2': x2, 't': t,
                    'x': x1, 'y': x2,  # Alias principales
                    'np': np,
                    'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                    'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                    'abs': np.abs, 'pi': np.pi, 'e': np.e
                }
                
                dx1dt = float(eval(f1_expr, {"__builtins__": {}}, variables))
                dx2dt = float(eval(f2_expr, {"__builtins__": {}}, variables))
                
                return np.array([dx1dt, dx2dt])
            except Exception as e:
                print(f"Error evaluando funciones: {e}")
                return np.array([0.0, 0.0])
        
        # Sistema lineal tradicional: dx/dt = Ax + f(t)
        dXdt = np.dot(self.A, X)
        
        # Agregar término forzado si existe
        if self.termino_forzado:
            tipo = self.termino_forzado['tipo']
            c1 = self.termino_forzado['coef1']
            c2 = self.termino_forzado['coef2']
            param = self.termino_forzado.get('param', 0)
            
            if tipo == 'constante':
                dXdt[0] += c1
                dXdt[1] += c2
            elif tipo == 'exponencial':
                dXdt[0] += c1 * np.exp(param * t)
                dXdt[1] += c2 * np.exp(param * t)
            elif tipo == 'seno':
                dXdt[0] += c1 * np.sin(param * t)
                dXdt[1] += c2 * np.sin(param * t)
            elif tipo == 'coseno':
                dXdt[0] += c1 * np.cos(param * t)
                dXdt[1] += c2 * np.cos(param * t)
        
        return dXdt
    
    def crear_grafica(self, ax, xlim=(-3, 3), ylim=(-3, 3), n_puntos=20):
        """Crea la gráfica del sistema en el axis proporcionado"""
        ax.clear()
        
        # Para sistemas no lineales, ajustar verificación
        if self.funcion_personalizada:
            tiene_autovalores = False
        else:
            tiene_autovalores = self.autovalores is not None
        
        # Crear malla para el campo de direcciones
        x = np.linspace(xlim[0], xlim[1], n_puntos)
        y = np.linspace(ylim[0], ylim[1], n_puntos)
        X, Y = np.meshgrid(x, y)
        
        # Calcular derivadas en cada punto
        if self.funcion_personalizada:
            # Para sistemas personalizados, evaluar las funciones en cada punto
            U = np.zeros_like(X)
            V = np.zeros_like(Y)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    derivadas = self.sistema_ecuaciones([X[i,j], Y[i,j]], 0)
                    U[i,j] = derivadas[0]
                    V[i,j] = derivadas[1]
        else:
            # Para sistemas lineales, usar la matriz
            U = self.A[0, 0] * X + self.A[0, 1] * Y
            V = self.A[1, 0] * X + self.A[1, 1] * Y
        
        # Normalizar
        M = np.sqrt(U**2 + V**2)
        M[M == 0] = 1
        U_norm = U / M
        V_norm = V / M
        
        # Campo de direcciones
        ax.quiver(X, Y, U_norm, V_norm, M, cmap='viridis', alpha=0.6)
        
        # Trayectorias automáticas - ELIMINADAS
        # Ahora solo se crean con clics del usuario
        
        # Autovectores (solo para sistemas lineales homogéneos)
        if tiene_autovalores and self.autovalores is not None and not self.termino_forzado:
            if not np.iscomplex(self.autovalores[0]):
                for i in range(2):
                    v = self.autovectores[:, i].real
                    if abs(self.autovalores[i]) > 1e-10:
                        scale = 2.5
                        # Dibujar autovectores desde el origen
                        ax.arrow(0, 0, scale * v[0], scale * v[1], 
                                head_width=0.2, head_length=0.15, 
                                fc='red', ec='red', linewidth=2, alpha=0.8)
                        ax.arrow(0, 0, -scale * v[0], -scale * v[1], 
                                head_width=0.2, head_length=0.15, 
                                fc='red', ec='red', linewidth=2, alpha=0.8)
        
        # Encontrar y marcar puntos de equilibrio
        puntos_eq = self.encontrar_puntos_equilibrio(xlim, ylim)
        if puntos_eq:
            for i, (px, py) in enumerate(puntos_eq):
                if i == 0:
                    ax.plot(px, py, 'ko', markersize=12, markeredgecolor='white', 
                            markeredgewidth=2, label='Punto de equilibrio', zorder=5)
                else:
                    ax.plot(px, py, 'ko', markersize=12, markeredgecolor='white', 
                            markeredgewidth=2, zorder=5)
        
        # Configuración
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        
        # Etiquetas de ejes - usar x,y para funciones personalizadas, x₁,x₂ para matrices
        if self.funcion_personalizada:
            ax.set_xlabel('x', fontsize=11)
            ax.set_ylabel('y', fontsize=11)
        else:
            ax.set_xlabel('x₁', fontsize=11)
            ax.set_ylabel('x₂', fontsize=11)
        
        tipo, estabilidad = self.clasificar_punto_equilibrio()
        if self.termino_forzado:
            titulo = f'Sistema No Homogéneo: dx/dt = Ax + f(t)\n'
            titulo += f'Parte homogénea: {tipo} ({estabilidad})'
        elif self.funcion_personalizada:
            titulo = f'Sistema Personalizado\n'
            if self.es_no_lineal:
                titulo += 'Sistema No Lineal'
            else:
                titulo += 'Sistema Lineal'
        else:
            titulo = f'Sistema Dinámico 2D: {tipo}\n{estabilidad}'
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')


class InterfazGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistemas Dinámicos 2D - Análisis Completo")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.a11_var = tk.StringVar(value="-1")
        self.a12_var = tk.StringVar(value="0")
        self.a21_var = tk.StringVar(value="0")
        self.a22_var = tk.StringVar(value="-2")
        
        # Variables para término forzado
        self.usar_forzado = tk.BooleanVar(value=False)
        self.tipo_forzado = tk.StringVar(value="constante")
        self.coef1_var = tk.StringVar(value="0")
        self.coef2_var = tk.StringVar(value="0")
        self.param_var = tk.StringVar(value="1")
        
        # Variables para funciones personalizadas
        self.modo_funcion = tk.BooleanVar(value=False)
        self.f1_expr = tk.StringVar(value="-x")
        self.f2_expr = tk.StringVar(value="-y")
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Crear widgets
        self.crear_widgets()
        
        # Analizar el sistema inicial
        self.analizar_sistema()
    
    def configurar_estilos(self):
        """Configura los estilos de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones
        style.configure('Accent.TButton',
                       background='#2196F3',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        
        style.map('Accent.TButton',
                 background=[('active', '#1976D2')])
        
        # Estilo para frames
        style.configure('Card.TFrame',
                       background='white',
                       relief='flat',
                       borderwidth=2)
        
        # Estilo para labels
        style.configure('Title.TLabel',
                       background='white',
                       font=('Arial', 12, 'bold'),
                       foreground='#333333')
        
        style.configure('Subtitle.TLabel',
                       background='white',
                       font=('Arial', 10),
                       foreground='#666666')
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo (controles)
        self.crear_panel_izquierdo(main_frame)
        
        # Panel derecho (gráfica)
        self.crear_panel_derecho(main_frame)
    
    def crear_panel_izquierdo(self, parent):
        """Crea el panel de controles"""
        left_frame = ttk.Frame(parent, padding="5")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Título
        titulo_frame = ttk.Frame(left_frame, style='Card.TFrame', padding="15")
        titulo_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(titulo_frame, text="Sistemas Dinámicos 2D",
                 style='Title.TLabel', font=('Arial', 16, 'bold')).grid(row=0, column=0)
        ttk.Label(titulo_frame, text="Sistemas lineales, no lineales, homogéneos y no homogéneos",
                 style='Subtitle.TLabel').grid(row=1, column=0, pady=(5, 0))
        
        # Frame de entrada de matriz
        self.crear_selector_modo(left_frame)
        self.crear_entrada_matriz(left_frame)
        self.crear_entrada_funciones(left_frame)
        
        # Frame de término forzado
        self.crear_termino_forzado(left_frame)
        
        # Frame de ejemplos
        self.crear_ejemplos(left_frame)
        
        # Frame de resultados
        self.crear_resultados(left_frame)
    
    def crear_entrada_matriz(self, parent):
        """Crea el frame para ingresar la matriz"""
        self.matriz_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        self.matriz_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.matriz_frame, text="Matriz del Sistema A (2×2)",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Etiquetas de matriz
        ttk.Label(self.matriz_frame, text="⎡", font=('Arial', 40), background='white').grid(
            row=1, column=0, rowspan=2)
        ttk.Label(self.matriz_frame, text="⎤", font=('Arial', 40), background='white').grid(
            row=1, column=3, rowspan=2)
        
        # Entradas
        entry_width = 12
        vcmd = (self.root.register(self.validar_numero), '%P')
        
        self.entry_a11 = ttk.Entry(self.matriz_frame, textvariable=self.a11_var,
                                   width=entry_width, justify='center',
                                   validate='key', validatecommand=vcmd,
                                   font=('Arial', 12))
        self.entry_a11.grid(row=1, column=1, padx=5, pady=5)
        ToolTip(self.entry_a11, "Elemento a₁₁ de la matriz")
        
        self.entry_a12 = ttk.Entry(self.matriz_frame, textvariable=self.a12_var,
                                   width=entry_width, justify='center',
                                   validate='key', validatecommand=vcmd,
                                   font=('Arial', 12))
        self.entry_a12.grid(row=1, column=2, padx=5, pady=5)
        ToolTip(self.entry_a12, "Elemento a₁₂ de la matriz")
        
        self.entry_a21 = ttk.Entry(self.matriz_frame, textvariable=self.a21_var,
                                   width=entry_width, justify='center',
                                   validate='key', validatecommand=vcmd,
                                   font=('Arial', 12))
        self.entry_a21.grid(row=2, column=1, padx=5, pady=5)
        ToolTip(self.entry_a21, "Elemento a₂₁ de la matriz")
        
        self.entry_a22 = ttk.Entry(self.matriz_frame, textvariable=self.a22_var,
                                   width=entry_width, justify='center',
                                   validate='key', validatecommand=vcmd,
                                   font=('Arial', 12))
        self.entry_a22.grid(row=2, column=2, padx=5, pady=5)
        ToolTip(self.entry_a22, "Elemento a₂₂ de la matriz")
        
        # Botón analizar
        btn_analizar = ttk.Button(self.matriz_frame, text="Analizar Sistema",
                  style='Accent.TButton',
                  command=self.analizar_sistema)
        btn_analizar.grid(row=3, column=0, columnspan=4, pady=(15, 0), sticky=(tk.W, tk.E))
        ToolTip(btn_analizar, "Analiza el sistema con la matriz ingresada")
    
    def crear_selector_modo(self, parent):
        """Crea el selector de modo (Matriz vs Función)"""
        modo_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        modo_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(modo_frame, text="Modo de Entrada:",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Radio buttons para seleccionar modo
        ttk.Radiobutton(modo_frame, text="Matriz (Sistema Lineal)", 
                       variable=self.modo_funcion, value=False,
                       command=self.cambiar_modo).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(modo_frame, text="Funciones (Lineal/No Lineal)", 
                       variable=self.modo_funcion, value=True,
                       command=self.cambiar_modo).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ToolTip(modo_frame, "Elige entre ingresar matriz o funciones personalizadas")
    
    def crear_entrada_funciones(self, parent):
        """Crea el frame para ingresar funciones personalizadas"""
        self.funciones_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        self.funciones_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.funciones_frame, text="Funciones del Sistema",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Label(self.funciones_frame, text="dx₁/dt =", 
                 background='white', font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.E, padx=(0, 5), pady=5)
        
        self.entry_f1 = ttk.Entry(self.funciones_frame, textvariable=self.f1_expr,
                                  width=30, font=('Consolas', 10))
        self.entry_f1.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.funciones_frame, text="dx₂/dt =", 
                 background='white', font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.E, padx=(0, 5), pady=5)
        
        self.entry_f2 = ttk.Entry(self.funciones_frame, textvariable=self.f2_expr,
                                  width=30, font=('Consolas', 10))
        self.entry_f2.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.funciones_frame.columnconfigure(1, weight=1)
        
        # Ayuda de sintaxis
        ayuda_text = "Variables: x, y, t (también x1, x2)\n"
        ayuda_text += "Funciones: sin(), cos(), exp(), sqrt(), abs()\n"
        ayuda_text += "Ejemplos: y, x**3-x, sin(y), -9*x + 2*y, x*y"
        
        ttk.Label(self.funciones_frame, text=ayuda_text,
                 background='white', foreground='#666',
                 font=('Arial', 8), wraplength=350).grid(
            row=3, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
        
        # Botón analizar
        btn_analizar_func = ttk.Button(self.funciones_frame, text="Analizar Sistema",
                  style='Accent.TButton',
                  command=self.analizar_sistema)
        btn_analizar_func.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky=(tk.W, tk.E))
        
        # Ejemplos no lineales
        ttk.Label(self.funciones_frame, text="Ejemplos Rápidos:",
                 style='Title.TLabel').grid(row=5, column=0, columnspan=2, pady=(15, 5))
        
        ejemplos_nl = [
            ("Péndulo", "y", "sin(x)"),
            ("Van der Pol", "y", "y*(1-x**2)-x"),
            ("Lotka-Volterra", "x*(1-y)", "-y*(1-x)"),
            ("Duffing", "y", "x - x**3"),
        ]
        
        for i, (nombre, f1, f2) in enumerate(ejemplos_nl):
            btn = ttk.Button(self.funciones_frame, text=nombre,
                           command=lambda f1=f1, f2=f2: self.cargar_funcion(f1, f2))
            btn.grid(row=6+i//2, column=i%2, pady=2, padx=2, sticky=(tk.W, tk.E))
        
        # Ocultar inicialmente
        self.funciones_frame.grid_remove()
    
    def cambiar_modo(self):
        """Cambia entre modo matriz y modo función"""
        if self.modo_funcion.get():
            # Mostrar funciones, ocultar matriz
            self.matriz_frame.grid_remove()
            self.funciones_frame.grid()
            # Desactivar término forzado en modo función
            self.usar_forzado.set(False)
            self.toggle_forzado()
        else:
            # Mostrar matriz, ocultar funciones
            self.funciones_frame.grid_remove()
            self.matriz_frame.grid()
    
    def cargar_funcion(self, f1, f2):
        """Carga un ejemplo de función"""
        self.f1_expr.set(f1)
        self.f2_expr.set(f2)
        self.analizar_sistema()
    
    def crear_termino_forzado(self, parent):
        """Crea el frame para el término forzado"""
        forzado_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        forzado_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Checkbox para activar
        check_forzado = ttk.Checkbutton(forzado_frame, 
                                        text="Agregar Término Forzado f(t)",
                                        variable=self.usar_forzado,
                                        command=self.toggle_forzado,
                                        style='Title.TLabel')
        check_forzado.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        
        # Frame contenedor para los controles (inicialmente oculto)
        self.forzado_controls = ttk.Frame(forzado_frame)
        self.forzado_controls.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Tipo de función
        ttk.Label(self.forzado_controls, text="Tipo:", background='white').grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        tipo_combo = ttk.Combobox(self.forzado_controls, 
                                  textvariable=self.tipo_forzado,
                                  values=['constante', 'exponencial', 'seno', 'coseno'],
                                  state='readonly',
                                  width=12)
        tipo_combo.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
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
        
        # Parámetro (k o ω)
        self.label_param = tk.Label(self.forzado_controls, text="(no aplica)", 
                                    background='white')
        self.label_param.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_param = ttk.Entry(self.forzado_controls, 
                                     textvariable=self.param_var,
                                     width=8, justify='center',
                                     state='disabled')
        self.entry_param.grid(row=2, column=1, pady=5, padx=(5, 0))
        
        # Fórmula actual
        self.label_formula = tk.Label(self.forzado_controls, 
                                      text="f(t) = [0, 0]ᵀ",
                                      background='white',
                                      font=('Consolas', 9),
                                      foreground='#0066cc')
        self.label_formula.grid(row=3, column=0, columnspan=4, pady=(10, 0))
        
        # Ocultar controles inicialmente
        self.forzado_controls.grid_remove()
        
        # Tooltips
        ToolTip(check_forzado, "Activa para agregar términos no homogéneos al sistema")
        ToolTip(tipo_combo, "Tipo de función forzada: constante, e^(kt), sin(ωt), cos(ωt)")
    
    def toggle_forzado(self):
        """Muestra u oculta los controles del término forzado"""
        if self.usar_forzado.get():
            self.forzado_controls.grid()
            self.actualizar_label_param()
        else:
            self.forzado_controls.grid_remove()
        self.actualizar_formula_forzado()
    
    def actualizar_label_param(self, event=None):
        """Actualiza el label del parámetro según el tipo"""
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
        """Actualiza la fórmula mostrada"""
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
    
    def crear_ejemplos(self, parent):
        """Crea el frame de ejemplos predefinidos"""
        ejemplos_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        ejemplos_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(ejemplos_frame, text="Ejemplos Predefinidos",
                 style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ejemplos = [
            ("Nodo Estable", [[-1, 0], [0, -2]]),
            ("Nodo Inestable", [[1, 0], [0, 2]]),
            ("Punto Silla", [[1, 0], [0, -1]]),
            ("Espiral Estable", [[-0.5, 1], [-1, -0.5]]),
            ("Espiral Inestable", [[0.5, 1], [-1, 0.5]]),
            ("Centro", [[0, 1], [-1, 0]]),
            ("Nodo Degenerado", [[-1, 1], [0, -1]])
        ]
        
        for i, (nombre, matriz) in enumerate(ejemplos):
            btn = ttk.Button(ejemplos_frame, text=nombre,
                           command=lambda m=matriz: self.cargar_ejemplo(m))
            btn.grid(row=i+1, column=0, columnspan=2, pady=2, sticky=(tk.W, tk.E))
    
    def crear_resultados(self, parent):
        """Crea el frame de resultados"""
        resultados_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        resultados_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        parent.rowconfigure(5, weight=1)
        
        ttk.Label(resultados_frame, text="Resultados del Análisis",
                 style='Title.TLabel').grid(row=0, column=0, sticky=(tk.W), pady=(0, 10))
        
        # Área de texto con scrollbar
        text_frame = ttk.Frame(resultados_frame)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        resultados_frame.rowconfigure(1, weight=1)
        resultados_frame.columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_resultados = tk.Text(text_frame, wrap=tk.WORD,
                                       width=40, height=20,
                                       yscrollcommand=scrollbar.set,
                                       font=('Consolas', 9),
                                       bg='#f9f9f9',
                                       relief='flat',
                                       padx=10, pady=10)
        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_resultados.yview)
    
    def crear_panel_derecho(self, parent):
        """Crea el panel de la gráfica"""
        right_frame = ttk.Frame(parent, style='Card.TFrame', padding="15")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(right_frame, text="Visualización del Sistema",
                 style='Title.TLabel').grid(row=0, column=0, pady=(0, 10))
        
        # Frame para botones de control
        controles_frame = ttk.Frame(right_frame)
        controles_frame.grid(row=0, column=0, pady=(0, 10), sticky=tk.E, padx=10)
        
        btn_limpiar = ttk.Button(controles_frame, text="Limpiar Trayectorias",
                                command=self.limpiar_trayectorias)
        btn_limpiar.pack(side=tk.RIGHT, padx=5)
        ToolTip(btn_limpiar, "Limpia las trayectorias agregadas con clics")
        
        info_label = ttk.Label(controles_frame, 
                              text="Clic en la gráfica para generar trayectorias",
                              background='white', font=('Arial', 8),
                              foreground='#666')
        info_label.pack(side=tk.RIGHT, padx=10)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(8, 7), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Conectar evento de clic
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        
        # Variable para almacenar el sistema actual
        self.sistema_actual = None
        
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)
    
    def validar_numero(self, valor):
        """Valida que el input sea un número válido"""
        if valor == "" or valor == "-" or valor == ".":
            return True
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    def cargar_ejemplo(self, matriz):
        """Carga un ejemplo predefinido"""
        self.a11_var.set(str(matriz[0][0]))
        self.a12_var.set(str(matriz[0][1]))
        self.a21_var.set(str(matriz[1][0]))
        self.a22_var.set(str(matriz[1][1]))
        # Desactivar término forzado al cargar ejemplo
        self.usar_forzado.set(False)
        self.toggle_forzado()
        self.analizar_sistema()
    
    def analizar_sistema(self):
        """Analiza el sistema y actualiza la interfaz"""
        try:
            # Modo función personalizada
            if self.modo_funcion.get():
                f1 = self.f1_expr.get().strip()
                f2 = self.f2_expr.get().strip()
                
                if not f1 or not f2:
                    messagebox.showwarning("Advertencia", "Por favor ingrese ambas funciones")
                    return
                
                # Validar que las funciones se puedan evaluar
                try:
                    test_vars = {
                        'x': 1.0, 'y': 1.0, 'x1': 1.0, 'x2': 1.0, 't': 0.0,
                        'np': np,
                        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                        'abs': np.abs, 'pi': np.pi, 'e': np.e
                    }
                    float(eval(f1, {"__builtins__": {}}, test_vars))
                    float(eval(f2, {"__builtins__": {}}, test_vars))
                except Exception as e:
                    messagebox.showerror("Error en funciones", 
                        f"Error al evaluar las funciones:\n{str(e)}\n\n"
                        f"Verifica la sintaxis:\n"
                        f"dx/dt = {f1}\n"
                        f"dy/dt = {f2}")
                    return
                
                funcion_personalizada = {
                    'f1': f1,
                    'f2': f2,
                    'es_lineal': False  # Asumir no lineal por defecto
                }
                
                # Crear sistema
                sistema = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
            
            # Modo matriz
            else:
                # Obtener valores de la matriz
                a11 = float(self.a11_var.get() or 0)
                a12 = float(self.a12_var.get() or 0)
                a21 = float(self.a21_var.get() or 0)
                a22 = float(self.a22_var.get() or 0)
                
                matriz = [[a11, a12], [a21, a22]]
                
                # Obtener término forzado si está activado
                termino_forzado = None
                if self.usar_forzado.get():
                    termino_forzado = {
                        'tipo': self.tipo_forzado.get(),
                        'coef1': float(self.coef1_var.get() or 0),
                        'coef2': float(self.coef2_var.get() or 0),
                        'param': float(self.param_var.get() or 1)
                    }
                    self.actualizar_formula_forzado()
                
                # Crear sistema
                sistema = SistemaDinamico2D(matriz, termino_forzado)
            
            # Actualizar resultados
            self.mostrar_resultados(sistema)
            
            # Guardar sistema actual para clics
            self.sistema_actual = sistema
            
            # Actualizar gráfica
            sistema.crear_grafica(self.ax)
            self.canvas.draw()
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            messagebox.showerror("Error", f"Error al analizar el sistema:\n{str(e)}\n\nDetalle:\n{error_detail}")
    
    def on_canvas_click(self, event):
        """Maneja clics en la gráfica para agregar trayectorias interactivas"""
        # Verificar que hay un sistema analizado y que el clic es válido
        if self.sistema_actual is None:
            return
        
        if event.inaxes != self.ax:
            return
        
        # Obtener coordenadas del clic
        x_click = event.xdata
        y_click = event.ydata
        
        if x_click is None or y_click is None:
            return
        
        try:
            condicion_inicial = [x_click, y_click]
            
            # Límites para la integración
            max_distance = 100  # Distancia máxima desde el origen
            min_distance = 0.01  # Distancia mínima al punto de equilibrio
            
            # Función para verificar límites durante la integración
            def trayectoria_limitada(t_span, direccion=1):
                """Calcula trayectoria con límites para evitar problemas numéricos"""
                puntos = []
                t_actual = 0
                estado = condicion_inicial.copy()
                dt = 0.01 * direccion  # Paso de tiempo pequeño
                
                for _ in range(1000):  # Máximo 1000 pasos
                    # Verificar distancia al origen
                    distancia = np.sqrt(estado[0]**2 + estado[1]**2)
                    
                    # Detener si está muy lejos o muy cerca del equilibrio
                    if distancia > max_distance or distancia < min_distance:
                        break
                    
                    puntos.append(estado.copy())
                    
                    # Integrar un paso
                    try:
                        derivada = self.sistema_actual.sistema_ecuaciones(estado, t_actual)
                        estado = [estado[0] + dt * derivada[0], 
                                 estado[1] + dt * derivada[1]]
                        t_actual += dt
                    except:
                        break
                
                return np.array(puntos) if puntos else np.array([condicion_inicial])
            
            # Trayectoria hacia adelante
            solucion_forward = trayectoria_limitada(10, direccion=1)
            
            # Trayectoria hacia atrás
            solucion_backward = trayectoria_limitada(10, direccion=-1)
            
            # Dibujar ambas trayectorias con el mismo estilo
            if len(solucion_forward) > 1:
                self.ax.plot(solucion_forward[:, 0], solucion_forward[:, 1], 
                           'b-', linewidth=2, alpha=0.8)
            
            if len(solucion_backward) > 1:
                self.ax.plot(solucion_backward[:, 0], solucion_backward[:, 1], 
                           'b-', linewidth=2, alpha=0.8)
            
            # Marcar el punto inicial
            self.ax.plot(x_click, y_click, 'ro', markersize=8, 
                        markeredgecolor='darkred', markeredgewidth=2)
            
            self.canvas.draw()
        except Exception as e:
            print(f"Error al crear trayectoria desde clic: {e}")
    
    def limpiar_trayectorias(self):
        """Limpia las trayectorias agregadas manualmente y redibuja el sistema"""
        if self.sistema_actual:
            self.sistema_actual.crear_grafica(self.ax)
            self.canvas.draw()
    
    def mostrar_resultados(self, sistema):
        """Muestra los resultados en el área de texto"""
        self.text_resultados.delete(1.0, tk.END)
        
        resultado = "═" * 50 + "\n"
        
        if sistema.funcion_personalizada:
            resultado += "   SISTEMA DINÁMICO PERSONALIZADO\n"
            resultado += "═" * 50 + "\n\n"
            
            resultado += "Funciones del sistema:\n"
            resultado += f"  dx₁/dt = {sistema.funcion_personalizada['f1']}\n"
            resultado += f"  dx₂/dt = {sistema.funcion_personalizada['f2']}\n\n"
            
            if sistema.es_no_lineal:
                resultado += "Tipo: Sistema NO LINEAL\n"
                resultado += "\nNOTA: Para sistemas no lineales, el análisis\n"
                resultado += "de estabilidad requiere linealización en los\n"
                resultado += "puntos de equilibrio.\n\n"
            else:
                resultado += "Tipo: Sistema Lineal\n\n"
            
            resultado += "Visualización: Gráfica de campo de direcciones\n"
            resultado += "y trayectorias desde diferentes puntos iniciales.\n"
            
        elif sistema.termino_forzado:
            resultado += "   SISTEMA DINÁMICO 2D NO HOMOGÉNEO\n"
            resultado += "═" * 50 + "\n\n"
            
            resultado += "Matriz del sistema A:\n"
            resultado += f"  ⎡ {sistema.A[0,0]:8.4f}  {sistema.A[0,1]:8.4f} ⎤\n"
            resultado += f"  ⎣ {sistema.A[1,0]:8.4f}  {sistema.A[1,1]:8.4f} ⎦\n\n"
            
            resultado += "─" * 50 + "\n\n"
            resultado += "Término Forzado f(t):\n"
            tf = sistema.termino_forzado
            tipo = tf['tipo']
            c1, c2 = tf['coef1'], tf['coef2']
            param = tf.get('param', 0)
            
            if tipo == 'constante':
                resultado += f"  f(t) = [{c1:.4f}, {c2:.4f}]ᵀ\n"
            elif tipo == 'exponencial':
                resultado += f"  f(t) = [{c1:.4f}e^({param:.4f}t), {c2:.4f}e^({param:.4f}t)]ᵀ\n"
            elif tipo == 'seno':
                resultado += f"  f(t) = [{c1:.4f}sin({param:.4f}t), {c2:.4f}sin({param:.4f}t)]ᵀ\n"
            elif tipo == 'coseno':
                resultado += f"  f(t) = [{c1:.4f}cos({param:.4f}t), {c2:.4f}cos({param:.4f}t)]ᵀ\n"
            
            resultado += "\n" + "─" * 50 + "\n\n"
            resultado += f"Determinante: {sistema.determinante:.6f}\n"
            resultado += f"Traza:        {sistema.traza:.6f}\n\n"
            
            resultado += "─" * 50 + "\n\n"
            resultado += "Autovalores:\n"
            for i, autoval in enumerate(sistema.autovalores, 1):
                if np.iscomplex(autoval):
                    resultado += f"  λ{i} = {autoval.real:.6f} + {autoval.imag:.6f}i\n"
                else:
                    resultado += f"  λ{i} = {autoval.real:.6f}\n"
            
            resultado += "\n" + "═" * 50 + "\n\n"
            tipo, estabilidad = sistema.clasificar_punto_equilibrio()
            resultado += "CLASIFICACIÓN (parte homogénea):\n"
            resultado += f"  Tipo:        {tipo}\n"
            resultado += f"  Estabilidad: {estabilidad}\n\n"
            resultado += "NOTA: El término forzado añade comportamiento\n"
            resultado += "no homogéneo a la solución particular.\n"
            
        else:
            resultado += "   ANÁLISIS DEL SISTEMA DINÁMICO 2D\n"
            resultado += "═" * 50 + "\n\n"
            
            resultado += "Matriz del sistema A:\n"
            resultado += f"  ⎡ {sistema.A[0,0]:8.4f}  {sistema.A[0,1]:8.4f} ⎤\n"
            resultado += f"  ⎣ {sistema.A[1,0]:8.4f}  {sistema.A[1,1]:8.4f} ⎦\n\n"
            
            resultado += "─" * 50 + "\n\n"
            resultado += f"Determinante: {sistema.determinante:.6f}\n"
            resultado += f"Traza:        {sistema.traza:.6f}\n\n"
            
            resultado += "─" * 50 + "\n\n"
            resultado += "Autovalores:\n"
            for i, autoval in enumerate(sistema.autovalores, 1):
                if np.iscomplex(autoval):
                    resultado += f"  λ{i} = {autoval.real:.6f} + {autoval.imag:.6f}i\n"
                else:
                    resultado += f"  λ{i} = {autoval.real:.6f}\n"
            
            resultado += "\n" + "─" * 50 + "\n\n"
            resultado += "Autovectores:\n"
            for i in range(2):
                autovec = sistema.autovectores[:, i]
                if np.iscomplex(autovec[0]):
                    resultado += f"  v{i+1} = [{autovec[0].real:.4f} + {autovec[0].imag:.4f}i,\n"
                    resultado += f"        {autovec[1].real:.4f} + {autovec[1].imag:.4f}i]ᵀ\n"
                else:
                    resultado += f"  v{i+1} = [{autovec[0].real:.6f},\n"
                    resultado += f"        {autovec[1].real:.6f}]ᵀ\n"
            
            resultado += "\n" + "═" * 50 + "\n\n"
            tipo, estabilidad = sistema.clasificar_punto_equilibrio()
            resultado += "CLASIFICACIÓN:\n"
            resultado += f"  Tipo:        {tipo}\n"
            resultado += f"  Estabilidad: {estabilidad}\n"
        
        resultado += "\n" + "=" * 50 + "\n"
        
        self.text_resultados.insert(1.0, resultado)
        
        # Colorear según estabilidad si aplica
        if not sistema.es_no_lineal:
            tipo, estabilidad = sistema.clasificar_punto_equilibrio()
            if "Estable" in estabilidad and "Inestable" not in estabilidad:
                self.text_resultados.tag_config("clasificacion", foreground='#2E7D32')
            elif "Inestable" in estabilidad:
                self.text_resultados.tag_config("clasificacion", foreground='#C62828')
            else:
                self.text_resultados.tag_config("clasificacion", foreground='#F57C00')


def main():
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.mainloop()


if __name__ == "__main__":
    main()
