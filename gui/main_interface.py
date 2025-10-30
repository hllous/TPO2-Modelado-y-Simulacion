"""
Interfaz principal de la aplicación
Punto de entrada visual con acceso a módulos
"""

import tkinter as tk
from tkinter import ttk
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES
from gui.interfaz import InterfazGrafica
from gui.bifurcacion import InterfazBifurcacion
from gui.sistema_1d import InterfazSistema1D


class InterfazPrincipal:
    """Interfaz principal moderna con acceso a módulos"""
    
    def __init__(self, root):
        """
        Inicializa la interfaz principal
        
        Parámetros:
        - root: ventana raíz de tkinter
        """
        self.root = root
        self.root.title("Sistemas Dinámicos - Aplicación Principal")
        self.root.geometry("900x600")
        self.root.configure(bg=COLORES['fondo'])
        
        # Configurar estilos
        configurar_estilos_ttk()
        
        # Variables de estado
        self.modulo_activo = None
        
        # Crear estructura de contenedores
        self._crear_layout()
    
    def _crear_layout(self):
        """Crea la estructura principal de la interfaz"""
        # Contenedor principal
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Crear sidebar y contenido
        self._crear_sidebar(main_container)
        self._crear_contenido(main_container)
    
    def _crear_sidebar(self, parent):
        """Crea barra lateral con opciones de módulos"""
        sidebar = ttk.Frame(parent, relief=tk.FLAT, padding="0")
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        
        # Header del sidebar
        header = tk.Frame(sidebar, bg=COLORES['primario'], height=80)
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)
        
        logo_label = tk.Label(
            header,
            text="Sistemas\nDinámicos",
            bg=COLORES['primario'],
            fg='white',
            font=FUENTES['titulo'],
            justify=tk.CENTER
        )
        logo_label.pack(expand=True)
        
        # Separador
        separador = tk.Frame(sidebar, bg='#e0e0e0', height=1)
        separador.pack(side=tk.TOP, fill=tk.X)
        
        # Contenedor de botones
        botones_frame = ttk.Frame(sidebar, padding="10")
        botones_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=10)
        
        # Botones de módulos
        self.botones_modulos = {}
        
        # Botón módulo 2D
        btn_2d = tk.Button(
            botones_frame,
            text="📊 Sistemas 2D",
            bg=COLORES['primario'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=15,
            relief=tk.FLAT,
            cursor='hand2',
            command=self.abrir_modulo_2d,
            activebackground=COLORES['primario_hover']
        )
        btn_2d.pack(side=tk.TOP, fill=tk.X, pady=8)
        self.botones_modulos['2d'] = btn_2d
        

        
        # Botón módulo 1D
        btn_1d = tk.Button(
            botones_frame,
            text="📈 Sistemas 1D",
            bg=COLORES['primario'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=15,
            relief=tk.FLAT,
            cursor='hand2',
            command=self.abrir_modulo_1d,
            activebackground=COLORES['primario_hover']
        )
        btn_1d.pack(side=tk.TOP, fill=tk.X, pady=8)
        self.botones_modulos['1d'] = btn_1d
        
        # Botón módulo bifurcación
        btn_bifurcacion = tk.Button(
            botones_frame,
            text="🔀 Bifurcaciones",
            bg=COLORES['primario'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=15,
            relief=tk.FLAT,
            cursor='hand2',
            command=self.abrir_modulo_bifurcacion,
            activebackground=COLORES['primario_hover']
        )
        btn_bifurcacion.pack(side=tk.TOP, fill=tk.X, pady=8)
        self.botones_modulos['bifurcacion'] = btn_bifurcacion
        
        # Footer del sidebar
        footer = tk.Frame(sidebar, bg=COLORES['fondo'])
        footer.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        info_text = tk.Label(
            footer,
            text="Haz clic en un módulo\npara comenzar",
            bg=COLORES['fondo'],
            fg=COLORES['texto_secundario'],
            font=('Arial', 8),
            justify=tk.CENTER
        )
        info_text.pack()
    
    def _crear_contenido(self, parent):
        """Crea área de contenido principal"""
        self.content_frame = ttk.Frame(parent)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Mostrar pantalla de bienvenida inicial
        self._mostrar_bienvenida()
    
    def _mostrar_bienvenida(self):
        """Muestra pantalla de bienvenida"""
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Frame principal de bienvenida
        welcome_frame = ttk.Frame(self.content_frame, padding="40")
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        welcome_frame.columnconfigure(0, weight=1)
        welcome_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = tk.Label(
            welcome_frame,
            text="Bienvenido a Sistemas Dinámicos",
            font=FUENTES['titulo'],
            fg=COLORES['texto_principal'],
            bg=COLORES['fondo']
        )
        titulo.grid(row=0, column=0, pady=(0, 20))
        
        # Contenido central
        content = tk.Frame(welcome_frame, bg=COLORES['fondo'])
        content.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        
        # Mensaje principal
        mensaje = tk.Label(
            content,
            text="Selecciona un módulo desde la barra lateral\npara comenzar a explorar sistemas dinámicos",
            font=('Arial', 14),
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo'],
            justify=tk.CENTER
        )
        mensaje.pack(expand=True)
        
        # Descripción de módulos disponibles
        descripcion_frame = ttk.Frame(welcome_frame, padding="20")
        descripcion_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=20)
        
        descripcion_titulo = tk.Label(
            descripcion_frame,
            text="Módulos Disponibles:",
            font=('Arial', 12, 'bold'),
            fg=COLORES['texto_principal'],
            bg=COLORES['fondo']
        )
        descripcion_titulo.pack(anchor=tk.W, pady=(0, 10))
        
        # Información de módulo 2D
        modulo_2d_text = tk.Label(
            descripcion_frame,
            text="📊 Sistemas 2D - Análisis completo de sistemas dinámicos lineales y no lineales\ncon visualización de flujo de fase, campos de dirección y puntos de equilibrio.",
            font=('Arial', 10),
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo'],
            justify=tk.LEFT,
            wraplength=400
        )
        modulo_2d_text.pack(anchor=tk.W, pady=5)
        
        # Información módulo 1D
        modulo_1d_text = tk.Label(
            descripcion_frame,
            text="📈 Sistemas 1D - Análisis completo de sistemas dinámicos unidimensionales\nno lineales con campos de fase, trayectorias y equilibrios.",
            font=('Arial', 10),
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo'],
            justify=tk.LEFT,
            wraplength=400
        )
        modulo_1d_text.pack(anchor=tk.W, pady=5)
        
        # Información bifurcación
        bifurcacion_text = tk.Label(
            descripcion_frame,
            text="🔀 Bifurcaciones - Análisis de bifurcaciones en sistemas dinámicos 1D\ncon diagramas de bifurcación y análisis de estabilidad.",
            font=('Arial', 10),
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo'],
            justify=tk.LEFT,
            wraplength=400
        )
        bifurcacion_text.pack(anchor=tk.W, pady=5)
    
    def abrir_modulo_2d(self):
        """Abre el módulo de sistemas 2D"""
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Crear frame para el módulo
        modulo_frame = ttk.Frame(self.content_frame)
        modulo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear módulo 2D pasando el frame como contenedor
        self.modulo_activo = 'sistemas_2d'
        interfaz_2d = InterfazGrafica(modulo_frame)
        interfaz_2d.crear_widgets()
    
    def abrir_modulo_bifurcacion(self):
        """Abre el módulo de bifurcaciones"""
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Crear frame para el módulo
        modulo_frame = ttk.Frame(self.content_frame)
        modulo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear módulo bifurcación pasando el frame como contenedor
        self.modulo_activo = 'bifurcacion'
        interfaz_bifurcacion = InterfazBifurcacion(modulo_frame)
    
    def abrir_modulo_1d(self):
        """Abre el módulo de sistemas 1D"""
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Crear frame para el módulo
        modulo_frame = ttk.Frame(self.content_frame)
        modulo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear módulo 1D pasando el frame como contenedor
        self.modulo_activo = 'sistemas_1d'
        interfaz_1d = InterfazSistema1D(modulo_frame)
    
    def volver_a_inicio(self):
        """Vuelve a la pantalla de inicio"""
        self.modulo_activo = None
        self._mostrar_bienvenida()
