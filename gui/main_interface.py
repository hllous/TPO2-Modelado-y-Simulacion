"""
Interfaz principal de la aplicación
Punto de entrada visual con acceso a módulos
"""

import tkinter as tk
from tkinter import ttk
from ui.estilos import configurar_estilos_ttk, COLORES, FUENTES, ESPACIOS
from gui.interfaz import InterfazGrafica
from gui.bifurcacion import InterfazBifurcacion
from gui.sistema_1d import InterfazSistema1D
from gui.hamilton import InterfazHamilton
from gui.lotka_volterra import InterfazLotkaVolterra
from gui.modelo_infeccion import InterfazModeloInfeccion


class InterfazPrincipal:
    """Interfaz principal moderna con acceso a módulos"""
    
    # Definición de módulos - DRY
    MODULOS = {
        '2d': {
            'titulo': '📊 Sistemas 2D',
            'clase': InterfazGrafica,
            'descripcion': 'Análisis completo de sistemas dinámicos lineales y no lineales\ncon visualización de flujo de fase, campos de dirección y puntos de equilibrio.'
        },
        '1d': {
            'titulo': '📈 Sistemas 1D',
            'clase': InterfazSistema1D,
            'descripcion': 'Análisis completo de sistemas dinámicos unidimensionales\nno lineales con campos de fase, trayectorias y equilibrios.'
        },
        'bifurcacion': {
            'titulo': '🔀 Bifurcaciones',
            'clase': InterfazBifurcacion,
            'descripcion': 'Análisis de bifurcaciones en sistemas dinámicos 1D\ncon diagramas de bifurcación y análisis de estabilidad.'
        },
        'infeccion': {
            'titulo': '🦠 Modelo Infección',
            'clase': InterfazModeloInfeccion,
            'descripcion': 'Simulación de propagación viral con modelo logístico\ndP/dt = K·P·(N-P). Evalúa infectados en días específicos.'
        },
        'hamilton': {
            'titulo': '⚡ Hamilton',
            'clase': InterfazHamilton,
            'descripcion': 'Análisis de sistemas Hamiltonianos y conservativos\nverifica si un sistema es conservativo paso a paso.'
        },
        'lotka_volterra': {
            'titulo': '🦅 Lotka-Volterra',
            'clase': InterfazLotkaVolterra,
            'descripcion': 'Análisis del sistema depredador-presa\ncon oscilaciones periódicas y análisis detallado de fases.'
        }
    }
    
    def __init__(self, root):
        """
        Inicializa la interfaz principal
        
        Parámetros:
        - root: ventana raíz de tkinter
        """
        self.root = root
        self.root.title("Sistemas Dinámicos - Aplicación Principal")
        self.root.geometry("1000x650")
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
            font=FUENTES['titulo_modulo'],
            justify=tk.CENTER
        )
        logo_label.pack(expand=True)
        
        # Separador
        separador = tk.Frame(sidebar, bg=COLORES['borde'], height=1)
        separador.pack(side=tk.TOP, fill=tk.X)
        
        # Contenedor de botones
        botones_frame = ttk.Frame(sidebar, padding=f"{ESPACIOS['md']}")
        botones_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=ESPACIOS['md'])
        
        # Crear botones dinámicamente
        self.botones_modulos = {}
        for key, config in self.MODULOS.items():
            btn = tk.Button(
                botones_frame,
                text=config['titulo'],
                bg=COLORES['primario'],
                fg='white',
                font=FUENTES['normal_bold'],
                padx=ESPACIOS['md'],
                pady=ESPACIOS['md'],
                relief=tk.FLAT,
                cursor='hand2',
                command=lambda k=key: self._abrir_modulo(k),
                activebackground=COLORES['primario_hover']
            )
            btn.pack(side=tk.TOP, fill=tk.X, pady=ESPACIOS['sm'])
            self.botones_modulos[key] = btn
        
        # Footer del sidebar
        footer = tk.Frame(sidebar, bg=COLORES['fondo'])
        footer.pack(side=tk.BOTTOM, fill=tk.X, padx=ESPACIOS['md'], pady=ESPACIOS['md'])
        
        info_text = tk.Label(
            footer,
            text="Selecciona un\nmódulo",
            bg=COLORES['fondo'],
            fg=COLORES['texto_secundario'],
            font=FUENTES['muy_pequena'],
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
        welcome_frame = ttk.Frame(self.content_frame, padding=f"{ESPACIOS['lg']}")
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        welcome_frame.columnconfigure(0, weight=1)
        welcome_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = tk.Label(
            welcome_frame,
            text="Bienvenido a Sistemas Dinámicos",
            font=FUENTES['titulo'],
            fg=COLORES['primario'],
            bg=COLORES['fondo']
        )
        titulo.grid(row=0, column=0, pady=(0, ESPACIOS['lg']))
        
        # Contenido central
        content = tk.Frame(welcome_frame, bg=COLORES['fondo'])
        content.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        
        # Mensaje principal
        mensaje = tk.Label(
            content,
            text="Selecciona un módulo desde la barra lateral\npara comenzar a explorar sistemas dinámicos",
            font=FUENTES['titulo_seccion'],
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo'],
            justify=tk.CENTER
        )
        mensaje.pack(expand=True)
        
        # Descripción de módulos disponibles
        descripcion_frame = ttk.Frame(welcome_frame, padding=f"{ESPACIOS['lg']}")
        descripcion_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=ESPACIOS['md'])
        
        descripcion_titulo = tk.Label(
            descripcion_frame,
            text="Módulos Disponibles:",
            font=FUENTES['titulo_seccion'],
            fg=COLORES['texto_principal'],
            bg=COLORES['fondo']
        )
        descripcion_titulo.pack(anchor=tk.W, pady=(0, ESPACIOS['md']))
        
        # Mostrar descripción de módulos
        for key, config in self.MODULOS.items():
            modulo_text = tk.Label(
                descripcion_frame,
                text=f"{config['titulo']} - {config['descripcion']}",
                font=FUENTES['pequena'],
                fg=COLORES['texto_secundario'],
                bg=COLORES['fondo'],
                justify=tk.LEFT,
                wraplength=450
            )
            modulo_text.pack(anchor=tk.W, pady=ESPACIOS['sm'])
    
    def _abrir_modulo(self, modulo_key):
        """Abre el módulo especificado"""
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Crear frame para el módulo
        modulo_frame = ttk.Frame(self.content_frame)
        modulo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Obtener configuración del módulo
        config = self.MODULOS[modulo_key]
        
        # Crear instancia del módulo
        self.modulo_activo = modulo_key
        modulo_instancia = config['clase'](modulo_frame)
        
        # Si tiene método crear_widgets, llamarlo
        if hasattr(modulo_instancia, 'crear_widgets'):
            modulo_instancia.crear_widgets()
    
    def volver_a_inicio(self):
        """Vuelve a la pantalla de inicio"""
        self.modulo_activo = None
        self._mostrar_bienvenida()

