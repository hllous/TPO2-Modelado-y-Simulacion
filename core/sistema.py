"""
Núcleo matemático del sistema dinámico 2D
Contiene la clase SistemaDinamico2D y su lógica de análisis
"""

import numpy as np
import sympy as sp
from scipy.integrate import odeint
from scipy.optimize import fsolve
from core.utils import normalizar_funciones, FUNCIONES_SYMPY, crear_diccionario_variables_evaluacion


class SistemaDinamico2D:
    """
    Representa un sistema dinámico 2D general
    Soporta: sistemas lineales, lineales no homogéneos y personalizados (no lineales)
    """
    
    def __init__(self, matriz=None, termino_forzado=None, funcion_personalizada=None, parametros=None):
        """
        Inicializa el sistema dinámico
        
        Parámetros:
        - matriz: matriz 2x2 para sistemas lineales (dx/dt = Ax)
        - termino_forzado: dict con {tipo, coef1, coef2, param}
        - funcion_personalizada: dict con {'f1': expr, 'f2': expr, 'es_lineal': bool}
        - parametros: dict con valores de parámetros adicionales (ej: {'u': 0.5, 'mu': 1.0})
        """
        self.funcion_personalizada = funcion_personalizada
        self.parametros = parametros or {}
        
        if funcion_personalizada:
            self.A = None
            self.es_no_lineal = not funcion_personalizada.get('es_lineal', False)
            self.autovalores = None
            self.autovectores = None
            self.determinante = None
            self.traza = None
            
            # Parsear funciones con sympy para análisis simbólico
            self._parsear_funciones_simbolicamnete()
        else:
            self.A = np.array(matriz, dtype=float)
            self.es_no_lineal = False
            self.autovalores, self.autovectores = np.linalg.eig(self.A)
            self.determinante = np.linalg.det(self.A)
            self.traza = np.trace(self.A)
            self.jacobiano_simbolico = None
        
        self.termino_forzado = termino_forzado
    
    def _parsear_funciones_simbolicamnete(self):
        """Parsea las funciones personalizadas con sympy y calcula el Jacobiano simbólico"""
        try:
            # Definir variables simbólicas
            self.x_sym = sp.Symbol('x', real=True)
            self.y_sym = sp.Symbol('y', real=True)
            
            # Normalizar y parsear las funciones
            f1_str = normalizar_funciones(self.funcion_personalizada['f1'])
            f2_str = normalizar_funciones(self.funcion_personalizada['f2'])
            
            # Crear diccionario de símbolos y funciones disponibles para sympify
            local_dict = {
                'x': self.x_sym, 
                'y': self.y_sym,
                **FUNCIONES_SYMPY
            }
            
            # Agregar símbolos para los parámetros
            self.param_symbols = {}
            for param_name in self.parametros.keys():
                self.param_symbols[param_name] = sp.Symbol(param_name, real=True)
                local_dict[param_name] = self.param_symbols[param_name]
            
            self.f1_sym = sp.sympify(f1_str, locals=local_dict)
            self.f2_sym = sp.sympify(f2_str, locals=local_dict)
            
            # Calcular derivadas parciales para el Jacobiano
            self.df1_dx = sp.diff(self.f1_sym, self.x_sym)
            self.df1_dy = sp.diff(self.f1_sym, self.y_sym)
            self.df2_dx = sp.diff(self.f2_sym, self.x_sym)
            self.df2_dy = sp.diff(self.f2_sym, self.y_sym)
            
            # Matriz Jacobiana simbólica
            self.jacobiano_simbolico = sp.Matrix([
                [self.df1_dx, self.df1_dy],
                [self.df2_dx, self.df2_dy]
            ])
            
        except Exception as e:
            print(f"Error al parsear funciones simbólicamente: {e}")
            self.f1_sym = None
            self.f2_sym = None
            self.jacobiano_simbolico = None
    
    def calcular_jacobiano_en_punto(self, x, y):
        """
        Calcula la matriz Jacobiana evaluada en un punto específico
        
        Parámetros:
        - x, y: coordenadas del punto
        
        Retorna: matriz Jacobiana 2x2 como numpy array
        """
        if not self.funcion_personalizada or self.jacobiano_simbolico is None:
            return None
        
        try:
            # Crear lista de sustituciones con coordenadas
            subs_list = [(self.x_sym, x), (self.y_sym, y)]
            
            # Agregar sustituciones para los parámetros
            for param_name, param_value in self.parametros.items():
                if param_name in self.param_symbols:
                    subs_list.append((self.param_symbols[param_name], param_value))
            
            # Evaluar el Jacobiano simbólico en el punto
            jacobiano_evaluado = self.jacobiano_simbolico.subs(subs_list)
            
            # Convertir a numpy array
            J = np.array(jacobiano_evaluado, dtype=float)
            return J
        except Exception as e:
            print(f"Error calculando Jacobiano en ({x}, {y}): {e}")
            return None
    
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
            # Normalizar y obtener expresiones
            f1_expr = normalizar_funciones(self.funcion_personalizada['f1'])
            f2_expr = normalizar_funciones(self.funcion_personalizada['f2'])
            
            # Crear diccionario de variables usando utilidad
            variables = crear_diccionario_variables_evaluacion(x1, x2, t, self.parametros)
            
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
    
    def clasificar_punto_equilibrio(self, punto_equilibrio=None):
        """
        Clasifica el tipo de punto de equilibrio según autovalores
        
        Parámetros:
        - punto_equilibrio: tupla (x, y) del punto a analizar. Si None, usa (0,0) o el primer equilibrio encontrado
        
        Retorna: (tipo, estabilidad)
        """
        if self.funcion_personalizada:
            # Para sistemas no lineales, analizar en el punto de equilibrio especificado
            if punto_equilibrio is None:
                # Buscar el punto de equilibrio (0,0) o el primero encontrado
                puntos_eq = self.encontrar_puntos_equilibrio()
                if puntos_eq:
                    punto_equilibrio = puntos_eq[0]  # Usar el primer punto encontrado
                else:
                    punto_equilibrio = (0, 0)  # Usar origen como fallback
            
            # Calcular Jacobiano en el punto
            J = self.calcular_jacobiano_en_punto(punto_equilibrio[0], punto_equilibrio[1])
            if J is None:
                return "Error en linealización", "No se pudo calcular el Jacobiano"
            
            # Calcular autovalores del Jacobiano
            try:
                autovalores, autovectores = np.linalg.eig(J)
                self.autovalores = autovalores
                self.autovectores = autovectores
                self.determinante = np.linalg.det(J)
                self.traza = np.trace(J)
            except:
                return "Error en cálculo", "No se pudieron calcular autovalores"
        
        if self.autovalores is None:
            return "N/A", "Sistema personalizado sin análisis"
        
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
