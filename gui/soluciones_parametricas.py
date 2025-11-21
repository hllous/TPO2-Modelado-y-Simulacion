"""
Interfaz para calcular y visualizar soluciones paramétricas x(t) e y(t)
de sistemas dinámicos lineales 2D
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ui.estilos import COLORES, FUENTES
from core.sistema import SistemaDinamico2D


class InterfazSolucionesParametricas:
    """Interfaz para soluciones paramétricas de sistemas lineales 2D"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz
        
        Parámetros:
        - root: contenedor padre (Frame o Tk)
        """
        self.root = root
        self.sistema_actual = None
        
        # Configurar root si es Tk
        if isinstance(self.root, tk.Tk):
            self.root.title("Soluciones Paramétricas x(t), y(t)")
            self.root.geometry("1200x800")
            self.root.configure(bg=COLORES['fondo'])
        
        self._inicializar_variables()
        self._crear_widgets()
    
    def _inicializar_variables(self):
        """Inicializa variables de la interfaz"""
        # Variables para funciones (con valores por defecto)
        self.f1_var = tk.StringVar(value="y")
        self.f2_var = tk.StringVar(value="-x")
        
        # Variable para resultado
        self.resultado_tipo = tk.StringVar(value="")
    
    def _crear_widgets(self):
        """Crea la estructura principal de widgets"""
        # Frame principal con scroll
        if isinstance(self.root, tk.Tk):
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
        else:
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Contenedor con scroll
        canvas = tk.Canvas(main_frame, bg=COLORES['fondo'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="10")
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def _on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # Scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Crear secciones
        self._crear_titulo(scrollable_frame)
        self._crear_entrada_funciones(scrollable_frame)
        self._crear_botones(scrollable_frame)
        self._crear_area_resultados(scrollable_frame)
    
    def _crear_titulo(self, parent):
        """Crea sección de título"""
        titulo_frame = ttk.Frame(parent, style='Card.TFrame', padding="20")
        titulo_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(titulo_frame, text="🧮 Soluciones Paramétricas x(t), y(t)",
                 style='Title.TLabel', font=FUENTES['titulo']).pack()
        ttk.Label(titulo_frame, 
                 text="Calcula las soluciones generales de sistemas lineales homogéneos 2D",
                 style='Subtitle.TLabel', font=FUENTES['normal']).pack(pady=(5, 0))
    
    def _crear_entrada_funciones(self, parent):
        """Crea entrada de funciones"""
        funciones_frame = ttk.LabelFrame(parent, text="� Funciones del Sistema", padding="15")
        funciones_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Descripción
        desc = ttk.Label(funciones_frame, 
                        text="Ingrese las funciones del sistema (deben ser lineales y homogéneas):",
                        font=FUENTES['normal'])
        desc.pack(anchor=tk.W, pady=(0, 10))
        
        # f1
        f1_frame = ttk.Frame(funciones_frame)
        f1_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(f1_frame, text="dx/dt = f₁(x,y) =", font=FUENTES['normal']).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Entry(f1_frame, textvariable=self.f1_var, width=40, font=FUENTES['normal']).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # f2
        f2_frame = ttk.Frame(funciones_frame)
        f2_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(f2_frame, text="dy/dt = f₂(x,y) =", font=FUENTES['normal']).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Entry(f2_frame, textvariable=self.f2_var, width=40, font=FUENTES['normal']).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Nota con ejemplos
        nota = ttk.Label(funciones_frame,
                        text="💡 Ejemplos válidos: 'y' , '-x' , '-2*x + 3*y' , 'x - y'\n"
                             "Por defecto: Centro con f₁ = y, f₂ = -x",
                        font=FUENTES['pequena'], foreground=COLORES['texto_secundario'])
        nota.pack(anchor=tk.W, pady=(5, 0))
    
    def _crear_botones(self, parent):
        """Crea botones de acción"""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(btn_frame, text="🔍 Calcular Soluciones Paramétricas",
                  command=self.calcular_soluciones,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="🔄 Limpiar",
                  command=self.limpiar).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="📋 Ejemplos",
                  command=self.mostrar_ejemplos).pack(side=tk.LEFT, padx=5)
    
    def _crear_area_resultados(self, parent):
        """Crea área para mostrar resultados"""
        self.resultados_frame = ttk.LabelFrame(parent, text="📊 Resultados", padding="15")
        self.resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje inicial
        msg = ttk.Label(self.resultados_frame,
                       text="Ingrese las funciones y haga clic en 'Calcular Soluciones Paramétricas'\n\n"
                            "💡 Por defecto hay un ejemplo de Centro cargado (f₁=y, f₂=-x)",
                       font=FUENTES['normal'], foreground=COLORES['texto_secundario'],
                       justify=tk.CENTER)
        msg.pack(expand=True, pady=50)
    
    def calcular_soluciones(self):
        """Calcula y muestra las soluciones paramétricas"""
        try:
            # Leer funciones
            f1 = self.f1_var.get().strip()
            f2 = self.f2_var.get().strip()
            
            if not f1 or not f2:
                messagebox.showerror("Error", "Por favor, ingrese ambas funciones")
                return
            
            # Crear sistema con funciones
            funcion_personalizada = {
                'f1': f1,
                'f2': f2,
                'es_lineal': True  # Para soluciones paramétricas, debe ser lineal
            }
            self.sistema_actual = SistemaDinamico2D(funcion_personalizada=funcion_personalizada)
            
            # Obtener soluciones paramétricas
            resultado = self.sistema_actual.obtener_soluciones_parametricas()
            
            if not resultado['es_valido']:
                messagebox.showwarning("Advertencia", resultado['mensaje'])
                return
            
            # Mostrar resultados
            self._mostrar_resultados(resultado)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en las funciones ingresadas:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular soluciones:\n{str(e)}")
    
    def _mostrar_resultados(self, resultado):
        """Muestra los resultados en la interfaz"""
        # Limpiar resultados anteriores
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        # Tipo de solución
        tipo_frame = ttk.Frame(self.resultados_frame, style='Card.TFrame', padding="15")
        tipo_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(tipo_frame, text="Tipo de Solución:",
                 font=FUENTES['normal_bold']).pack(anchor=tk.W)
        ttk.Label(tipo_frame, text=resultado['tipo'],
                 font=FUENTES['titulo_seccion'], 
                 foreground=COLORES['primario']).pack(anchor=tk.W, pady=(5, 0))
        
        # Autovalores y autovectores
        eigen_frame = ttk.Frame(self.resultados_frame, style='Card.TFrame', padding="15")
        eigen_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(eigen_frame, text="Autovalores y Autovectores:",
                 font=FUENTES['normal_bold']).pack(anchor=tk.W, pady=(0, 10))
        
        λ1, λ2 = resultado['autovalores']
        v1, v2 = resultado['autovectores']
        
        # Formatear autovalores
        λ1_str = self._formatear_numero_complejo(λ1)
        λ2_str = self._formatear_numero_complejo(λ2)
        v1_str = f"[{self._formatear_numero_complejo(v1[0])}, {self._formatear_numero_complejo(v1[1])}]"
        v2_str = f"[{self._formatear_numero_complejo(v2[0])}, {self._formatear_numero_complejo(v2[1])}]"
        
        eigen_text = f"λ₁ = {λ1_str},  v₁ = {v1_str}\nλ₂ = {λ2_str},  v₂ = {v2_str}"
        
        eigen_label = tk.Text(eigen_frame, height=2, wrap=tk.WORD, font=FUENTES['normal'],
                             bg=COLORES['fondo'], relief=tk.FLAT, borderwidth=0)
        eigen_label.pack(fill=tk.X)
        eigen_label.insert('1.0', eigen_text)
        eigen_label.config(state=tk.DISABLED, fg=COLORES['secundario'])
        
        # Soluciones paramétricas con renderizado LaTeX
        sol_frame = ttk.Frame(self.resultados_frame, style='Card.TFrame', padding="15")
        sol_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(sol_frame, text="Solución General del Sistema:",
                 font=FUENTES['titulo_seccion'], 
                 foreground=COLORES['primario']).pack(anchor=tk.W, pady=(0, 15))
        
        # Renderizar x(t) con LaTeX
        self._renderizar_ecuacion(sol_frame, "x(t) = ", resultado['latex']['x'], COLORES['exito'])
        
        # Renderizar y(t) con LaTeX
        self._renderizar_ecuacion(sol_frame, "y(t) = ", resultado['latex']['y'], COLORES['exito'])
        
        # Nota sobre constantes
        nota_frame = ttk.Frame(sol_frame, style='Card.TFrame', padding="10")
        nota_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(nota_frame, text="📝 Nota:",
                 font=FUENTES['normal_bold']).pack(anchor=tk.W)
        ttk.Label(nota_frame, 
                 text="• c₁ y c₂ son constantes arbitrarias determinadas por las condiciones iniciales\n"
                      "• Esta es la solución general del sistema lineal homogéneo\n"
                      "• Para una solución particular, necesita especificar x(0) e y(0)",
                 font=FUENTES['pequena'], justify=tk.LEFT).pack(anchor=tk.W, pady=(5, 0))
        
        # Botones de acción
        btn_frame = ttk.Frame(self.resultados_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="📋 Copiar LaTeX",
                  command=lambda: self._copiar_latex(resultado)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="💾 Copiar Expresiones",
                  command=lambda: self._copiar_expresiones(resultado)).pack(side=tk.LEFT, padx=5)
    
    def _renderizar_ecuacion(self, parent, label_text, latex_expr, color):
        """Renderiza una ecuación usando matplotlib con LaTeX"""
        ecuacion_frame = ttk.Frame(parent)
        ecuacion_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Label a la izquierda
        ttk.Label(ecuacion_frame, text=label_text, font=FUENTES['titulo_seccion'],
                 foreground=color).pack(side=tk.LEFT, padx=(0, 10), anchor=tk.N)
        
        # Canvas para la ecuación renderizada
        canvas_frame = ttk.Frame(ecuacion_frame, relief=tk.SOLID, borderwidth=1)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Crear figura de matplotlib
        fig = Figure(figsize=(8, 1), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Renderizar LaTeX
        try:
            # Agregar $ para modo matemático
            latex_formula = f"${latex_expr}$"
            ax.text(0.05, 0.5, latex_formula, fontsize=14, verticalalignment='center',
                   transform=ax.transAxes, color='black')
        except Exception as e:
            # Si falla el renderizado LaTeX, mostrar texto plano
            ax.text(0.05, 0.5, latex_expr, fontsize=12, verticalalignment='center',
                   transform=ax.transAxes, color='black', family='monospace')
        
        fig.tight_layout(pad=0.5)
        
        # Crear canvas de tkinter
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _formatear_numero_complejo(self, z):
        """Formatea un número complejo para visualización"""
        if abs(z.imag) < 1e-10:  # Es real
            return f"{z.real:.4f}"
        elif abs(z.real) < 1e-10:  # Es imaginario puro
            return f"{z.imag:.4f}i"
        else:  # Complejo
            signo = '+' if z.imag >= 0 else '-'
            return f"{z.real:.4f} {signo} {abs(z.imag):.4f}i"
    
    def _copiar_latex(self, resultado):
        """Copia las expresiones en formato LaTeX"""
        latex_text = f"x(t) = {resultado['latex']['x']}\n\ny(t) = {resultado['latex']['y']}"
        self.root.clipboard_clear()
        self.root.clipboard_append(latex_text)
        messagebox.showinfo("✓ Copiado", "Expresiones LaTeX copiadas al portapapeles")
    
    def _copiar_expresiones(self, resultado):
        """Copia las expresiones en texto plano"""
        texto = f"x(t) = {resultado['solucion_general']['x']}\n\ny(t) = {resultado['solucion_general']['y']}"
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        messagebox.showinfo("✓ Copiado", "Expresiones copiadas al portapapeles")
    
    def limpiar(self):
        """Limpia todos los campos"""
        # Restaurar valores por defecto
        self.f1_var.set("y")
        self.f2_var.set("-x")
        
        # Limpiar resultados
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        msg = ttk.Label(self.resultados_frame,
                       text="Ingrese las funciones y haga clic en 'Calcular Soluciones Paramétricas'",
                       font=FUENTES['normal'], foreground=COLORES['texto_secundario'])
        msg.pack(expand=True, pady=50)
    
    def mostrar_ejemplos(self):
        """Muestra ejemplos predefinidos"""
        ejemplos_window = tk.Toplevel(self.root)
        ejemplos_window.title("Ejemplos de Sistemas Lineales")
        ejemplos_window.geometry("650x600")
        ejemplos_window.configure(bg=COLORES['fondo'])
        
        # Frame principal con título
        main_frame = ttk.Frame(ejemplos_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="📚 Ejemplos de Sistemas Lineales Homogéneos",
                 font=FUENTES['titulo_seccion']).pack(pady=(0, 10))
        
        ttk.Label(main_frame, text="Haga clic en un ejemplo para cargarlo:",
                 font=FUENTES['pequena']).pack(anchor=tk.W, pady=(0, 15))
        
        # Crear canvas y scrollbar para los ejemplos
        canvas = tk.Canvas(main_frame, bg=COLORES['fondo'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Ejemplos de funciones lineales
        ejemplos_func = {
            '🎯 Centro (Ejemplo por defecto)': ('y', '-x'),
            '📉 Nodo Estable': ('-x', '-2*y'),
            '📈 Nodo Inestable': ('x', '2*y'),
            '⚡ Nodo Silla': ('x', '-y'),
            '🌀 Espiral Estable 1': ('-x + 2*y', '-2*x - y'),
            '🌪️ Espiral Inestable 1': ('x - 2*y', '2*x + y'),
            '🔄 Espiral Estable 2': ('-2*x + y', '-x - 2*y'),
            '💫 Sistema Acoplado 1': ('-x + y', '-2*x'),
            '✨ Sistema Acoplado 2': ('2*x + y', 'x + 2*y'),
            '🎨 Sistema Mixto': ('-x + 3*y', '-3*x - y')
        }
        
        for nombre, (f1, f2) in ejemplos_func.items():
            frame_ejemplo = ttk.Frame(scrollable_frame, style='Card.TFrame', padding="10")
            frame_ejemplo.pack(fill=tk.X, pady=5, padx=5)
            
            def cargar(func1=f1, func2=f2):
                self.f1_var.set(func1)
                self.f2_var.set(func2)
                ejemplos_window.destroy()
            
            ttk.Label(frame_ejemplo, text=nombre,
                     font=FUENTES['normal_bold']).pack(anchor=tk.W)
            ttk.Label(frame_ejemplo, text=f"f₁ = {f1},  f₂ = {f2}",
                     font=FUENTES['pequena'], 
                     foreground=COLORES['secundario']).pack(anchor=tk.W)
            
            btn = ttk.Button(frame_ejemplo, text="Cargar", command=cargar)
            btn.pack(anchor=tk.E, pady=(5, 0))
        
        # Habilitar scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Limpiar el binding cuando se cierre la ventana
        def _on_close():
            canvas.unbind_all("<MouseWheel>")
            ejemplos_window.destroy()
        
        ejemplos_window.protocol("WM_DELETE_WINDOW", _on_close)
