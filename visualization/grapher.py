"""
Módulo para crear gráficas del sistema dinámico
Simplificado con utilidades DRY
"""

import numpy as np
from visualization.math_utils import (
    calcular_campo_vectorial, normalizar_vectores, 
    encontrar_limites_automaticos
)


class Grapher:
    """Encargada de crear las visualizaciones del sistema"""
    
    DEFAULT_XLIM = (-5, 5)
    DEFAULT_YLIM = (-5, 5)
    
    def __init__(self, sistema):
        """Inicializa el graficador"""
        self.sistema = sistema
        self.xlim = self.DEFAULT_XLIM
        self.ylim = self.DEFAULT_YLIM
    
    def establecer_limites(self, xlim=None, ylim=None):
        """Establece los límites de la visualización"""
        if xlim:
            self.xlim = xlim
        if ylim:
            self.ylim = ylim
    
    def crear_grafica(self, ax, xlim=None, ylim=None, n_puntos=20):
        """Crea gráfica completa con visualización del sistema"""
        ax.clear()
        
        xlim = xlim or self.xlim
        ylim = ylim or self.ylim
        
        # Calcular límites automáticos si están en valores por defecto
        if xlim == self.DEFAULT_XLIM and ylim == self.DEFAULT_YLIM:
            xlim, ylim = encontrar_limites_automaticos(self.sistema)
        
        self._dibujar_campo_direcciones(ax, xlim, ylim, n_puntos)
        self._dibujar_autovectores(ax)
        self._marcar_puntos_equilibrio(ax, xlim, ylim)
        self._configurar_ejes(ax, xlim, ylim)
        self._agregar_titulo(ax)
    
    def _dibujar_campo_direcciones(self, ax, xlim, ylim, n_puntos):
        """Dibuja el campo de direcciones"""
        x = np.linspace(xlim[0], xlim[1], n_puntos)
        y = np.linspace(ylim[0], ylim[1], n_puntos)
        X, Y = np.meshgrid(x, y)
        
        U, V = calcular_campo_vectorial(self.sistema, X, Y)
        U_norm, V_norm, M = normalizar_vectores(U, V)
        
        ax.quiver(X, Y, U_norm, V_norm, M, cmap='viridis', alpha=0.6)
    
    def _dibujar_autovectores(self, ax):
        """Dibuja autovectores si aplican"""
        si_dibujar = (
            not self.sistema.funcion_personalizada and 
            self.sistema.autovalores is not None and 
            not self.sistema.termino_forzado and
            not np.iscomplex(self.sistema.autovalores[0])
        )
        
        if not si_dibujar:
            return
        
        for i in range(2):
            v = self.sistema.autovectores[:, i].real
            if abs(self.sistema.autovalores[i]) > 1e-10:
                scale = 2.5
                ax.arrow(0, 0, scale*v[0], scale*v[1], 
                        head_width=0.2, head_length=0.15, 
                        fc='red', ec='red', linewidth=2, alpha=0.8)
                ax.arrow(0, 0, -scale*v[0], -scale*v[1], 
                        head_width=0.2, head_length=0.15, 
                        fc='red', ec='red', linewidth=2, alpha=0.8)
    
    def _marcar_puntos_equilibrio(self, ax, xlim, ylim):
        """Marca puntos de equilibrio"""
        puntos_eq = self.sistema.encontrar_puntos_equilibrio(xlim, ylim)
        
        if puntos_eq:
            for i, (px, py) in enumerate(puntos_eq):
                kwargs = {
                    'markersize': 12, 'markeredgecolor': 'white',
                    'markeredgewidth': 2, 'zorder': 5
                }
                if i == 0:
                    kwargs['label'] = 'Punto de equilibrio'
                ax.plot(px, py, 'ko', **kwargs)
    
    def _configurar_ejes(self, ax, xlim, ylim):
        """Configura apariencia de los ejes"""
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        
        if self.sistema.funcion_personalizada:
            ax.set_xlabel('x', fontsize=11)
            ax.set_ylabel('y', fontsize=11)
        else:
            ax.set_xlabel('x₁', fontsize=11)
            ax.set_ylabel('x₂', fontsize=11)
    
    def _agregar_titulo(self, ax):
        """Agrega título descriptivo"""
        if self.sistema.termino_forzado:
            titulo = 'Sistema No Homogéneo: dx/dt = Ax + f(t)\n'
            tipo, estab = self.sistema.clasificar_punto_equilibrio()
            titulo += f'Parte homogénea: {tipo} ({estab})'
        elif self.sistema.funcion_personalizada:
            titulo = 'Sistema Personalizado\n'
            titulo += 'No Lineal' if self.sistema.es_no_lineal else 'Lineal'
        else:
            tipo, estab = self.sistema.clasificar_punto_equilibrio()
            titulo = f'Sistema Dinámico 2D: {tipo}\n{estab}'
        
        ax.set_title(titulo, fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
