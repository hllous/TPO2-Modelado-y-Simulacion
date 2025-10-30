"""
Visualización de bifurcaciones en sistemas dinámicos 1D
Genera diagramas de bifurcación y diagramas de fase
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, Tuple
from core.bifurcacion import AnalizadorBifurcacion


class VisualizadorBifurcacion:
    """Clase para visualizar diagramas de bifurcación y fase"""
    
    def __init__(self, analizador: AnalizadorBifurcacion):
        """
        Inicializa el visualizador
        
        Args:
            analizador: Instancia de AnalizadorBifurcacion
        """
        self.analizador = analizador
        
    def graficar_diagrama_bifurcacion(self, r_range: Tuple[float, float], 
                                       fig: Figure = None, num_points: int = 200) -> Figure:
        """
        Genera el diagrama de bifurcación
        
        Args:
            r_range: Rango de valores de r (r_min, r_max)
            fig: Figura de matplotlib (opcional)
            num_points: Número de puntos a evaluar
            
        Returns:
            Figura de matplotlib
        """
        if fig is None:
            fig = plt.figure(figsize=(10, 6))
        
        ax = fig.add_subplot(111)
        
        data = self.analizador.generar_datos_bifurcacion(r_range, num_points=num_points)
        
        has_data = False
        
        stable_branches = self._separar_ramas(data['estable']['r'], data['estable']['x'])
        unstable_branches = self._separar_ramas(data['inestable']['r'], data['inestable']['x'])
        
        for i, (r_branch, x_branch) in enumerate(stable_branches):
            if len(r_branch) > 0:
                label = 'Estable' if i == 0 else None
                ax.plot(r_branch, x_branch, 'b-', linewidth=2, label=label)
                has_data = True
        
        for i, (r_branch, x_branch) in enumerate(unstable_branches):
            if len(r_branch) > 0:
                label = 'Inestable' if i == 0 else None
                ax.plot(r_branch, x_branch, 'r--', linewidth=2, label=label)
                has_data = True
        
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
        ax.set_xlabel('Parámetro r', fontsize=12)
        ax.set_ylabel('x*', fontsize=12)
        ax.set_title('Diagrama de Bifurcación', fontsize=14, fontweight='bold')
        
        if has_data:
            ax.legend()
        else:
            ax.text(0.5, 0.5, 'No se encontraron puntos de equilibrio', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12, color='red')
        
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def _separar_ramas(self, r_data: np.ndarray, x_data: np.ndarray) -> list:
        """
        Separa los datos en ramas continuas para graficar correctamente
        
        Args:
            r_data: Array de valores de r
            x_data: Array de valores de x correspondientes
            
        Returns:
            Lista de tuplas (r_branch, x_branch) para cada rama continua
        """
        if len(r_data) == 0:
            return []
        
        from collections import defaultdict
        points_by_r = defaultdict(list)
        
        for r, x in zip(r_data, x_data):
            points_by_r[r].append(x)
        
        r_unique = sorted(points_by_r.keys())
        max_branches = max(len(points_by_r[r]) for r in r_unique)
        
        branches = [{'r': [], 'x': []} for _ in range(max_branches)]
        
        for r in r_unique:
            x_values = sorted(points_by_r[r])
            for i, x in enumerate(x_values):
                branches[i]['r'].append(r)
                branches[i]['x'].append(x)
        
        result = []
        for branch in branches:
            if len(branch['r']) > 0:
                result.append((np.array(branch['r']), np.array(branch['x'])))
        
        return result
    
    def graficar_diagrama_fase(self, r_values: list, x_range: Tuple[float, float],
                               fig: Figure = None) -> Figure:
        """
        Genera diagramas de fase para r < 0, r = 0, r > 0
        
        Args:
            r_values: Lista de tres valores de r [r_neg, r_zero, r_pos]
            x_range: Rango de valores de x (x_min, x_max)
            fig: Figura de matplotlib (opcional)
            
        Returns:
            Figura de matplotlib
        """
        if fig is None:
            fig = plt.figure(figsize=(15, 4))
        
        titles = ['r < 0', 'r = 0', 'r > 0']
        x_vals = np.linspace(x_range[0], x_range[1], 500)
        
        for i, (r_val, title) in enumerate(zip(r_values, titles)):
            ax = fig.add_subplot(1, 3, i + 1)
            
            f_vals = self.analizador.evaluar_funcion(x_vals, r_val)
            
            ax.plot(x_vals, f_vals, 'k-', linewidth=1.5, label='f(x)')
            ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.8)
            ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.8)
            
            eq_data = self.analizador.obtener_equilibrios_con_estabilidad(r_val)
            
            for eq in eq_data:
                x_eq = eq['x']
                if x_range[0] <= x_eq <= x_range[1]:
                    if eq['estabilidad'] == 'estable':
                        ax.plot(x_eq, 0, 'bo', markersize=10, 
                               markerfacecolor='blue', label='Estable' if i == 0 else '')
                    elif eq['estabilidad'] == 'inestable':
                        ax.plot(x_eq, 0, 'ro', markersize=10, 
                               markerfacecolor='white', markeredgewidth=2,
                               markeredgecolor='red', label='Inestable' if i == 0 else '')
            
            arrow_x = np.linspace(x_range[0], x_range[1], 15)
            for x_pos in arrow_x:
                f_val = float(self.analizador.evaluar_funcion(np.array([x_pos]), r_val)[0])
                arrow_size = 0.3 * np.sign(f_val) * min(abs(f_val), 1.0)
                
                if abs(f_val) > 0.01:
                    color = 'blue' if self._es_region_estable(x_pos, r_val) else 'red'
                    style = '-' if self._es_region_estable(x_pos, r_val) else '--'
                    
                    ax.arrow(x_pos, -0.5, arrow_size, 0, 
                            head_width=0.15, head_length=0.1,
                            fc=color, ec=color, linewidth=1.5,
                            linestyle=style, alpha=0.7)
            
            ax.set_xlabel('x', fontsize=11)
            ax.set_ylabel('f(x)', fontsize=11)
            ax.set_title(f'{title} (r = {r_val:.2f})', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_ylim([min(-1, np.min(f_vals)), max(1, np.max(f_vals))])
            
            if i == 0:
                ax.legend(loc='best', fontsize=9)
        
        fig.tight_layout()
        return fig
    
    def _es_region_estable(self, x_val: float, r_val: float) -> bool:
        """
        Determina si una región es estable (f'(x) < 0)
        
        Args:
            x_val: Valor de x
            r_val: Valor de r
            
        Returns:
            True si la región es estable
        """
        try:
            derivative = float(self.analizador.df_dx.subs([
                (self.analizador.x, x_val), 
                (self.analizador.r, r_val)
            ]))
            return derivative < 0
        except:
            return False
