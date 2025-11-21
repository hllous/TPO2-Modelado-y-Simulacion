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
        """Agrega término forzado a la derivada (simplificado con KISS)"""
        tipo = self.termino_forzado['tipo']
        c1, c2 = self.termino_forzado['coef1'], self.termino_forzado['coef2']
        param = self.termino_forzado.get('param', 0)
        
        # Mapeo simplificado de términos forzados
        funciones_forzado = {
            'constante': lambda t: 1,
            'exponencial': lambda t: np.exp(param * t),
            'seno': lambda t: np.sin(param * t),
            'coseno': lambda t: np.cos(param * t)
        }
        
        factor = funciones_forzado.get(tipo, lambda t: 0)(t)
        dXdt[0] += c1 * factor
        dXdt[1] += c2 * factor
        
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
        
        # Intentar primero búsqueda simbólica para sistemas personalizados
        if self.funcion_personalizada and hasattr(self, 'f1_sym') and self.f1_sym is not None:
            try:
                # Resolver simbólicamente
                soluciones_simbolicas = sp.solve([self.f1_sym, self.f2_sym], 
                                                 [self.x_sym, self.y_sym], dict=True)
                
                for sol_dict in soluciones_simbolicas:
                    try:
                        # Sustituir parámetros
                        sol_subs = sol_dict
                        for param_name, param_value in self.parametros.items():
                            if param_name in self.param_symbols:
                                sol_subs = {k: v.subs(self.param_symbols[param_name], param_value) 
                                           for k, v in sol_subs.items()}
                        
                        # Convertir a float
                        x_val = complex(sol_subs[self.x_sym])
                        y_val = complex(sol_subs[self.y_sym])
                        
                        # Solo tomar soluciones reales
                        if abs(x_val.imag) < 1e-10 and abs(y_val.imag) < 1e-10:
                            x_float = float(x_val.real)
                            y_float = float(y_val.real)
                            
                            # Verificar que esté dentro de los límites
                            if xlim[0] <= x_float <= xlim[1] and ylim[0] <= y_float <= ylim[1]:
                                # Verificar que realmente sea equilibrio
                                derivadas = self.sistema_ecuaciones([x_float, y_float], 0)
                                if abs(derivadas[0]) < tolerancia and abs(derivadas[1]) < tolerancia:
                                    if self._es_punto_nuevo([x_float, y_float], puntos_equilibrio, tolerancia):
                                        puntos_equilibrio.append((x_float, y_float))
                    except (TypeError, ValueError, AttributeError):
                        continue
            except:
                pass  # Si falla búsqueda simbólica, usar numérica
        
        # Detectar y almacenar posibles ciclos límite antes de la búsqueda numérica
        self._detectar_ciclos_limite()
        
        # Detectar y almacenar posibles ciclos límite antes de la búsqueda numérica
        self._detectar_ciclos_limite()
        
        # Búsqueda numérica complementaria (encuentra puntos que la simbólica puede perder)
        # LIMITAR búsqueda si ya detectamos un ciclo límite
        max_puntos_numericos = 5 if hasattr(self, 'ciclo_limite') and self.ciclo_limite else 50
        puntos_prueba = self._generar_puntos_prueba(xlim, ylim, max_puntos=max_puntos_numericos)
        
        # Silenciar warnings de convergencia de fsolve
        import warnings
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=RuntimeWarning)
            
            for x0, y0 in puntos_prueba:
                try:
                    sol = fsolve(lambda X: self.sistema_ecuaciones(X, 0), [x0, y0], full_output=True)
                    x_sol = sol[0]
                    info = sol[1]
                    
                    # Verificar que la solución es válida (convergió)
                    if info['fvec'] is not None:
                        # Verificar que está dentro de límites
                        if xlim[0] <= x_sol[0] <= xlim[1] and ylim[0] <= x_sol[1] <= ylim[1]:
                            derivadas = self.sistema_ecuaciones(x_sol, 0)
                            
                            if abs(derivadas[0]) < tolerancia and abs(derivadas[1]) < tolerancia:
                                if self._es_punto_nuevo(x_sol, puntos_equilibrio, tolerancia):
                                    puntos_equilibrio.append((x_sol[0], x_sol[1]))
                except:
                    continue
        
        # Retornar (0,0) para sistemas lineales si no encontró nada
        if len(puntos_equilibrio) == 0 and not self.funcion_personalizada:
            puntos_equilibrio.append((0, 0))
        
        return puntos_equilibrio
    
    def _detectar_ciclos_limite(self):
        """
        Detecta ciclos límite analizando las soluciones simbólicas.
        Un ciclo límite típicamente aparece cuando las soluciones son paramétricas.
        """
        self.ciclo_limite = None
        
        if not self.funcion_personalizada or not hasattr(self, 'f1_sym') or self.f1_sym is None:
            return
        
        try:
            # Método directo: detectar factor común primero (más robusto)
            # Factorizar las ecuaciones
            f1_factorizado = sp.factor(self.f1_sym)
            f2_factorizado = sp.factor(self.f2_sym)
            
            # Buscar factores comunes (pueden indicar curva de equilibrios)
            f1_factors = self._obtener_factores(f1_factorizado)
            f2_factors = self._obtener_factores(f2_factorizado)
            
            # Convertir factores a strings para comparación
            f1_factors_str = [str(sp.simplify(f)) for f in f1_factors]
            f2_factors_str = [str(sp.simplify(f)) for f in f2_factors]
            
            factores_comunes = []
            for i, f1_str in enumerate(f1_factors_str):
                for j, f2_str in enumerate(f2_factors_str):
                    # Comparar factores (simplificados)
                    if f1_str == f2_str and len(f1_str) > 3:  # Evitar factores triviales como "x" o "-1"
                        factor_original = f1_factors[i]
                        if self.x_sym in factor_original.free_symbols and self.y_sym in factor_original.free_symbols:
                            factores_comunes.append(factor_original)
            
            # Analizar factores comunes
            for factor in factores_comunes:
                curva_info = self._analizar_factor_comun(factor)
                if curva_info:
                    self.ciclo_limite = curva_info
                    return
            
            # Método alternativo: resolver simbólicamente y buscar soluciones paramétricas
            soluciones = sp.solve([self.f1_sym, self.f2_sym], 
                                 [self.x_sym, self.y_sym], dict=True)
            
            # Buscar soluciones paramétricas
            for sol_dict in soluciones:
                x_sol = sol_dict.get(self.x_sym)
                y_sol = sol_dict.get(self.y_sym)
                
                if x_sol is None or y_sol is None:
                    continue
                
                # Verificar si alguna solución es paramétrica (contiene la variable libre)
                # Ejemplo: y = sqrt(1 - x**2) indica una curva
                if self.x_sym in y_sol.free_symbols or self.y_sym in x_sol.free_symbols:
                    # Intentar identificar el tipo de curva
                    curva_info = self._identificar_curva(x_sol, y_sol)
                    if curva_info:
                        self.ciclo_limite = curva_info
                        return
                    
        except Exception as e:
            pass  # No se pudo detectar ciclo límite
    
    def _obtener_factores(self, expr):
        """Extrae factores de una expresión factorizada"""
        if isinstance(expr, sp.Mul):
            return list(expr.args)
        else:
            return [expr]
    
    def _identificar_curva(self, x_expr, y_expr):
        """
        Intenta identificar el tipo de curva a partir de las expresiones paramétricas.
        Retorna dict con info de la curva o None.
        """
        try:
            # Caso: círculo -> y = ±sqrt(R² - x²)
            if isinstance(y_expr, sp.sqrt) or isinstance(y_expr, sp.Pow):
                # Extraer argumento del sqrt
                if isinstance(y_expr, sp.sqrt):
                    arg = y_expr.args[0]
                elif hasattr(y_expr, 'exp') and y_expr.exp == sp.Rational(1, 2):
                    arg = y_expr.args[0]
                else:
                    return None
                
                # Verificar si es de la forma R² - x²
                expanded = sp.expand(arg)
                
                # Buscar término con x²
                x_coef = expanded.coeff(self.x_sym**2)
                const = expanded.as_coeff_add(self.x_sym)[0]
                
                if x_coef is not None and x_coef == -1:
                    # Forma: R² - x² donde R² = const
                    R_cuadrado = const
                    if R_cuadrado > 0:
                        R = float(sp.sqrt(R_cuadrado))
                        return {
                            'tipo': 'circulo',
                            'centro': (0, 0),
                            'radio': R,
                            'ecuacion': f'x² + y² = {R_cuadrado}'
                        }
        except:
            pass
        
        return None
    
    def _analizar_factor_comun(self, factor):
        """
        Analiza un factor común para determinar si representa un ciclo límite.
        """
        try:
            # Reorganizar como ecuación = 0
            ecuacion = sp.expand(factor)
            
            # Detectar círculo: ax² + ay² + bx + cy + d = 0
            coef_x2 = ecuacion.coeff(self.x_sym**2)
            coef_y2 = ecuacion.coeff(self.y_sym**2)
            coef_x = ecuacion.coeff(self.x_sym, 1)  # Coef lineal de x
            coef_y = ecuacion.coeff(self.y_sym, 1)  # Coef lineal de y
            
            # Obtener término independiente (sin x ni y)
            termino_indep = ecuacion.subs([(self.x_sym, 0), (self.y_sym, 0)])
            
            if coef_x2 is not None and coef_y2 is not None and coef_x2 != 0:
                # Verificar si los coeficientes de x² e y² son iguales (círculo)
                ratio = sp.simplify(coef_y2 / coef_x2)
                
                if ratio == 1 or ratio == -1:  # Mismos coeficientes (en valor absoluto)
                    # Normalizar dividiendo por coef_x2
                    coef_x_norm = coef_x / coef_x2 if coef_x else 0
                    coef_y_norm = coef_y / coef_x2 if coef_y else 0
                    const_norm = termino_indep / coef_x2 if termino_indep else 0
                    
                    # Fórmula: x² + y² + ax + by + c = 0
                    # Centro: (-a/2, -b/2)
                    # Radio: sqrt((a/2)² + (b/2)² - c)
                    
                    a = float(coef_x_norm) if coef_x_norm else 0
                    b = float(coef_y_norm) if coef_y_norm else 0
                    c = float(const_norm) if const_norm else 0
                    
                    centro_x = -a / 2
                    centro_y = -b / 2
                    R_cuadrado = (a/2)**2 + (b/2)**2 - c
                    
                    if R_cuadrado > 0:
                        R = np.sqrt(R_cuadrado)
                        return {
                            'tipo': 'circulo',
                            'centro': (centro_x, centro_y),
                            'radio': R,
                            'ecuacion': str(factor) + ' = 0'
                        }
        except:
            pass
        
        return None
    
    @staticmethod
    def _generar_puntos_prueba(xlim, ylim, max_puntos=None):
        """
        Genera puntos iniciales para búsqueda de equilibrios
        Estrategia mejorada: malla adaptativa + puntos en bordes + origen
        
        Parámetros:
        - max_puntos: limita el número de puntos (útil cuando hay ciclos límite)
        """
        import numpy as np
        puntos = []
        
        # Siempre incluir el origen (importante para sistemas lineales)
        puntos.append((0, 0))
        
        # Si hay límite de puntos, usar solo puntos clave
        if max_puntos and max_puntos < 20:
            # Solo origen y esquinas
            puntos.extend([
                (xlim[0], ylim[0]),
                (xlim[0], ylim[1]),
                (xlim[1], ylim[0]),
                (xlim[1], ylim[1])
            ])
            return puntos[:max_puntos]
        
        # Agregar esquinas del dominio
        puntos.extend([
            (xlim[0], ylim[0]),
            (xlim[0], ylim[1]),
            (xlim[1], ylim[0]),
            (xlim[1], ylim[1])
        ])
        
        # Agregar puntos en los bordes (ayuda a encontrar equilibrios cerca de límites)
        n_bordes = 5
        for i in range(n_bordes):
            t = i / (n_bordes - 1)
            # Borde superior e inferior
            puntos.append((xlim[0] + t * (xlim[1] - xlim[0]), ylim[0]))
            puntos.append((xlim[0] + t * (xlim[1] - xlim[0]), ylim[1]))
            # Borde izquierdo y derecho
            puntos.append((xlim[0], ylim[0] + t * (ylim[1] - ylim[0])))
            puntos.append((xlim[1], ylim[0] + t * (ylim[1] - ylim[0])))
        
        # Malla densa adaptativa (aumentada de 8x8 a 12x12 = 144 puntos)
        n_grid = 12  # Densidad aumentada
        x_range = np.linspace(xlim[0], xlim[1], n_grid)
        y_range = np.linspace(ylim[0], ylim[1], n_grid)
        for xi in x_range:
            for yi in y_range:
                puntos.append((float(xi), float(yi)))
        
        # Agregar puntos en ejes si (0,0) está dentro del dominio
        if xlim[0] <= 0 <= xlim[1]:
            # Puntos en eje X
            for x_val in np.linspace(xlim[0], xlim[1], 8):
                if abs(x_val) > 0.01:  # Evitar duplicar origen
                    puntos.append((float(x_val), 0))
        
        if ylim[0] <= 0 <= ylim[1]:
            # Puntos en eje Y
            for y_val in np.linspace(ylim[0], ylim[1], 8):
                if abs(y_val) > 0.01:  # Evitar duplicar origen
                    puntos.append((0, float(y_val)))
        
        # Agregar puntos en diagonales
        n_diag = 6
        for i in range(n_diag):
            t = i / (n_diag - 1)
            # Diagonal principal
            x_diag = xlim[0] + t * (xlim[1] - xlim[0])
            y_diag = ylim[0] + t * (ylim[1] - ylim[0])
            puntos.append((x_diag, y_diag))
            
            # Diagonal secundaria
            y_diag_inv = ylim[1] - t * (ylim[1] - ylim[0])
            puntos.append((x_diag, y_diag_inv))
        
        return puntos
    
    @staticmethod
    def _es_punto_nuevo(sol, puntos_existentes, tolerancia):
        """Verifica si un punto es nuevo (no está duplicado)"""
        for px, py in puntos_existentes:
            if abs(sol[0] - px) < tolerancia and abs(sol[1] - py) < tolerancia:
                return False
        return True
    
    def resolver_temporal(self, condiciones_iniciales, t_max=10, num_puntos=1000):
        """
        Resuelve el sistema con condiciones iniciales y devuelve la evolución temporal
        
        Parámetros:
        - condiciones_iniciales: [x0, y0] valores iniciales
        - t_max: tiempo máximo de simulación
        - num_puntos: número de puntos de discretización
        
        Retorna:
        - t: array de tiempos
        - solucion: array [x(t), y(t)] con shape (num_puntos, 2)
        """
        t = np.linspace(0, t_max, num_puntos)
        solucion = odeint(self.sistema_ecuaciones, condiciones_iniciales, t)
        return t, solucion
    
    def evaluar_en_tiempo(self, condiciones_iniciales, t_eval):
        """
        Evalúa la solución en un tiempo específico
        
        Parámetros:
        - condiciones_iniciales: [x0, y0]
        - t_eval: tiempo específico a evaluar
        
        Retorna:
        - [x(t_eval), y(t_eval)]
        """
        if t_eval < 0:
            raise ValueError("El tiempo debe ser no negativo")
        
        # Resolver hasta ese tiempo
        t = np.linspace(0, t_eval, max(int(t_eval * 10), 100))
        solucion = odeint(self.sistema_ecuaciones, condiciones_iniciales, t)
        return solucion[-1]
    
    def calcular_trayectoria_completa(self, condiciones_iniciales, t_max=10, 
                                     direccion='ambas', num_puntos=1000):
        """
        Calcula trayectoria completa (hacia adelante y/o atrás en el tiempo)
        
        Parámetros:
        - condiciones_iniciales: [x0, y0]
        - t_max: tiempo máximo
        - direccion: 'adelante', 'atras', o 'ambas'
        - num_puntos: puntos de discretización
        
        Retorna:
        - t: array de tiempos
        - solucion: array de soluciones
        """
        if direccion == 'adelante':
            return self.resolver_temporal(condiciones_iniciales, t_max, num_puntos)
        
        elif direccion == 'atras':
            t = np.linspace(0, -t_max, num_puntos)
            solucion = odeint(self.sistema_ecuaciones, condiciones_iniciales, t)
            return t, solucion
        
        elif direccion == 'ambas':
            # Hacia adelante
            t_fw = np.linspace(0, t_max, num_puntos // 2)
            sol_fw = odeint(self.sistema_ecuaciones, condiciones_iniciales, t_fw)
            
            # Hacia atrás
            t_bw = np.linspace(0, -t_max, num_puntos // 2)
            sol_bw = odeint(self.sistema_ecuaciones, condiciones_iniciales, t_bw)
            
            # Combinar (invertir la parte hacia atrás)
            t_total = np.concatenate([t_bw[::-1], t_fw[1:]])
            sol_total = np.concatenate([sol_bw[::-1], sol_fw[1:]])
            
            return t_total, sol_total
        
        else:
            raise ValueError("direccion debe ser 'adelante', 'atras', o 'ambas'")
    
    def obtener_soluciones_parametricas(self):
        """
        Calcula las soluciones paramétricas x(t) e y(t) para sistemas lineales homogéneos
        
        Retorna:
        - dict con:
          - 'solucion_general': {'x': expresión, 'y': expresión}
          - 'autovalores': [λ1, λ2]
          - 'autovectores': [[v1_x, v1_y], [v2_x, v2_y]]
          - 'tipo': descripción del tipo de solución
          - 'latex': {'x': latex de x(t), 'y': latex de y(t)}
          - 'es_valido': bool
        """
        if self.es_no_lineal:
            return {
                'es_valido': False,
                'mensaje': 'Las soluciones paramétricas solo están disponibles para sistemas lineales homogéneos'
            }
        
        if self.termino_forzado and self.termino_forzado.get('tipo') != 'ninguno':
            return {
                'es_valido': False,
                'mensaje': 'Las soluciones paramétricas mostradas son solo para la parte homogénea del sistema'
            }
        
        try:
            # Si se ingresó por funciones, extraer la matriz de coeficientes
            if self.funcion_personalizada and self.autovalores is None:
                # Evaluar el Jacobiano en (0, 0) para sistemas lineales homogéneos
                # Para sistemas lineales: f(x,y) = ax + by, el Jacobiano es constante
                if self.jacobiano_simbolico is not None:
                    J_en_origen = self.jacobiano_simbolico.subs([(self.x_sym, 0), (self.y_sym, 0)])
                    
                    # Convertir a matriz numpy
                    A = np.array(J_en_origen.tolist(), dtype=float)
                    
                    # Calcular autovalores y autovectores
                    autovalores, autovectores = np.linalg.eig(A)
                else:
                    return {
                        'es_valido': False,
                        'mensaje': 'No se pudo calcular la matriz del sistema'
                    }
            else:
                autovalores = self.autovalores
                autovectores = self.autovectores
            
            # Función auxiliar para convertir números a formas simbólicas exactas
            # Constantes pre-calculadas para eficiencia
            SQRT_2 = sp.sqrt(2)
            SQRT_3 = sp.sqrt(3)
            INV_SQRT_2 = 1/SQRT_2
            
            def numero_a_simbolico(val, tolerancia=1e-3):
                """Convierte un número a su forma simbólica cuando sea posible"""
                if isinstance(val, complex):
                    # Convertir parte real e imaginaria por separado
                    re_simb = numero_a_simbolico(val.real, tolerancia)
                    im_simb = numero_a_simbolico(val.imag, tolerancia)
                    if im_simb == 0:
                        return re_simb
                    return re_simb + sp.I * im_simb
                
                # Casos especiales comunes
                if abs(val) < 1e-10:
                    return sp.Integer(0)
                elif abs(val - 1) < 1e-10:
                    return sp.Integer(1)
                elif abs(val + 1) < 1e-10:
                    return sp.Integer(-1)
                elif abs(val - float(INV_SQRT_2)) < tolerancia:  # ≈ 0.7071
                    return INV_SQRT_2
                elif abs(val + float(INV_SQRT_2)) < tolerancia:  # ≈ -0.7071
                    return -INV_SQRT_2
                elif abs(val - float(SQRT_2)) < tolerancia:  # ≈ 1.4142
                    return SQRT_2
                elif abs(val + float(SQRT_2)) < tolerancia:  # ≈ -1.4142
                    return -SQRT_2
                elif abs(val - 0.5) < 1e-10:
                    return sp.Rational(1, 2)
                elif abs(val + 0.5) < 1e-10:
                    return sp.Rational(-1, 2)
                elif abs(val - float(SQRT_3)) < tolerancia:  # ≈ 1.7321
                    return SQRT_3
                elif abs(val + float(SQRT_3)) < tolerancia:  # ≈ -1.7321
                    return -SQRT_3
                # Si no hay conversión especial, redondear a 4 decimales
                return sp.Float(round(val, 4), 4)
            
            # Variables simbólicas
            t = sp.Symbol('t', real=True, positive=True)
            c1, c2 = sp.symbols('c1 c2', real=True)
            
            # Convertir autovalores y autovectores a formas simbólicas
            λ1 = numero_a_simbolico(autovalores[0])
            λ2 = numero_a_simbolico(autovalores[1])
            
            v1 = np.array([numero_a_simbolico(autovectores[0, 0]), 
                          numero_a_simbolico(autovectores[1, 0])])
            v2 = np.array([numero_a_simbolico(autovectores[0, 1]), 
                          numero_a_simbolico(autovectores[1, 1])])
            
            # Determinar el tipo de solución según los autovalores
            # Verificar si tienen parte imaginaria no nula
            def tiene_parte_imaginaria(λ):
                """Verifica si un autovalor tiene parte imaginaria no nula"""
                # Para símbolos de SymPy o valores complejos
                im_part = sp.im(λ)
                # Convertir a float para comparación numérica
                try:
                    return abs(float(im_part)) > 1e-10
                except (TypeError, ValueError):
                    # Si no se puede convertir, verificar simbólicamente
                    return im_part != 0 and not im_part.is_zero
            
            es_complejo_1 = tiene_parte_imaginaria(λ1)
            es_complejo_2 = tiene_parte_imaginaria(λ2)
            
            if not (es_complejo_1 or es_complejo_2):
                # Autovalores reales
                # Comparar usando SymPy para mayor precisión
                diff = sp.simplify(λ1 - λ2)
                if abs(float(diff)) < 1e-10:  # Autovalor repetido
                    tipo = 'Autovalor repetido'
                    λ = λ1
                    x_t = (c1 * v1[0] + c2 * (v1[0] * t + v2[0])) * sp.exp(λ * t)
                    y_t = (c1 * v1[1] + c2 * (v1[1] * t + v2[1])) * sp.exp(λ * t)
                else:  # Autovalores reales distintos
                    tipo = 'Autovalores reales distintos'
                    x_t = c1 * v1[0] * sp.exp(λ1 * t) + c2 * v2[0] * sp.exp(λ2 * t)
                    y_t = c1 * v1[1] * sp.exp(λ1 * t) + c2 * v2[1] * sp.exp(λ2 * t)
            else:  # Autovalores complejos conjugados
                tipo = 'Autovalores complejos conjugados'
                
                # Extraer parte real e imaginaria de λ1
                if isinstance(λ1, (sp.Add, sp.Mul)):
                    α = sp.re(λ1)
                    β = sp.im(λ1)
                else:
                    λ1_complex = complex(λ1)
                    α = numero_a_simbolico(λ1_complex.real)
                    β = numero_a_simbolico(λ1_complex.imag)
                
                # Extraer parte real e imaginaria del autovector
                u = np.array([sp.re(v1[0]), sp.re(v1[1])])
                w = np.array([sp.im(v1[0]), sp.im(v1[1])])
                
                # Solución: e^(αt)[c1*(u*cos(βt) - w*sin(βt)) + c2*(u*sin(βt) + w*cos(βt))]
                x_t = sp.exp(α * t) * (
                    c1 * (u[0] * sp.cos(β * t) - w[0] * sp.sin(β * t)) +
                    c2 * (u[0] * sp.sin(β * t) + w[0] * sp.cos(β * t))
                )
                y_t = sp.exp(α * t) * (
                    c1 * (u[1] * sp.cos(β * t) - w[1] * sp.sin(β * t)) +
                    c2 * (u[1] * sp.sin(β * t) + w[1] * sp.cos(β * t))
                )
            
            # Simplificar expresiones
            x_t_redondeado = sp.simplify(x_t)
            y_t_redondeado = sp.simplify(y_t)
            
            return {
                'es_valido': True,
                'solucion_general': {
                    'x': str(x_t_redondeado),
                    'y': str(y_t_redondeado)
                },
                'autovalores': [complex(λ1), complex(λ2)],
                'autovectores': [[complex(v1[0]), complex(v1[1])], 
                               [complex(v2[0]), complex(v2[1])]],
                'tipo': tipo,
                'latex': {
                    'x': sp.latex(x_t_redondeado),
                    'y': sp.latex(y_t_redondeado)
                },
                'sympy_expr': {
                    'x': x_t_redondeado,
                    'y': y_t_redondeado
                }
            }
        
        except Exception as e:
            return {
                'es_valido': False,
                'mensaje': f'Error al calcular soluciones paramétricas: {str(e)}'
            }
