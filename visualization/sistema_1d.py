"""
Visualización de sistemas no lineales 1D
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Tuple, Optional
from core.sistema_1d import SistemaDinamico1D


class VisualizadorSistema1D:
    """Visualiza sistemas dinámicos 1D"""
    
    def __init__(self, sistema: SistemaDinamico1D):
        """
        Inicializa el visualizador
        
        Parámetros:
        - sistema: instancia de SistemaDinamico1D
        """
        self.sistema = sistema
    
    def graficar_campo_fase(self, xlim: Tuple[float, float] = (-5, 5),
                           fig: Optional[Figure] = None) -> Figure:
        """Grafica el campo de fase y puntos de equilibrio"""
        if fig is None:
            fig = plt.figure(figsize=(10, 6))
        
        ax = fig.add_subplot(111)
        
        # Calcular función
        x_vals = np.linspace(xlim[0], xlim[1], 300)
        f_vals = self.sistema.evaluar_funcion(x_vals)
        
        # Graficar función
        ax.plot(x_vals, f_vals, 'b-', linewidth=2, label='dx/dt')
        ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.8, alpha=0.5)
        ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.8, alpha=0.5)
        
        # Encontrar y graficar equilibrios
        equilibrios = self.sistema.encontrar_equilibrios(xlim)
        
        for x_eq in equilibrios:
            estab = self.sistema.clasificar_estabilidad(x_eq)
            marker = 'o' if estab == 'estable' else 's'
            color = 'green' if estab == 'estable' else 'red'
            label = 'Estable' if x_eq == equilibrios[0] and estab == 'estable' else None
            ax.plot(x_eq, 0, marker=marker, markersize=10, color=color, 
                   label=label, markerfacecolor='white' if estab == 'inestable' else color,
                   markeredgewidth=2 if estab == 'inestable' else 0)
        
        # Flechas de dirección
        x_arrows = np.linspace(xlim[0], xlim[1], 20)
        for x_pos in x_arrows:
            f_val = float(self.sistema.evaluar_funcion(np.array([x_pos]))[0])
            if abs(f_val) > 0.01:
                arrow_dx = np.sign(f_val) * 0.3
                color = 'green' if f_val < 0 else 'red'
                ax.arrow(x_pos - arrow_dx/2, -max(abs(f_vals))*0.1, arrow_dx, 0,
                        head_width=max(abs(f_vals))*0.05, head_length=0.15,
                        fc=color, ec=color, alpha=0.6)
        
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('dx/dt', fontsize=12)
        ax.set_title('Campo de Fase', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(xlim)
        
        return fig
    
    def graficar_trayectoria(self, x0: float, t_span: Tuple[float, float] = (0, 10),
                            fig: Optional[Figure] = None) -> Figure:
        """Grafica una trayectoria temporal"""
        if fig is None:
            fig = plt.figure(figsize=(10, 5))
        
        ax = fig.add_subplot(111)
        
        t, x_traj = self.sistema.integrar_trayectoria(x0, t_span)
        
        ax.plot(t, x_traj, 'b-', linewidth=2, label=f'x(0) = {x0:.2f}')
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        
        # Marcar equilibrios
        equilibrios = self.sistema.encontrar_equilibrios()
        for x_eq in equilibrios:
            ax.axhline(y=x_eq, color='red', linestyle='--', alpha=0.3, linewidth=1)
        
        ax.set_xlabel('Tiempo (t)', fontsize=12)
        ax.set_ylabel('x(t)', fontsize=12)
        ax.set_title('Evolución Temporal', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def graficar_espacio_fase_tiempo(self, x0_values: list,
                                     t_span: Tuple[float, float] = (0, 10),
                                     fig: Optional[Figure] = None) -> Figure:
        """Grafica múltiples trayectorias en el espacio de fases vs tiempo"""
        if fig is None:
            fig = plt.figure(figsize=(12, 8))
        
        # Subplot 1: Campo de fase
        ax1 = fig.add_subplot(1, 2, 1)
        xlim = (-5, 5)
        x_vals = np.linspace(xlim[0], xlim[1], 300)
        f_vals = self.sistema.evaluar_funcion(x_vals)
        
        ax1.plot(x_vals, f_vals, 'b-', linewidth=2)
        ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
        
        equilibrios = self.sistema.encontrar_equilibrios(xlim)
        for x_eq in equilibrios:
            estab = self.sistema.clasificar_estabilidad(x_eq)
            color = 'green' if estab == 'estable' else 'red'
            ax1.plot(x_eq, 0, 'o', markersize=8, color=color)
        
        ax1.set_xlabel('x', fontsize=11)
        ax1.set_ylabel('dx/dt', fontsize=11)
        ax1.set_title('Campo de Fase', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Subplot 2: Trayectorias temporales
        ax2 = fig.add_subplot(1, 2, 2)
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(x0_values)))
        
        for i, x0 in enumerate(x0_values):
            t, x_traj = self.sistema.integrar_trayectoria(x0, t_span)
            ax2.plot(t, x_traj, linewidth=2, color=colors[i], 
                    label=f'x₀ = {x0:.2f}')
        
        for x_eq in equilibrios:
            ax2.axhline(y=x_eq, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        
        ax2.set_xlabel('Tiempo (t)', fontsize=11)
        ax2.set_ylabel('x(t)', fontsize=11)
        ax2.set_title('Trayectorias Temporales', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=9)
        
        fig.tight_layout()
        return fig
