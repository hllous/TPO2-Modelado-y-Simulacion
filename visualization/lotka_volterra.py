"""
Visualización del sistema Lotka-Volterra
"""

import numpy as np
from visualization.math_utils import normalizar_vectores


class GrapherLotkaVolterra:
    """Graficador especializado para Lotka-Volterra"""
    
    DEFAULT_XLIM = (0, 5)
    DEFAULT_YLIM = (0, 5)
    
    def __init__(self, sistema):
        """Inicializa el graficador"""
        self.sistema = sistema
        self.xlim = self.DEFAULT_XLIM
        self.ylim = self.DEFAULT_YLIM
    
    def crear_grafica(self, ax, xlim=None, ylim=None, n_puntos=15):
        """Crea gráfica completa del sistema"""
        ax.clear()
        
        xlim = xlim or self.xlim
        ylim = ylim or self.ylim
        
        self._dibujar_campo_vectorial(ax, xlim, ylim, n_puntos)
        self._marcar_equilibrios(ax, xlim, ylim)
        self._dibujar_isoclinas(ax, xlim, ylim)
        self._configurar_ejes(ax, xlim, ylim)
        self._agregar_titulo(ax)
    
    def _dibujar_campo_vectorial(self, ax, xlim, ylim, n_puntos):
        """Dibuja el campo de direcciones"""
        x = np.linspace(xlim[0], xlim[1], n_puntos)
        y = np.linspace(ylim[0], ylim[1], n_puntos)
        X, Y = np.meshgrid(x, y)
        
        U, V = self.sistema.campo_vectorial(X, Y)
        U_norm, V_norm, M = normalizar_vectores(U, V)
        
        ax.quiver(X, Y, U_norm, V_norm, M, cmap='plasma', alpha=0.6)
    
    def _marcar_equilibrios(self, ax, xlim, ylim):
        """Marca los puntos de equilibrio"""
        # Equilibrio trivial (extinción)
        if xlim[0] <= 0 <= xlim[1] and ylim[0] <= 0 <= ylim[1]:
            ax.plot(0, 0, 'rx', markersize=12, markeredgewidth=2, 
                   label='Extinción (0,0)', zorder=5)
        
        # Equilibrio interior
        eq = self.sistema.equilibrio_interior
        if xlim[0] <= eq[0] <= xlim[1] and ylim[0] <= eq[1] <= ylim[1]:
            ax.plot(eq[0], eq[1], 'ko', markersize=10, 
                   markeredgecolor='white', markeredgewidth=2,
                   label=f'Centro ({eq[0]:.2f}, {eq[1]:.2f})', zorder=5)
    
    def _dibujar_isoclinas(self, ax, xlim, ylim):
        """Dibuja las isoclinas (líneas nulas)"""
        y_iso_presa = self.sistema.alpha / self.sistema.beta
        if ylim[0] <= y_iso_presa <= ylim[1]:
            ax.axhline(y=y_iso_presa, color='blue', linestyle='--', 
                      alpha=0.5, linewidth=1.5, label='Isoclina presas')
        
        x_iso_depr = self.sistema.delta / self.sistema.gamma
        if xlim[0] <= x_iso_depr <= xlim[1]:
            ax.axvline(x=x_iso_depr, color='green', linestyle='--', 
                      alpha=0.5, linewidth=1.5, label='Isoclina depredadores')
    
    def _configurar_ejes(self, ax, xlim, ylim):
        """Configura los ejes"""
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_xlabel('Presas (x)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Depredadores (y)', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    def _agregar_titulo(self, ax):
        """Agrega título con parámetros"""
        titulo = 'Sistema Lotka-Volterra: Depredador-Presa\n'
        titulo += f'α={self.sistema.alpha:.2f}, β={self.sistema.beta:.3f}, '
        titulo += f'γ={self.sistema.gamma:.3f}, δ={self.sistema.delta:.2f}'
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9)
    
    def dibujar_trayectoria(self, ax, estado_inicial, t_final=100, color='red'):
        """Dibuja una trayectoria específica sobre la gráfica"""
        t, trayectoria = self.sistema.integrar_trayectoria(estado_inicial, t_final)
        
        x = trayectoria[:, 0]
        y = trayectoria[:, 1]
        
        ax.plot(x, y, color=color, alpha=0.7, linewidth=2, label='Trayectoria')
        ax.plot(x[0], y[0], 'go', markersize=10, markeredgecolor='white',
               markeredgewidth=2, label='Inicio', zorder=5)
        ax.plot(x[-1], y[-1], 'bo', markersize=10, markeredgecolor='white',
               markeredgewidth=2, label='Fin', zorder=5)
