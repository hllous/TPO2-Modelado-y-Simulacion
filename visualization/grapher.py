"""
Módulo para crear gráficas del sistema dinámico
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class Grapher:
    """Encargada de crear las visualizaciones del sistema"""
    
    def __init__(self, sistema):
        """
        Inicializa el graficador
        
        Parámetros:
        - sistema: instancia de SistemaDinamico2D
        """
        self.sistema = sistema
    
    def crear_grafica(self, ax, xlim=(-3, 3), ylim=(-3, 3), n_puntos=20):
        """
        Crea gráfica completa con campo de direcciones, autovectores y puntos de equilibrio
        
        Parámetros:
        - ax: eje de matplotlib
        - xlim, ylim: límites de visualización
        - n_puntos: resolución del campo de direcciones
        """
        ax.clear()
        
        # Calcular y dibujar campo de direcciones
        self._dibujar_campo_direcciones(ax, xlim, ylim, n_puntos)
        
        # Dibujar autovectores si aplica
        self._dibujar_autovectores(ax)
        
        # Marcar puntos de equilibrio
        self._marcar_puntos_equilibrio(ax, xlim, ylim)
        
        # Configurar apariencia
        self._configurar_ejes(ax, xlim, ylim)
        
        # Agregar título
        self._agregar_titulo(ax)
    
    def _dibujar_campo_direcciones(self, ax, xlim, ylim, n_puntos):
        """Dibuja el campo de direcciones (quiver plot)"""
        x = np.linspace(xlim[0], xlim[1], n_puntos)
        y = np.linspace(ylim[0], ylim[1], n_puntos)
        X, Y = np.meshgrid(x, y)
        
        # Calcular derivadas
        if self.sistema.funcion_personalizada:
            U, V = self._calcular_derivadas_personalizadas(X, Y)
        else:
            U, V = self._calcular_derivadas_lineales(X, Y)
        
        # Normalizar
        M = np.sqrt(U**2 + V**2)
        M[M == 0] = 1
        U_norm = U / M
        V_norm = V / M
        
        # Dibujar
        ax.quiver(X, Y, U_norm, V_norm, M, cmap='viridis', alpha=0.6)
    
    def _calcular_derivadas_personalizadas(self, X, Y):
        """Calcula derivadas para sistemas personalizados"""
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                derivadas = self.sistema.sistema_ecuaciones([X[i,j], Y[i,j]], 0)
                U[i,j] = derivadas[0]
                V[i,j] = derivadas[1]
        
        return U, V
    
    def _calcular_derivadas_lineales(self, X, Y):
        """Calcula derivadas para sistemas lineales"""
        U = self.sistema.A[0, 0] * X + self.sistema.A[0, 1] * Y
        V = self.sistema.A[1, 0] * X + self.sistema.A[1, 1] * Y
        return U, V
    
    def _dibujar_autovectores(self, ax):
        """Dibuja autovectores si el sistema los tiene"""
        tiene_autovalores = (
            not self.sistema.funcion_personalizada and 
            self.sistema.autovalores is not None and 
            not self.sistema.termino_forzado
        )
        
        if not tiene_autovalores or np.iscomplex(self.sistema.autovalores[0]):
            return
        
        for i in range(2):
            v = self.sistema.autovectores[:, i].real
            if abs(self.sistema.autovalores[i]) > 1e-10:
                scale = 2.5
                # Dibujar autovector desde origen
                ax.arrow(0, 0, scale * v[0], scale * v[1], 
                        head_width=0.2, head_length=0.15, 
                        fc='red', ec='red', linewidth=2, alpha=0.8)
                ax.arrow(0, 0, -scale * v[0], -scale * v[1], 
                        head_width=0.2, head_length=0.15, 
                        fc='red', ec='red', linewidth=2, alpha=0.8)
    
    def _marcar_puntos_equilibrio(self, ax, xlim, ylim):
        """Marca los puntos de equilibrio en la gráfica"""
        puntos_eq = self.sistema.encontrar_puntos_equilibrio(xlim, ylim)
        
        if puntos_eq:
            for i, (px, py) in enumerate(puntos_eq):
                kwargs = {'markersize': 12, 'markeredgecolor': 'white', 
                         'markeredgewidth': 2, 'zorder': 5}
                if i == 0:
                    kwargs['label'] = 'Punto de equilibrio'
                ax.plot(px, py, 'ko', **kwargs)
    
    def _configurar_ejes(self, ax, xlim, ylim):
        """Configura la apariencia de los ejes"""
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        
        # Etiquetas
        if self.sistema.funcion_personalizada:
            ax.set_xlabel('x', fontsize=11)
            ax.set_ylabel('y', fontsize=11)
        else:
            ax.set_xlabel('x₁', fontsize=11)
            ax.set_ylabel('x₂', fontsize=11)
    
    def _agregar_titulo(self, ax):
        """Agrega título descriptivo a la gráfica"""
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
