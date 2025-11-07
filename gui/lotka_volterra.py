"""
Interfaz gráfica para Lotka-Volterra
Módulo especializado con análisis integrado
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from core.lotka_volterra import SistemaLotkaVolterra
from core.analizador_lv import AnalizadorLotkaVolterra
from core.sistema import SistemaDinamico2D
from visualization.lotka_volterra import GrapherLotkaVolterra
from input_module.lotka_volterra import InputLotkaVolterra
from ui.estilos import COLORES, FUENTES
from ui.widget_utils import PanelAnalisisBase, ConstructorUI


class InterfazLotkaVolterra:
    """Interfaz completa para Lotka-Volterra"""
    
    def __init__(self, root):
        """Inicializa la interfaz"""
        self.root = root
        if isinstance(root, tk.Tk):
            root.title("Lotka-Volterra: Sistema Depredador-Presa")
            root.geometry("1400x900")
            root.configure(bg=COLORES['fondo'])
        else:
            if isinstance(root, tk.Frame):
                root.configure(bg=COLORES['fondo'])
        
        self.sistema = None
        self.grapher = None
        self.analizador = None
        self._crear_layout()
    
    def _crear_layout(self):
        """Crea la estructura principal"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo: entrada y controles
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S), padx=(0, 5))
        
        # Panel derecho: gráficas
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Crear componentes
        self.input_panel = InputLotkaVolterra(left_frame)
        self._crear_botones_control(left_frame)
        self._crear_paneles_grafica(right_frame)
        
        # Sistema inicial
        self._actualizar_sistema()
    
    def _crear_botones_control(self, parent):
        """Crea botones de control"""
        frame = ttk.LabelFrame(parent, text="Controles", padding="10")
        frame.pack(fill=tk.X, padx=5, pady=10)
        
        ConstructorUI.crear_boton(
            frame,
            "📊 Actualizar Gráfica",
            self._actualizar_sistema
        ).pack(fill=tk.X, pady=5)
        
        ConstructorUI.crear_boton(
            frame,
            "🔍 Análisis Detallado",
            self._mostrar_analisis,
            bg='#2196F3'
        ).pack(fill=tk.X, pady=5)
        
        ConstructorUI.crear_boton(
            frame,
            "🔄 Valores Predeterminados",
            self._valores_predeterminados,
            bg='#FF9800'
        ).pack(fill=tk.X, pady=5)
    
    def _crear_paneles_grafica(self, parent):
        """Crea panel de gráficas"""
        # Panel superior: gráfica del campo
        titulo_campo = ttk.Label(parent, text="Plano de Fase", 
                                font=('Arial', 11, 'bold'))
        titulo_campo.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.fig_campo = Figure(figsize=(8, 5), dpi=100)
        self.ax_campo = self.fig_campo.add_subplot(111)
        self.canvas_campo = FigureCanvasTkAgg(self.fig_campo, parent)
        self.canvas_campo.get_tk_widget().grid(row=1, column=0, 
                                              sticky=(tk.W, tk.E, tk.N, tk.S))
        
        parent.rowconfigure(1, weight=1)
    
    def _actualizar_sistema(self):
        """Actualiza el sistema con parámetros actuales"""
        params = self.input_panel.obtener_parametros()
        
        if params.get('modo') == 'personalizado':
            # Modo personalizado con funciones
            try:
                from core.sistema import SistemaDinamico2D
                self.sistema = SistemaDinamico2D(
                    funcion_personalizada={
                        'f1': params['func_presa'],
                        'f2': params['func_depredador'],
                        'es_lineal': False
                    }
                )
            except Exception as e:
                # Fallback: usar Lotka-Volterra estándar
                print(f"Error en sistema personalizado: {e}")
                self.sistema = SistemaLotkaVolterra(
                    alpha=1.0, beta=0.1, gamma=0.1, delta=0.5
                )
        else:
            # Modo estándar
            self.sistema = SistemaLotkaVolterra(
                alpha=params.get('alpha', 1.0),
                beta=params.get('beta', 0.1),
                gamma=params.get('gamma', 0.1),
                delta=params.get('delta', 0.5)
            )
        
        self.grapher = GrapherLotkaVolterra(self.sistema)
        self.analizador = AnalizadorLotkaVolterra(self.sistema)
        
        self._dibujar_campo()
    
    def _dibujar_campo(self):
        """Dibuja el campo de fase"""
        if self.sistema is None:
            return
        
        self.grapher.crear_grafica(self.ax_campo, n_puntos=12)
        self.canvas_campo.draw()
    
    def _mostrar_analisis(self):
        """Muestra ventana de análisis detallado"""
        if self.sistema is None:
            return
        
        ventana, notebook = PanelAnalisisBase.crear_ventana_analisis(
            self.root,
            "Análisis Detallado: Lotka-Volterra"
        )
        
        analisis = self.analizador.analizar_completo()
        
        # Crear pestañas con análisis
        self._crear_tab_ecuaciones(notebook, analisis['ecuaciones'])
        self._crear_tab_equilibrios(notebook, analisis['equilibrios'])
        self._crear_tab_dinamica(notebook, analisis['dinamica'])
        self._crear_tab_oscilaciones(notebook, analisis['oscilaciones'])
        self._crear_tab_interpretacion(notebook, analisis['interpretacion'])
    
    def _crear_tab_ecuaciones(self, notebook, datos):
        """Crea pestaña de ecuaciones"""
        contenido = f"{datos['titulo']}\n{'='*50}\n\n"
        for eq in datos['ecuaciones']:
            contenido += f"{eq}\n"
        
        contenido += "\nTérminos:\n" + "-"*50 + "\n"
        for nombre, expr in datos['terminos'].items():
            contenido += f"\n{nombre.replace('_', ' ').title()}:\n  {expr}\n"
        
        PanelAnalisisBase.crear_pestaña_texto(notebook, "Ecuaciones", contenido)
    
    def _crear_tab_equilibrios(self, notebook, datos):
        """Crea pestaña de equilibrios"""
        contenido = f"{datos['titulo']}\n{'='*50}\n\n"
        
        eq_t = datos['equilibrio_trivial']
        contenido += f"1. EQUILIBRIO TRIVIAL\n{'-'*50}\n"
        contenido += f"Punto: {eq_t['punto']}\nDescripción: {eq_t['descripcion']}\n"
        contenido += f"Tipo: {eq_t['tipo']}\nSignificado: {eq_t['significado']}\n\n"
        
        eq_i = datos['equilibrio_interior']
        contenido += f"2. EQUILIBRIO INTERIOR (Coexistencia)\n{'-'*50}\n"
        contenido += f"Punto: ({eq_i['punto'][0]:.4f}, {eq_i['punto'][1]:.4f})\n"
        contenido += f"Presas en equilibrio: {eq_i['presas']}\n"
        contenido += f"Depredadores en equilibrio: {eq_i['depredadores']}\n"
        contenido += f"Tipo de equilibrio: {eq_i['tipo']}\n"
        contenido += f"Significado: {eq_i['significado']}\nCaracterística: {eq_i['caracteristica']}\n"
        
        PanelAnalisisBase.crear_pestaña_texto(notebook, "Equilibrios", contenido)
    
    def _crear_tab_dinamica(self, notebook, datos):
        """Crea pestaña de dinámica"""
        contenido = f"{datos['titulo']}\n{'='*50}\n\n"
        
        for etapa in datos['etapas']:
            contenido += f"\nFASE {etapa['fase']}: {etapa['nombre'].upper()}\n{'-'*50}\n"
            contenido += f"Descripción: {etapa['descripcion']}\nEcuación: {etapa['ecuacion']}\n"
            contenido += f"Duración: {etapa['duracion']}\nComportamiento: {etapa['comportamiento']}\n"
        
        PanelAnalisisBase.crear_pestaña_texto(notebook, "Dinámica", contenido)
    
    def _crear_tab_oscilaciones(self, notebook, datos):
        """Crea pestaña de oscilaciones"""
        contenido = f"{datos['titulo']}\n{'='*50}\n\n"
        contenido += f"PERÍODO APROXIMADO: {datos['periodo_aproximado']}\n"
        contenido += f"Fórmula: {datos['formula']}\n\n"
        contenido += "AMPLITUDES:\n"
        for especie, info in datos['amplitudes'].items():
            contenido += f"  {especie.title()}: {info}\n"
        
        contenido += f"\n\nOBSERVACIÓN IMPORTANTE:\n{'-'*50}\n"
        contenido += f"{datos['observacion']}\nDesfase típico: {datos['desfase']}\n"
        
        PanelAnalisisBase.crear_pestaña_texto(notebook, "Ciclo Periódico", contenido)
    
    def _crear_tab_interpretacion(self, notebook, datos):
        """Crea pestaña de interpretación ecológica"""
        contenido = f"{datos['titulo']}\n{'='*50}\n\n"
        
        cons = datos['conservacion']
        contenido += "CONSERVACIÓN DEL SISTEMA:\n" + "-"*50 + "\n"
        contenido += f"Propiedad: {cons['propiedad']}\nImplicación: {cons['implicacion']}\n"
        contenido += f"Significado: {cons['significado']}\n\n"
        
        contenido += "IMPLICACIONES BIOLÓGICAS:\n" + "-"*50 + "\n"
        for imp in datos['implicaciones_biologicas']:
            contenido += f"{imp}\n"
        
        contenido += "\n\nEFECTO DE CAMBIOS EN PARÁMETROS:\n" + "-"*50 + "\n"
        for pert in datos['perturbaciones']:
            contenido += f"{pert}\n"
        
        PanelAnalisisBase.crear_pestaña_texto(notebook, "Interpretación", contenido)
    
    def _valores_predeterminados(self):
        """Carga valores predeterminados"""
        self.input_panel.establecer_parametros({
            'alpha': 1.0,
            'beta': 0.1,
            'gamma': 0.1,
            'delta': 0.5
        })
        self._actualizar_sistema()
