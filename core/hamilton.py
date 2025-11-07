"""
Analizador de sistemas Hamiltonianos y conservativos
Determina si un sistema dinámico 2D es conservativo
Un sistema dx/dt=U, dy/dt=V es conservativo si ∂U/∂y + ∂V/∂x = 0 (divergencia nula)
"""

import sympy as sp
from typing import Dict, List, Tuple, Optional


class AnalizadorHamilton:
    """Analiza si un sistema es Hamiltoniano/conservativo"""
    
    def __init__(self, f1_str: str, f2_str: str):
        """
        Inicializa el analizador
        
        Args:
            f1_str: dx/dt = f1(x, y)
            f2_str: dy/dt = f2(x, y)
        """
        self.x = sp.Symbol('x', real=True)
        self.y = sp.Symbol('y', real=True)
        
        try:
            local_dict = {'x': self.x, 'y': self.y, 'sin': sp.sin, 'cos': sp.cos, 
                         'tan': sp.tan, 'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
                         'pi': sp.pi, 'e': sp.E}
            self.U = sp.sympify(f1_str, locals=local_dict)
            self.V = sp.sympify(f2_str, locals=local_dict)
        except Exception as e:
            raise ValueError(f"Error al parsear funciones: {e}")
        
        self.pasos = []
        self._calcular_derivadas()
    
    def _calcular_derivadas(self):
        """Calcula derivadas parciales necesarias"""
        self.dU_dy = sp.diff(self.U, self.y)
        self.dV_dx = sp.diff(self.V, self.x)
        self.divergencia = sp.simplify(self.dU_dy + self.dV_dx)
    
    def analizar(self) -> Dict:
        """
        Analiza si el sistema es conservativo
        
        Returns:
            Dict con análisis completo y pasos
        """
        self.pasos = []
        
        # Paso 1: Mostrar funciones
        self._agregar_paso(
            "Funciones del sistema",
            f"U(x,y) = dx/dt = {self.U}",
            f"V(x,y) = dy/dt = {self.V}"
        )
        
        # Paso 2: Calcular derivadas parciales
        self._agregar_paso(
            "Derivadas parciales",
            f"∂U/∂y = {self.dU_dy}",
            f"∂V/∂x = {self.dV_dx}"
        )
        
        # Paso 3: Calcular divergencia
        self._agregar_paso(
            "Divergencia del campo vectorial",
            f"∇·F = ∂U/∂y + ∂V/∂x = {self.divergencia}"
        )
        
        # Paso 4: Conclusión
        es_conservativo = self.divergencia == 0
        
        if es_conservativo:
            self._agregar_paso(
                "Conclusión",
                "✓ El sistema ES CONSERVATIVO",
                "La divergencia es nula: no hay pérdida/ganancia de energía",
                "Existe una función H(x,y) tal que las trayectorias siguen curvas de nivel de H"
            )
        else:
            self._agregar_paso(
                "Conclusión",
                "✗ El sistema NO es conservativo",
                f"La divergencia es {self.divergencia} ≠ 0",
                "El sistema disipa o genera energía"
            )
        
        # Paso 5: Propiedades adicionales
        self._analizar_propiedades_especiales(es_conservativo)
        
        return {
            'es_conservativo': es_conservativo,
            'divergencia': self.divergencia,
            'pasos': self.pasos,
            'U': self.U,
            'V': self.V,
            'dU_dy': self.dU_dy,
            'dV_dx': self.dV_dx
        }
    
    def _analizar_propiedades_especiales(self, es_conservativo: bool):
        """Analiza si hay propiedades especiales del sistema"""
        propiedades = []
        
        # Verificar si es Hamiltoniano (antisimétrico)
        es_hamiltoniano = self._verificar_hamiltoniano()
        if es_hamiltoniano:
            propiedades.append("Sistema es Hamiltoniano (forma J∇H)")
        
        # Verificar si es gradiente (gradiente descendente)
        es_gradiente = self._verificar_gradiente()
        if es_gradiente:
            propiedades.append("Sistema es gradiente (disipativo, converge a puntos fijos)")
        
        # Verificar reversibilidad
        es_reversible = self._verificar_reversibilidad()
        if es_reversible:
            propiedades.append("Sistema es reversible en el tiempo")
        
        if propiedades:
            self._agregar_paso(
                "Propiedades especiales",
                *propiedades
            )
    
    def _verificar_hamiltoniano(self) -> bool:
        """Verifica si el sistema tiene forma Hamiltoniana: ∂H/∂y = -U, ∂H/∂x = V"""
        # Para un sistema Hamiltoniano: V = ∂H/∂x, U = -∂H/∂y
        # Esto implica ∂V/∂x = ∂²H/∂x² y ∂U/∂y = -∂²H/∂y²
        # Que requiere ∂V/∂x = -∂U/∂y (antisimétrico)
        
        condition = sp.simplify(self.dV_dx + self.dU_dy)
        return condition == 0
    
    def _verificar_gradiente(self) -> bool:
        """Verifica si el sistema es gradiente (convergente)"""
        # Un sistema es gradiente si U = -∂V/∂x y V = -∂V/∂y para algún V
        # Equivalentemente: ∂U/∂y = ∂V/∂x (simétrico)
        
        dU_dx = sp.diff(self.U, self.x)
        dV_dy = sp.diff(self.V, self.y)
        
        condition1 = sp.simplify(self.dU_dy - self.dV_dx)
        return condition1 == 0 and sp.simplify(dU_dx + dV_dy) < 0  # Disipativo
    
    def _verificar_reversibilidad(self) -> bool:
        """Verifica si (x,y,t) -> (x,-y,-t) es una simetría"""
        # Cambiar y -> -y y ver si U se transforma adecuadamente
        U_reflejado = self.U.subs(self.y, -self.y)
        V_reflejado = self.V.subs(self.y, -self.y)
        
        # Para reversibilidad: U(-y) = U(y) y V(-y) = -V(y)
        return U_reflejado == self.U and V_reflejado == -self.V
    
    def encontrar_funcion_energetica(self) -> Optional[str]:
        """
        Intenta encontrar una función energética H si el sistema es conservativo
        Retorna una descripción de cómo encontrarla
        """
        if not self.divergencia == 0:
            return None
        
        # Para sistemas conservativos, H satisface:
        # ∂H/∂x = -V
        # ∂H/∂y = U
        
        try:
            H = sp.integrate(self.U, self.y)
            H_check = sp.diff(H, self.x)
            
            if H_check == self.V:
                return f"H(x,y) = {H}"
            
            H2 = sp.integrate(-self.V, self.x)
            return f"H(x,y) puede obtenerse integrando:\n∫U dy = {H} + f(x)\n∫-V dx = {H2} + g(y)"
        except:
            return "No se puede encontrar forma cerrada para H"
    
    def _agregar_paso(self, titulo: str, *contenido: str):
        """Agrega un paso al análisis"""
        self.pasos.append({
            'titulo': titulo,
            'contenido': list(contenido)
        })


def verificar_conservativo(f1: str, f2: str) -> Dict:
    """Función conveniente para análisis rápido"""
    analizador = AnalizadorHamilton(f1, f2)
    return analizador.analizar()
