"""
Núcleo matemático del sistema dinámico 2D
Contiene la clase SistemaDinamico2D y su lógica de análisis
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve


class SistemaDinamico2D:
    """
    Representa un sistema dinámico 2D general
    Soporta: sistemas lineales, lineales no homogéneos y personalizados (no lineales)
    """
    
    def __init__(self, matriz=None, termino_forzado=None, funcion_personalizada=None):
        """
        Inicializa el sistema dinámico
        
        Parámetros:
        - matriz: matriz 2x2 para sistemas lineales (dx/dt = Ax)
        - termino_forzado: dict con {tipo, coef1, coef2, param}
        - funcion_personalizada: dict con {'f1': expr, 'f2': expr, 'es_lineal': bool}
        """
        self.funcion_personalizada = funcion_personalizada
        
        if funcion_personalizada:
            self.A = None
            self.es_no_lineal = not funcion_personalizada.get('es_lineal', False)
            self.autovalores = None
            self.autovectores = None
            self.determinante = None
            self.traza = None
        else:
            self.A = np.array(matriz, dtype=float)
            self.es_no_lineal = False
            self.autovalores, self.autovectores = np.linalg.eig(self.A)
            self.determinante = np.linalg.det(self.A)
            self.traza = np.trace(self.A)
        
        self.termino_forzado = termino_forzado
    
    def sistema_ecuaciones(self, X, t):
        """
        Calcula dx/dt = f(x, y, t)
        
        Parámetros:
        - X: vector [x1, x2]
        - t: tiempo
        
        Retorna: [dx1/dt, dx2/dt]
        """
        x1, x2 = X
        
        # Sistema personalizado con funciones
        if self.funcion_personalizada:
            return self._evaluar_funciones_personalizadas(x1, x2, t)
        
        # Sistema lineal: dx/dt = Ax + f(t)
        dXdt = np.dot(self.A, X)
        
        # Agregar término forzado si existe
        if self.termino_forzado:
            dXdt = self._agregar_termino_forzado(dXdt, t)
        
        return dXdt
    
    def _evaluar_funciones_personalizadas(self, x1, x2, t):
        """Evalúa funciones personalizadas de forma segura"""
        try:
            f1_expr = self.funcion_personalizada['f1']
            f2_expr = self.funcion_personalizada['f2']
            
            variables = {
                'x1': x1, 'x2': x2, 't': t,
                'x': x1, 'y': x2,
                'np': np,
                'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                'abs': np.abs, 'pi': np.pi, 'e': np.e
            }
            
            dx1dt = float(eval(f1_expr, {"__builtins__": {}}, variables))
            dx2dt = float(eval(f2_expr, {"__builtins__": {}}, variables))
            
            return np.array([dx1dt, dx2dt])
        except Exception as e:
            print(f"Error evaluando funciones: {e}")
            return np.array([0.0, 0.0])
    
    def _agregar_termino_forzado(self, dXdt, t):
        """Agrega término forzado a la derivada"""
        tipo = self.termino_forzado['tipo']
        c1 = self.termino_forzado['coef1']
        c2 = self.termino_forzado['coef2']
        param = self.termino_forzado.get('param', 0)
        
        if tipo == 'constante':
            dXdt[0] += c1
            dXdt[1] += c2
        elif tipo == 'exponencial':
            dXdt[0] += c1 * np.exp(param * t)
            dXdt[1] += c2 * np.exp(param * t)
        elif tipo == 'seno':
            dXdt[0] += c1 * np.sin(param * t)
            dXdt[1] += c2 * np.sin(param * t)
        elif tipo == 'coseno':
            dXdt[0] += c1 * np.cos(param * t)
            dXdt[1] += c2 * np.cos(param * t)
        
        return dXdt
    
    def clasificar_punto_equilibrio(self):
        """
        Clasifica el tipo de punto de equilibrio según autovalores
        
        Retorna: (tipo, estabilidad)
        """
        if self.es_no_lineal:
            return "Sistema No Lineal", "Análisis requiere linealización"
        
        if self.autovalores is None:
            return "N/A", "Sistema personalizado"
        
        lambda1, lambda2 = self.autovalores
        
        # Autovalores complejos
        if np.iscomplex(lambda1) or np.iscomplex(lambda2):
            return self._clasificar_complejos(lambda1)
        
        # Autovalores reales
        return self._clasificar_reales(lambda1, lambda2)
    
    def _clasificar_complejos(self, lambda1):
        """Clasifica cuando hay autovalores complejos"""
        parte_real = lambda1.real
        
        if abs(parte_real) < 1e-10:
            return "Centro", "Neutral (órbitas cerradas)"
        elif parte_real < 0:
            return "Espiral (Foco)", "Estable (atractor)"
        else:
            return "Espiral (Foco)", "Inestable (repulsor)"
    
    def _clasificar_reales(self, lambda1, lambda2):
        """Clasifica cuando hay autovalores reales"""
        # Autovalor cero
        if abs(lambda1) < 1e-10 or abs(lambda2) < 1e-10:
            return "Degenerado (autovalor cero)", "Caso especial"
        
        # Mismo signo
        if lambda1 * lambda2 > 0:
            if abs(lambda1 - lambda2) < 1e-10:
                estab = "Estable" if lambda1 < 0 else "Inestable"
                return "Nodo Estrella", estab
            else:
                estab = "Estable (atractor)" if lambda1 < 0 else "Inestable (repulsor)"
                return "Nodo Propio", estab
        
        # Signos opuestos
        return "Punto Silla", "Inestable (hiperbólico)"
    
    def encontrar_puntos_equilibrio(self, xlim=(-5, 5), ylim=(-5, 5), tolerancia=0.01):
        """
        Encuentra puntos de equilibrio del sistema
        
        Parámetros:
        - xlim, ylim: límites de búsqueda
        - tolerancia: tolerancia para detectar equilibrios
        
        Retorna: lista de tuplas (x, y)
        """
        puntos_equilibrio = []
        
        # Sistemas lineales homogéneos siempre tienen (0,0)
        if not self.termino_forzado and not self.funcion_personalizada:
            return [(0, 0)]
        
        # Búsqueda numérica para sistemas no homogéneos o personalizados
        puntos_prueba = self._generar_puntos_prueba(xlim, ylim)
        
        for x0, y0 in puntos_prueba:
            try:
                sol = fsolve(lambda X: self.sistema_ecuaciones(X, 0), [x0, y0])
                
                if xlim[0] <= sol[0] <= xlim[1] and ylim[0] <= sol[1] <= ylim[1]:
                    derivadas = self.sistema_ecuaciones(sol, 0)
                    
                    if abs(derivadas[0]) < tolerancia and abs(derivadas[1]) < tolerancia:
                        if self._es_punto_nuevo(sol, puntos_equilibrio, tolerancia):
                            puntos_equilibrio.append((sol[0], sol[1]))
            except:
                continue
        
        # Retornar (0,0) para sistemas lineales si no encontró nada
        if len(puntos_equilibrio) == 0 and not self.funcion_personalizada:
            puntos_equilibrio.append((0, 0))
        
        return puntos_equilibrio
    
    @staticmethod
    def _generar_puntos_prueba(xlim, ylim):
        """Genera puntos iniciales para búsqueda de equilibrios"""
        return [
            (0, 0),
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1),
            (2, 0), (-2, 0), (0, 2), (0, -2),
            (2, 2), (-2, -2), (2, -2), (-2, 2),
            (0.5, 0.5), (-0.5, -0.5), (1.5, 1.5), (-1.5, -1.5)
        ]
    
    @staticmethod
    def _es_punto_nuevo(sol, puntos_existentes, tolerancia):
        """Verifica si un punto es nuevo (no está duplicado)"""
        for px, py in puntos_existentes:
            if abs(sol[0] - px) < tolerancia and abs(sol[1] - py) < tolerancia:
                return False
        return True
